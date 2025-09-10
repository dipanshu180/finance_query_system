# Valuefy Backend Deployment Guide

## 🚀 Deploy to Render

### Prerequisites
- GitHub repository with your code
- OpenAI API key
- MongoDB URI (MongoDB Atlas recommended)
- MySQL URI (PlanetScale or similar cloud database recommended)

### Step 1: Prepare Your Repository
1. Make sure all files are committed and pushed to GitHub
2. Ensure your `requirements.txt` is up to date
3. Verify environment variables are properly configured

### Step 2: Deploy to Render

#### Option A: Using render.yaml (Recommended)
1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Blueprint"
4. Connect your repository
5. Render will automatically detect the `render.yaml` file
6. Click "Apply" to deploy

#### Option B: Manual Configuration
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `valuefy-backend`
   - **Root Directory**: `backned`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### Step 3: Configure Environment Variables
In your Render dashboard, go to Environment tab and add:

```
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=your_mongodb_connection_string
MYSQL_URI=your_mysql_connection_string
```

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Your API will be available at: `https://your-app-name.onrender.com`

### Step 5: Test Your Deployment
1. Visit: `https://your-app-name.onrender.com/health`
2. You should see a health check response
3. Test the main endpoint: `https://your-app-name.onrender.com/`

## 🔧 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check if all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **App Crashes on Start**
   - Check environment variables are set correctly
   - Verify database connections work from external IPs
   - Check logs in Render dashboard

3. **Database Connection Issues**
   - Ensure your database allows connections from external IPs
   - Use cloud databases (MongoDB Atlas, PlanetScale) for better reliability
   - Check connection strings are correct

4. **CORS Issues**
   - Update CORS origins in `main.py` to include your frontend domain
   - Ensure `allow_origins` includes your Vercel domain

### Health Check Endpoints
- `/` - Basic API info
- `/health` - Detailed health check with environment status

### Logs
- View logs in Render dashboard under "Logs" tab
- Check for any error messages or warnings

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI functionality | `sk-...` |
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://...` |
| `MYSQL_URI` | MySQL connection string | `mysql://user:pass@host:port/db` |
| `PORT` | Port number (set by Render) | `8000` |

## 🔄 Updating Your Deployment

1. Push changes to your GitHub repository
2. Render will automatically redeploy
3. Check logs for any issues
4. Test the updated endpoints

## 📊 Monitoring

- Monitor your app in Render dashboard
- Check resource usage
- Set up alerts for downtime
- Monitor API response times

## 🆘 Support

If you encounter issues:
1. Check Render documentation
2. Review application logs
3. Verify environment variables
4. Test database connections locally first


