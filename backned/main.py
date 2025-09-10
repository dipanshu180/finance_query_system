from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import time
from agents.mongo_agent import query_mongo
from agents.sql_agent import query_sql_database


app = FastAPI(title="Valuefy AI Portfolio Assistant", version="1.0.0")

# Add CORS middleware for frontend
import os
allowed_origins = [
    "http://localhost:3000",  # Local development
    "http://localhost:5173",  # Vite dev server
    "https://*.vercel.app",   # Vercel deployments
]

# Add specific Vercel domain if provided
vercel_domain = os.getenv("VERCEL_DOMAIN")
if vercel_domain:
    allowed_origins.append(f"https://{vercel_domain}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    processing_time: Optional[str] = None
    visualization_data: Optional[dict] = None

@app.get("/")
async def root():
    return {"message": "Valuefy AI Portfolio Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify all components are working"""
    try:
        # Check if environment variables are set
        import os
        openai_key = os.getenv("OPENAI_API_KEY")
        mongodb_uri = os.getenv("MONGODB_URI")
        mysql_uri = os.getenv("MYSQL_URI")
        
        # Test database connections
        db_status = {}
        
        # Test MongoDB connection
        try:
            from db.mongo_conn import test_mongodb_connection
            mongo_test = test_mongodb_connection()
            if mongo_test["status"] == "connected":
                db_status["mongodb"] = f"connected ({mongo_test['document_count']} docs)"
            else:
                db_status["mongodb"] = f"error: {mongo_test.get('error', 'Unknown error')[:100]}"
        except Exception as e:
            db_status["mongodb"] = f"error: {str(e)[:100]}"
        
        # Test MySQL connection
        try:
            from db.mysql_conn import connect_mysql
            conn = connect_mysql()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            db_status["mysql"] = "connected"
        except Exception as e:
            db_status["mysql"] = f"error: {str(e)[:100]}"
        
        status = {
            "status": "healthy",
            "openai_configured": bool(openai_key),
            "mongodb_configured": bool(mongodb_uri),
            "mysql_configured": bool(mysql_uri),
            "database_status": db_status,
            "timestamp": time.time()
        }
        
        return status
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }



@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        import time
        start_time = time.time()
        
        # Validate request
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Determine which agent to use based on the question
        question = request.question.lower()
        
        try:
            if any(keyword in question for keyword in ['portfolio', 'client', 'investor', 'risk', 'manager']):
                # Use MongoDB agent for client/portfolio queries
                mongo_response = query_mongo(request.question)
                # Handle both string and dictionary responses from MongoDB agent
                if isinstance(mongo_response, dict):
                    response = mongo_response.get('answer', 'No response from MongoDB agent')
                else:
                    response = str(mongo_response)
            else:
                # Use SQL agent for transaction queries
                response = query_sql_database(request.question)
        except Exception as agent_error:
            # Log the actual error for debugging
            import logging
            logging.error(f"Agent error: {str(agent_error)}")
            import traceback
            logging.error(f"Agent traceback: {traceback.format_exc()}")
            # If agent fails, provide a fallback response
            response = f"Sorry, I encountered an error while processing your question: {str(agent_error)}. Please try rephrasing your question."
        
        processing_time = f"{(time.time() - start_time):.2f}s"
        
        # Add visualization data for certain queries
        visualization_data = None
        if any(keyword in question for keyword in ['top', 'portfolio', 'investor', 'manager']):
            visualization_data = {
                "type": "portfolio_analysis",
                "query": request.question
            }
        
        return QuestionResponse(
            answer=response,
            processing_time=processing_time,
            visualization_data=visualization_data
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the full error for debugging
        import logging
        logging.error(f"Unexpected error in ask_question: {str(e)}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
