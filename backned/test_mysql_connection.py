#!/usr/bin/env python3
"""
Test MySQL connection with PlanetScale
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mysql_connection():
    """Test MySQL connection"""
    try:
        from db.mysql_conn import connect_mysql
        
        print("🔍 Testing MySQL connection...")
        conn = connect_mysql()
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) as total FROM transactions")
        count = cursor.fetchone()[0]
        print(f"✅ Total transactions: {count}")
        
        # Test sample data
        cursor.execute("SELECT * FROM transactions LIMIT 3")
        rows = cursor.fetchall()
        print("✅ Sample transactions:")
        for row in rows:
            print(f"   - {row[0]}: {row[2]} (₹{row[3]:,}) on {row[4]}")
        
        # Test total amount
        cursor.execute("SELECT SUM(amount_invested) as total FROM transactions")
        total = cursor.fetchone()[0]
        print(f"✅ Total amount invested: ₹{total:,.2f}")
        
        cursor.close()
        conn.close()
        print("✅ MySQL connection test successful!")
        
    except Exception as e:
        print(f"❌ MySQL connection failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you set MYSQL_URI in your .env file")
        print("2. Check if your PlanetScale database is running")
        print("3. Verify the connection string format")
        print("4. Make sure you ran the setup_database.sql script")

if __name__ == "__main__":
    test_mysql_connection()


