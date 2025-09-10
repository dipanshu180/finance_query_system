from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import warnings
import re
import logging
import traceback
from typing import Optional, Dict, Any

# Suppress LangSmith warnings
warnings.filterwarnings('ignore', category=UserWarning, module='langsmith')

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
mysql_uri = os.getenv("MYSQL_URI")

if not openai_api_key:
    logger.error("OPENAI_API_KEY missing in .env")
    raise ValueError("OPENAI_API_KEY missing in .env")

# MySQL is optional for deployment
if not mysql_uri:
    logger.warning("MYSQL_URI not provided - SQL queries will use mock data")
    MYSQL_AVAILABLE = False
else:
    MYSQL_AVAILABLE = True
    logger.info("MySQL URI provided - will attempt to connect to database")

class SQLQueryAgent:
    """Production-ready SQL Query Agent with enhanced error handling and fallback"""
    
    def __init__(self):
        try:
            if not MYSQL_AVAILABLE:
                logger.warning("MySQL not available - using mock mode")
                self.db = None
                self.agent = None
                self.schema_info = None
            else:
                self.db = SQLDatabase.from_uri(mysql_uri)
                self.schema_info = None
                self._init_schema_info()
                self._init_agent()
            
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo", 
                temperature=0, 
                api_key=openai_api_key,
                max_tokens=1500,
                timeout=30  # Add timeout
            )
        except Exception as e:
            logger.error(f"Failed to initialize SQLQueryAgent: {str(e)}")
            raise Exception(f"Failed to initialize SQL agent: {str(e)}")
    
    def _init_schema_info(self):
        """Initialize and cache schema information"""
        try:
            self.schema_info = self.db.get_table_info()
            logger.info("✅ Schema information loaded successfully!")
        except Exception as e:
            logger.error(f"⚠️ Failed to load schema: {str(e)}")
            self.schema_info = None
    
    def _init_agent(self):
        """Initialize the SQL agent with proper error handling"""
        try:
            toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            tools = toolkit.get_tools()
            
            # Custom prompt for better SQL generation
            custom_prompt = PromptTemplate(
                template="""You are a SQL expert helping to query a MySQL database. 

Database Schema:
{schema}

Available tools:
{tools}

IMPORTANT RULES:
1. Always check the schema before writing queries
2. Use EXACT column names from the schema: transaction_id, client_id, stock_name, amount_invested, date_, rm_name
3. The table name is 'transactions'
4. Use proper MySQL syntax
5. Format dates as 'YYYY-MM-DD' 
6. Always provide a clear final answer
7. If you encounter an error, analyze it and try a corrected query

Use this format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought:{agent_scratchpad}""",
                input_variables=["input", "agent_scratchpad"],
                partial_variables={
                    "schema": self.schema_info or "Schema not available",
                    "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
                    "tool_names": ", ".join([tool.name for tool in tools])
                }
            )
            
            # Create agent
            agent = create_react_agent(self.llm, tools, custom_prompt)
            
            # Create agent executor with better configuration
            self.agent = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,  # Increased iterations
                max_execution_time=60,  # Added timeout
                return_intermediate_steps=True
            )
            
            logger.info("SQL Agent initialized successfully!")
            
        except Exception as e:
            logger.error(f"Agent initialization failed: {str(e)}")
            self.agent = None
    
    def query(self, question: str) -> str:
        """Query the database with the given question"""
        logger.info(f"🔍 Processing question: {question}")
        
        if not question or not question.strip():
            return "Please provide a valid question."
        
        # If MySQL is not available, return mock data
        if not MYSQL_AVAILABLE or not self.db:
            return self._get_mock_sql_response(question)
        
        # Try agent first
        if self.agent:
            try:
                response = self.agent.invoke({"input": question})
                output = response.get('output', 'No output found')
                
                # Check if the response is meaningful
                if output and len(output.strip()) > 10 and "Agent stopped" not in output:
                    return output
                else:
                    logger.info("Agent response insufficient, trying fallback...")
                    
            except Exception as e:
                logger.error(f"Agent failed: {str(e)}")
                logger.info("Falling back to direct SQL generation...")
        
        # Fallback to direct SQL generation
        return self._direct_sql_query(question)
    
    def _get_mock_sql_response(self, question: str) -> str:
        """Provide mock SQL responses when MySQL is not available"""
        question_lower = question.lower()
        
        # Mock transaction data
        mock_transactions = [
            {"transaction_id": "T001", "client_id": "C001", "stock_name": "Reliance", "amount_invested": 50000, "date_": "2024-01-15", "rm_name": "John Doe"},
            {"transaction_id": "T002", "client_id": "C002", "stock_name": "TCS", "amount_invested": 75000, "date_": "2024-01-16", "rm_name": "Jane Smith"},
            {"transaction_id": "T003", "client_id": "C001", "stock_name": "Infosys", "amount_invested": 30000, "date_": "2024-01-17", "rm_name": "John Doe"},
            {"transaction_id": "T004", "client_id": "C003", "stock_name": "HDFC Bank", "amount_invested": 100000, "date_": "2024-01-18", "rm_name": "Mike Johnson"},
            {"transaction_id": "T005", "client_id": "C002", "stock_name": "Wipro", "amount_invested": 45000, "date_": "2024-01-19", "rm_name": "Jane Smith"}
        ]
        
        # Generate response based on question
        if 'total' in question_lower and 'transaction' in question_lower:
            return f"Total transactions: {len(mock_transactions)} [Note: Using mock data - MySQL not available]"
        elif 'total' in question_lower and 'amount' in question_lower:
            total_amount = sum(t['amount_invested'] for t in mock_transactions)
            return f"Total amount invested: ₹{total_amount:,} [Note: Using mock data - MySQL not available]"
        elif 'top' in question_lower and 'client' in question_lower:
            client_totals = {}
            for t in mock_transactions:
                client_id = t['client_id']
                client_totals[client_id] = client_totals.get(client_id, 0) + t['amount_invested']
            top_client = max(client_totals.items(), key=lambda x: x[1])
            return f"Top client by investment: {top_client[0]} with ₹{top_client[1]:,} [Note: Using mock data - MySQL not available]"
        elif 'stock' in question_lower:
            stocks = list(set(t['stock_name'] for t in mock_transactions))
            return f"Stocks invested in: {', '.join(stocks)} [Note: Using mock data - MySQL not available]"
        else:
            # Return sample transactions
            sample = mock_transactions[:3]
            result = "Sample transactions:\n"
            for t in sample:
                result += f"- {t['client_id']}: {t['stock_name']} (₹{t['amount_invested']:,}) on {t['date_']}\n"
            return result + "[Note: Using mock data - MySQL not available]"
    
    def _direct_sql_query(self, question: str) -> str:
        """Enhanced direct SQL query generation and execution"""
        try:
            # Generate SQL query
            sql_query = self._generate_sql_query(question)
            if not sql_query:
                return "Could not generate SQL query"
            
            logger.info(f"Generated SQL: {sql_query}")
            
            # Execute query with retry logic
            result = self._execute_query_with_retry(sql_query, question)
            
            # Format and return response
            return self._format_response(question, sql_query, result)
                
        except Exception as e:
            logger.error(f"Error in SQL handler: {str(e)}")
            return f"Error in SQL handler: {str(e)}"
    
    def _generate_sql_query(self, question: str) -> Optional[str]:
        """Generate SQL query using LLM"""
        try:
            sql_prompt = f"""
Based on this MySQL database schema:
{self.schema_info}

Generate a SQL query to answer: {question}

CRITICAL RULES:
1. Use EXACT column names: transaction_id, client_id, stock_name, amount_invested, date_, rm_name
2. Table name is: transactions
3. Use proper MySQL syntax
4. For date filtering, use date_ column with format 'YYYY-MM-DD'
5. Use LIMIT 10 for large result sets
6. Return ONLY the SQL query, no explanation

SQL Query:"""
            
            response = self.llm.invoke(sql_prompt)
            sql_query = self._clean_sql_query(response.content)
            
            return sql_query
            
        except Exception as e:
            logger.error(f"SQL generation error: {str(e)}")
            return None
    
    def _clean_sql_query(self, sql_query: str) -> str:
        """Clean and format SQL query"""
        # Remove code blocks
        sql_query = re.sub(r'```sql\n?', '', sql_query)
        sql_query = re.sub(r'```\n?', '', sql_query)
        
        # Remove extra whitespace
        sql_query = sql_query.strip()
        
        # Ensure semicolon at end
        if not sql_query.endswith(';'):
            sql_query += ';'
            
        return sql_query
    
    def _execute_query_with_retry(self, sql_query: str, question: str) -> str:
        """Execute query with error handling and retry logic"""
        try:
            result = self.db.run(sql_query)
            logger.info(f"Raw Result: {result}")
            return result
            
        except Exception as query_error:
            error_msg = str(query_error)
            logger.error(f"Query error: {error_msg}")
            
            # Try to fix common errors
            if "Unknown column" in error_msg:
                # Try to fix column name issues
                corrected_query = self._fix_column_names(sql_query)
                if corrected_query != sql_query:
                    logger.info(f"Retrying with corrected query: {corrected_query}")
                    try:
                        result = self.db.run(corrected_query)
                        logger.info(f"Retry Result: {result}")
                        return result
                    except Exception as retry_error:
                        logger.error(f"Retry failed: {str(retry_error)}")
            
            return f"Query execution failed: {error_msg}"
    
    def _fix_column_names(self, sql_query: str) -> str:
        """Fix common column name issues"""
        # Common column name fixes
        replacements = {
            'transactoin_id': 'transaction_id',  # Fix the typo in the database
            'amount': 'amount_invested',
            'transaction_date': 'date_',
            'date': 'date_',
            'rm': 'rm_name',
            'relationship_manager': 'rm_name'
        }
        
        corrected_query = sql_query
        for wrong, correct in replacements.items():
            corrected_query = re.sub(rf'\b{wrong}\b', correct, corrected_query, flags=re.IGNORECASE)
        
        return corrected_query
    
    def _format_response(self, question: str, sql_query: str, result: str) -> str:
        """Format the final response"""
        if "Query execution failed" in result:
            return result
        
        try:
            format_prompt = f"""
Question: {question}
SQL Query: {sql_query}
Query Result: {result}

Please provide a clear, natural language answer to the original question based on these results.

Guidelines:
1. Be concise but informative
2. Format numbers with commas for readability
3. Include currency symbols (₹) where applicable
4. If result is empty, say "No data found"
5. For lists, format them nicely
6. Don't include technical SQL details in the answer

Answer:"""
            
            formatted_response = self.llm.invoke(format_prompt)
            return formatted_response.content
            
        except Exception as e:
            logger.error(f"Formatting error: {str(e)}")
            return f"Result: {result}\n(Formatting error: {str(e)})"

