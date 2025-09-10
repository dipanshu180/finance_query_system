# Railway MySQL Setup Guide for Valuefy AI Portfolio Assistant

## 🚂 **Setting Up MySQL on Railway**

### **Step 1: Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Click "Login" and sign up with GitHub
3. Verify your email if prompted

### **Step 2: Create MySQL Database**
1. Click "New Project"
2. Select "Database" from the options
3. Choose "MySQL" from the database options
4. Wait for deployment (takes 1-2 minutes)
5. Your MySQL database will be automatically created

### **Step 3: Get Connection String**
1. Click on your MySQL service in the project dashboard
2. Go to "Connect" tab
3. Copy the connection string
4. It looks like: `mysql://root:password@host:port/railway`

### **Step 4: Set Up Database Schema**
1. In Railway, go to "Query" tab
2. Copy the entire contents of `setup_database.sql`
3. Paste and run it in the query console
4. This creates your tables and sample data

## 🔧 **Environment Variables for Render**

Add this to your Render deployment:

```
MYSQL_URI=mysql://root:password@host:port/railway
```

## 🧪 **Testing Your Railway Database**

### **Test Connection Locally**
```bash
# Add your MySQL URI to .env file
echo "MYSQL_URI=your_railway_connection_string" >> .env

# Test the connection
python test_mysql_connection.py
```

### **Test via Railway Console**
1. Go to Railway dashboard
2. Click on your MySQL service
3. Go to "Query" tab
4. Run: `SELECT COUNT(*) FROM transactions;`

## 📊 **Sample Data Included**

The setup script creates:
- **10 sample transactions** with real Indian companies
- **4 different clients** (C001-C004)
- **3 relationship managers**
- **Various stock investments** (Reliance, TCS, Infosys, etc.)
- **Total investment**: ₹5,85,000

## 🔍 **Query Examples**

Once set up, you can ask:
- "Show me total transactions"
- "Which client invested the most?"
- "What stocks are available?"
- "Show me transactions by John Doe"
- "What's the total amount invested?"

## 🚨 **Troubleshooting**

### **Connection Issues**
- Check if your Railway service is running
- Verify the connection string format
- Make sure you copied the full connection string

### **Schema Issues**
- Make sure you ran the `setup_database.sql` script
- Check if the `transactions` table exists
- Verify column names match the code

### **Performance Issues**
- Railway free tier has limits
- Monitor your usage in Railway dashboard
- Consider upgrading if needed

## 💡 **Railway Pro Tips**

1. **Use Railway's built-in console** for database management
2. **Monitor your usage** in the Railway dashboard
3. **Set up environment variables** in Railway for easy management
4. **Use Railway's CLI** for advanced operations
5. **Check Railway's status page** if you have issues

## 🔄 **Next Steps**

1. Set up Railway MySQL database
2. Add the `MYSQL_URI` to Render
3. Deploy your backend
4. Test the `/health` endpoint
5. Try some SQL queries via the API

## 📱 **Railway Mobile App**

Railway has a mobile app for monitoring your services:
- Download from App Store/Google Play
- Monitor your database usage
- Check service status
- View logs and metrics


