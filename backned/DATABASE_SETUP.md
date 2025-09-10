# Database Setup Guide for Valuefy AI Portfolio Assistant

## 🗄️ **Setting Up Cloud MySQL Database**

### **Option 1: PlanetScale (Recommended)**

#### **Step 1: Create Account**
1. Go to [planetscale.com](https://planetscale.com)
2. Sign up with GitHub
3. Verify your email

#### **Step 2: Create Database**
1. Click "Create database"
2. Name: `valuefy`
3. Region: Choose closest to your users
4. Click "Create database"

#### **Step 3: Get Connection String**
1. Click on your `valuefy` database
2. Go to "Connect" tab
3. Click "Connect with" → "General purpose"
4. Copy the connection string
5. It looks like: `mysql://username:password@host:port/database`

#### **Step 4: Set Up Database Schema**
1. In PlanetScale, go to "Console" tab
2. Copy and paste the contents of `setup_database.sql`
3. Run the script to create tables and sample data

### **Option 2: Railway**

#### **Step 1: Create Account**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

#### **Step 2: Create MySQL Database**
1. Click "New Project"
2. Select "Database" → "MySQL"
3. Wait for deployment to complete

#### **Step 3: Get Connection String**
1. Click on your MySQL service
2. Go to "Connect" tab
3. Copy the connection string

#### **Step 4: Set Up Database Schema**
1. Use Railway's database console
2. Run the `setup_database.sql` script

### **Option 3: AWS RDS**

#### **Step 1: Create RDS Instance**
1. Go to AWS Console → RDS
2. Click "Create database"
3. Choose "MySQL"
4. Select "Free tier" template
5. Set database name: `valuefy`

#### **Step 2: Configure Security**
1. Set up security group to allow connections
2. Note down the endpoint and credentials

#### **Step 3: Get Connection String**
Format: `mysql://username:password@endpoint:3306/valuefy`

## 🔧 **Environment Variables**

Add these to your Render deployment:

```
MYSQL_URI=mysql://username:password@host:port/database
```

## 🧪 **Testing Your Database**

### **Test Connection Locally**
```bash
# Install MySQL client
pip install mysql-connector-python

# Test connection
python -c "
from db.mysql_conn import connect_mysql
conn = connect_mysql()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM transactions')
print('Total transactions:', cursor.fetchone()[0])
cursor.close()
conn.close()
"
```

### **Test via API**
1. Deploy to Render
2. Visit: `https://your-app.onrender.com/health`
3. Check if `mysql_configured: true` and `database_status.mysql: connected`

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
- Check if your database allows external connections
- Verify the connection string format
- Ensure your IP is whitelisted (if required)

### **Schema Issues**
- Make sure you ran the `setup_database.sql` script
- Check if the `transactions` table exists
- Verify column names match the code

### **Performance Issues**
- Check if indexes are created
- Monitor database usage in your cloud provider
- Consider upgrading your plan if needed

## 💡 **Pro Tips**

1. **Use connection pooling** for better performance
2. **Monitor your database usage** to avoid hitting limits
3. **Set up backups** for production data
4. **Use environment variables** for sensitive data
5. **Test locally first** before deploying

## 🔄 **Next Steps**

1. Set up your chosen database
2. Add the `MYSQL_URI` to Render
3. Deploy your backend
4. Test the `/health` endpoint
5. Try some SQL queries via the API