def test_agent():
    """Test the SQL agent with various queries"""
    
    # Initialize agent
    try:
        agent = SQLQueryAgent()
    except Exception as e:
        logger.error(f"Failed to initialize agent for testing: {str(e)}")
        return
    
    # Test questions
    test_questions = [
        "How many total transactions are there?",
        "What is the total amount invested across all transactions?",
        "Show me the top clients by investment amount",
        "Which stocks have been invested in?",
        "Who is the relationship manager for client C001?",
        "What transactions happened in January 2025?",
        "Show me all transactions with their details"
    ]
    
    logger.info("🚀 Testing SQL Agent with various queries...")
    
    for i, question in enumerate(test_questions, 1):
        logger.info(f"\n{'='*70}")
        logger.info(f"Test {i}: {question}")
        logger.info('='*70)
        
        try:
            response = agent.query(question)
            logger.info("Response:")
            logger.info(response)
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        
        logger.info("")  # Add spacing between tests

def debug_database():
    """Debug database connection and structure"""
    try:
        db = SQLDatabase.from_uri(mysql_uri)
        logger.info("🔍 Database Debug Info:")
        logger.info(f"Tables: {db.get_usable_table_names()}")
        logger.info(f"Schema:\n{db.get_table_info()}")
        
        # Test a simple query
        result = db.run("SELECT COUNT(*) as total FROM transactions")
        logger.info(f"Total transactions: {result}")
        
    except Exception as e:
        logger.error(f"Database debug error: {str(e)}")

# Main query function for external use
def query_sql_database(question: str) -> str:
    """Main function to query the SQL database"""
    try:
        agent = SQLQueryAgent()
        return agent.query(question)
    except Exception as e:
        logger.error(f"Error in query_sql_database: {str(e)}")
        return f"Error: {str(e)}"


def get_sql_agent():
    """Get SQL agent instance for external use"""
    try:
        return SQLQueryAgent()
    except Exception as e:
        logger.error(f"Failed to initialize SQL agent: {str(e)}")
        raise Exception(f"Failed to initialize SQL agent: {str(e)}")

if __name__ == "__main__":
    debug_database()
    logger.info("\n" + "="*80 + "\n")
    test_agent()



