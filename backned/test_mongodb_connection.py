#!/usr/bin/env python3
"""
Test MongoDB connection with Atlas
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from db.mongo_conn import get_mongo_collection
        
        print("🔍 Testing MongoDB connection...")
        collection = get_mongo_collection()
        
        # Test basic query
        total_clients = collection.count_documents({})
        print(f"✅ Total clients: {total_clients}")
        
        # Test sample data
        sample_clients = list(collection.find().limit(3))
        print("✅ Sample clients:")
        for client in sample_clients:
            print(f"   - {client.get('name', 'Unknown')} (ID: {client.get('client_id', 'N/A')}, Risk: {client.get('risk_appetite', 'N/A')})")
        
        # Test risk appetite queries
        high_risk = collection.count_documents({"risk_appetite": "High"})
        medium_risk = collection.count_documents({"risk_appetite": "Medium"})
        low_risk = collection.count_documents({"risk_appetite": "Low"})
        
        print(f"✅ Risk distribution:")
        print(f"   - High risk: {high_risk} clients")
        print(f"   - Medium risk: {medium_risk} clients")
        print(f"   - Low risk: {low_risk} clients")
        
        # Test investment preferences
        stocks_clients = collection.count_documents({"investment_preferences": "Stocks"})
        real_estate_clients = collection.count_documents({"investment_preferences": "Real Estate"})
        
        print(f"✅ Investment preferences:")
        print(f"   - Stocks: {stocks_clients} clients")
        print(f"   - Real Estate: {real_estate_clients} clients")
        
        print("✅ MongoDB connection test successful!")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you set MONGODB_URI in your .env file")
        print("2. Check if your MongoDB Atlas cluster is running")
        print("3. Verify the connection string format")
        print("4. Make sure you ran the setup_mongodb.js script")
        print("5. Check if your IP is whitelisted in Atlas")

if __name__ == "__main__":
    test_mongodb_connection()


