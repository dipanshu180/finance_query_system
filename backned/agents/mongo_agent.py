# agents/mongo_agent.py

from db.mongo_conn import get_mongo_collection
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import ast
import json
import time

load_dotenv()

# Try to get MongoDB collection, but don't fail if it's not available
try:
    if os.getenv("MONGODB_URI"):
        collection = get_mongo_collection()
        MONGODB_AVAILABLE = True
    else:
        print("⚠️ MongoDB URI not provided - using mock data")
        collection = None
        MONGODB_AVAILABLE = False
except Exception as e:
    print(f"⚠️ MongoDB not available: {str(e)}")
    collection = None
    MONGODB_AVAILABLE = False

# Setup LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

template = """
You are a MongoDB query generator.
The MongoDB collection is called `clients`. Each document looks like this:
{{
  "client_id": "C001",
  "name": "Virat Kohli",
  "risk_appetite": "High",
  "investment_preferences": ["Stocks", "Real Estate"],
  "rm_id": 101
}}

Convert the user's question into a MongoDB query **filter** in JSON format.
ONLY return the valid JSON object with the query. No explanation, no markdown formatting.

User Question:
"{question}"
"""

prompt = PromptTemplate.from_template(template)

def query_mongo(question: str):
    start = time.time()

    try:
        # If MongoDB is not available, provide mock responses
        if not MONGODB_AVAILABLE:
            return get_mock_response(question, start)
        
        # First, let's check if we have any data in the collection
        total_clients = collection.count_documents({})
        if total_clients == 0:
            return {
                "answer": "No client data found in the database. Please add some sample client data first.",
                "query": question,
                "processing_time": f"{time.time() - start:.2f}s"
            }

        # Format the prompt with user question
        final_prompt = prompt.format(question=question)

        # Get response from OpenAI LLM
        llm_response = llm.invoke(final_prompt).content.strip()
        
        # Clean the response - remove any markdown formatting
        llm_response = llm_response.replace('```python', '').replace('```', '').strip()

        try:
            # Try to parse as JSON first (for MongoDB queries with operators)
            query_dict = json.loads(llm_response)
        except json.JSONDecodeError:
            try:
                # Fallback to ast.literal_eval for simple Python dicts
                query_dict = ast.literal_eval(llm_response)
            except Exception as parse_error:
                # Try to create a simple query based on keywords
                query_dict = create_simple_query(question)
                if not query_dict:
                    return {
                        "answer": f"Could not parse LLM output: {llm_response}. Error: {str(parse_error)}",
                        "query": question,
                        "processing_time": f"{time.time() - start:.2f}s"
                    }

        # Query MongoDB
        results = list(collection.find(query_dict))
        
        if not results:
            answer = "No matching clients found for your query."
        else:
            # Format the results nicely
            client_info = []
            for doc in results:
                client_info.append(f"{doc.get('name', 'Unknown')} (ID: {doc.get('client_id', 'N/A')}, Risk: {doc.get('risk_appetite', 'N/A')})")
            
            answer = f"Found {len(results)} client(s): {', '.join(client_info)}"

        return {
            "answer": answer,
            "query": question,
            "processing_time": f"{time.time() - start:.2f}s"
        }

    except Exception as e:
        return {
            "answer": f"Error querying MongoDB: {str(e)}",
            "query": question,
            "processing_time": f"{time.time() - start:.2f}s"
        }

def get_mock_response(question: str, start_time: float):
    """Provide mock responses when MongoDB is not available"""
    question_lower = question.lower()
    
    # Mock client data
    mock_clients = [
        {"name": "Virat Kohli", "client_id": "C001", "risk_appetite": "High", "investment_preferences": ["Stocks", "Real Estate"]},
        {"name": "Rohit Sharma", "client_id": "C002", "risk_appetite": "Medium", "investment_preferences": ["Stocks", "Bonds"]},
        {"name": "MS Dhoni", "client_id": "C003", "risk_appetite": "Low", "investment_preferences": ["Bonds", "Fixed Deposits"]},
        {"name": "KL Rahul", "client_id": "C004", "risk_appetite": "High", "investment_preferences": ["Stocks", "Real Estate", "Crypto"]},
        {"name": "Rishabh Pant", "client_id": "C005", "risk_appetite": "Medium", "investment_preferences": ["Stocks", "Mutual Funds"]}
    ]
    
    # Filter based on question keywords
    if 'high' in question_lower and 'risk' in question_lower:
        filtered_clients = [c for c in mock_clients if c['risk_appetite'] == 'High']
        client_names = [f"{c['name']} (ID: {c['client_id']})" for c in filtered_clients]
        answer = f"Found {len(filtered_clients)} client(s) with high risk appetite: {', '.join(client_names)}"
    elif 'low' in question_lower and 'risk' in question_lower:
        filtered_clients = [c for c in mock_clients if c['risk_appetite'] == 'Low']
        client_names = [f"{c['name']} (ID: {c['client_id']})" for c in filtered_clients]
        answer = f"Found {len(filtered_clients)} client(s) with low risk appetite: {', '.join(client_names)}"
    elif 'medium' in question_lower and 'risk' in question_lower:
        filtered_clients = [c for c in mock_clients if c['risk_appetite'] == 'Medium']
        client_names = [f"{c['name']} (ID: {c['client_id']})" for c in filtered_clients]
        answer = f"Found {len(filtered_clients)} client(s) with medium risk appetite: {', '.join(client_names)}"
    elif 'stocks' in question_lower:
        filtered_clients = [c for c in mock_clients if 'Stocks' in c['investment_preferences']]
        client_names = [f"{c['name']} (ID: {c['client_id']})" for c in filtered_clients]
        answer = f"Found {len(filtered_clients)} client(s) who invest in stocks: {', '.join(client_names)}"
    elif 'real estate' in question_lower or 'property' in question_lower:
        filtered_clients = [c for c in mock_clients if 'Real Estate' in c['investment_preferences']]
        client_names = [f"{c['name']} (ID: {c['client_id']})" for c in filtered_clients]
        answer = f"Found {len(filtered_clients)} client(s) who invest in real estate: {', '.join(client_names)}"
    else:
        # Return all clients
        client_info = [f"{c['name']} (ID: {c['client_id']}, Risk: {c['risk_appetite']})" for c in mock_clients]
        answer = f"Found {len(mock_clients)} client(s): {', '.join(client_info)}"
    
    return {
        "answer": f"{answer} [Note: Using mock data - MongoDB not available]",
        "query": question,
        "processing_time": f"{time.time() - start_time:.2f}s"
    }

def create_simple_query(question: str):
    """Create a simple MongoDB query based on keywords"""
    question_lower = question.lower()
    
    if 'high' in question_lower and 'risk' in question_lower:
        return {"risk_appetite": "High"}
    elif 'low' in question_lower and 'risk' in question_lower:
        return {"risk_appetite": "Low"}
    elif 'medium' in question_lower and 'risk' in question_lower:
        return {"risk_appetite": "Medium"}
    elif 'stocks' in question_lower:
        return {"investment_preferences": "Stocks"}
    elif 'real estate' in question_lower or 'property' in question_lower:
        return {"investment_preferences": "Real Estate"}
    else:
        # Return all clients if no specific criteria
        return {}
