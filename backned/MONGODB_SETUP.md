# MongoDB Setup Guide for Valuefy AI Portfolio Assistant

## 🍃 **Setting Up MongoDB Atlas (Recommended)**

### **Step 1: Create MongoDB Atlas Account**
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
2. Click "Try Free" and sign up
3. Verify your email

### **Step 2: Create Cluster**
1. Choose "Shared" (Free tier)
2. Select a region close to your users
3. Choose "M0 Sandbox" (Free)
4. Click "Create Cluster"

### **Step 3: Set Up Database Access**
1. Go to "Database Access" in the left menu
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and password
5. Set privileges to "Read and write to any database"
6. Click "Add User"

### **Step 4: Set Up Network Access**
1. Go to "Network Access" in the left menu
2. Click "Add IP Address"
3. Choose "Allow access from anywhere" (0.0.0.0/0)
4. Click "Confirm"

### **Step 5: Get Connection String**
1. Go to "Clusters" in the left menu
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your database user password
6. It looks like: `mongodb+srv://username:password@cluster.mongodb.net/`

### **Step 6: Set Up Database Schema**
1. Go to "Clusters" → "Browse Collections"
2. Click "Create Database"
3. Database name: `valuefy`
4. Collection name: `clients`
5. Use MongoDB Compass or Atlas Data Explorer
6. Run the `setup_mongodb.js` script

## 🔧 **Environment Variables for Render**

Add this to your Render deployment:

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/valuefy
```

## 🧪 **Testing Your MongoDB Database**

### **Test Connection Locally**
```bash
# Add your MongoDB URI to .env file
echo "MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/valuefy" >> .env

# Test the connection
python -c "
from db.mongo_conn import get_mongo_collection
collection = get_mongo_collection()
print('Total clients:', collection.count_documents({}))
"
```

### **Test via MongoDB Atlas**
1. Go to your cluster dashboard
2. Click "Browse Collections"
3. Check if the `valuefy.clients` collection exists
4. Verify sample data is loaded

## 📊 **Sample Data Included**

The setup script creates:
- **7 sample clients** with Indian cricket players
- **3 risk appetite levels** (High, Medium, Low)
- **Various investment preferences** (Stocks, Real Estate, Crypto, etc.)
- **3 relationship managers** (RM IDs: 101, 102, 103)
- **Total investment data** for each client

## 🔍 **Query Examples**

Once set up, you can ask:
- "Find clients with high risk appetite"
- "Show me clients who invest in stocks"
- "Which clients prefer real estate?"
- "Find clients managed by RM 101"
- "Show me all clients"

## 🚨 **Troubleshooting**

### **Connection Issues**
- Check if your IP is whitelisted in Network Access
- Verify the connection string format
- Make sure you replaced `<password>` with actual password
- Check if your cluster is running

### **Schema Issues**
- Make sure you ran the `setup_mongodb.js` script
- Check if the `valuefy` database exists
- Verify the `clients` collection exists
- Check if sample data is loaded

### **Performance Issues**
- Check if indexes are created
- Monitor your cluster usage in Atlas
- Consider upgrading your plan if needed

## 💡 **MongoDB Atlas Pro Tips**

1. **Use MongoDB Compass** for database management
2. **Set up monitoring** in Atlas dashboard
3. **Use Atlas Charts** for data visualization
4. **Set up alerts** for cluster issues
5. **Use Atlas Search** for advanced queries

## 🔄 **Alternative: Local MongoDB**

If you prefer local MongoDB:

```bash
# Install MongoDB locally
# Windows: Download from mongodb.com
# Mac: brew install mongodb-community
# Linux: apt-get install mongodb

# Start MongoDB
mongod

# Use local connection string
MONGODB_URI=mongodb://localhost:27017/valuefy
```

## 📱 **MongoDB Mobile App**

MongoDB has a mobile app for monitoring:
- Download from App Store/Google Play
- Monitor your cluster status
- View database metrics
- Check connection health

## 🔄 **Next Steps**

1. Set up MongoDB Atlas database
2. Add the `MONGODB_URI` to Render
3. Deploy your backend
4. Test the `/health` endpoint
5. Try some MongoDB queries via the API


