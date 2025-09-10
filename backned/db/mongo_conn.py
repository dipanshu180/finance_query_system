# db/mongo_conn.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

def get_mongo_collection():
    """Get MongoDB collection with proper error handling and cloud support"""
    try:
        # Get MongoDB URI from environment
        uri = os.getenv("MONGODB_URI")
        
        if not uri:
            logger.warning("MONGODB_URI not provided - MongoDB not available")
            raise Exception("MONGODB_URI not provided")
        
        # Parse database and collection names from URI or use defaults
        db_name = os.getenv("MONGODB_DATABASE", "valuefy")
        collection_name = os.getenv("MONGODB_COLLECTION", "clients")
        
        logger.info(f"Connecting to MongoDB: {uri}")
        logger.info(f"Database: {db_name}, Collection: {collection_name}")
        
        # Create MongoDB client with proper configuration
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000,        # 10 second connection timeout
            socketTimeoutMS=20000,         # 20 second socket timeout
            retryWrites=True,              # Enable retryable writes
            maxPoolSize=10,                # Connection pool size
            minPoolSize=1                  # Minimum connections
        )
        
        # Test the connection
        client.admin.command('ping')
        logger.info("MongoDB connection successful")
        
        # Get database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        return collection
        
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
        raise Exception(f"Failed to connect to MongoDB: {str(e)}")

def test_mongodb_connection():
    """Test MongoDB connection and return status"""
    try:
        collection = get_mongo_collection()
        
        # Test basic operations
        count = collection.count_documents({})
        logger.info(f"MongoDB test successful - {count} documents found")
        
        return {
            "status": "connected",
            "document_count": count,
            "database": collection.database.name,
            "collection": collection.name
        }
        
    except Exception as e:
        logger.error(f"MongoDB test failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def get_mongodb_info():
    """Get MongoDB connection information"""
    try:
        uri = os.getenv("MONGODB_URI")
        if not uri:
            return {"status": "not_configured"}
        
        # Parse URI to get connection details (without password)
        if "mongodb+srv://" in uri:
            # Atlas connection
            return {
                "status": "configured",
                "type": "atlas",
                "uri": uri.split("@")[0] + "@***"  # Hide password
            }
        else:
            # Local or other connection
            return {
                "status": "configured", 
                "type": "local",
                "uri": uri
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
