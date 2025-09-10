# Vercel Deployment Guide for Valuefy Frontend

## 🚀 **Deploy to Vercel - Step by Step**

### **Step 1: Prepare Your Repository**
1. Make sure all changes are committed and pushed to GitHub
2. Verify your `package.json` is correct
3. Check that `vercel.json` is in the `frontend/val_frontend` folder

### **Step 2: Deploy to Vercel**

#### **Option A: Deploy via Vercel Dashboard (Recommended)**
1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Set the **Root Directory** to `frontend/val_frontend`
6. Click "Deploy"

#### **Option B: Deploy via Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend/val_frontend

# Deploy
vercel

# Follow the prompts
```

### **Step 3: Configure Environment Variables**

In your Vercel dashboard:
1. Go to your project
2. Click "Settings" → "Environment Variables"
3. Add these variables:

```
VITE_API_URL=https://your-backend-app.onrender.com
```

### **Step 4: Update Backend CORS (Important!)**

In your Render backend, update the CORS origins to include your Vercel domain:

```python
# In backned/main.py
allowed_origins = [
    "http://localhost:3000",  # Local development
    "http://localhost:5173",  # Vite dev server
    "https://your-app-name.vercel.app",  # Your Vercel domain
]
```

### **Step 5: Test Your Deployment**

1. Visit your Vercel URL: `https://your-app-name.vercel.app`
2. Test the chat interface
3. Check if API calls work
4. Verify all features are working

## 🔧 **Configuration Files**

### **vercel.json**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### **Environment Variables**
- `VITE_API_URL`: Your backend API URL
- `VITE_APP_NAME`: App name (optional)
- `VITE_APP_VERSION`: App version (optional)

## 🚨 **Common Issues & Solutions**

### **1. Build Failures**
- Check if all dependencies are in `package.json`
- Verify Node.js version compatibility
- Check for TypeScript errors

### **2. API Connection Issues**
- Verify `VITE_API_URL` is set correctly
- Check if backend CORS allows your Vercel domain
- Test backend health endpoint

### **3. Environment Variables Not Working**
- Make sure variables start with `VITE_`
- Redeploy after adding new variables
- Check variable names are correct

### **4. Routing Issues**
- Verify `vercel.json` has proper rewrites
- Check if SPA routing is configured

## 📊 **Performance Optimization**

### **Build Optimization**
- Vite automatically optimizes builds
- Assets are minified and compressed
- Code splitting is enabled

### **Caching**
- Static assets are cached for 1 year
- API responses use appropriate cache headers
- CDN distribution worldwide

## 🔄 **Updating Your Deployment**

### **Automatic Updates**
- Push to your main branch
- Vercel automatically redeploys
- Preview deployments for pull requests

### **Manual Updates**
```bash
# In your frontend directory
vercel --prod
```

## 📱 **Mobile Optimization**

Your app is already optimized for mobile:
- Responsive design
- Touch-friendly interface
- Fast loading on mobile networks

## 🔍 **Monitoring & Analytics**

### **Vercel Analytics**
- Built-in performance monitoring
- Real user metrics
- Core Web Vitals tracking

### **Custom Analytics**
- Add Google Analytics if needed
- Use environment variables for configuration

## 🆘 **Troubleshooting**

### **Check Logs**
1. Go to Vercel dashboard
2. Click on your project
3. Go to "Functions" tab
4. Check build and runtime logs

### **Common Commands**
```bash
# Check build locally
npm run build

# Preview production build
npm run preview

# Check environment variables
vercel env ls
```

## 🎯 **Next Steps After Deployment**

1. **Test all features** on the live site
2. **Update backend CORS** with your Vercel domain
3. **Set up custom domain** (optional)
4. **Configure monitoring** and alerts
5. **Set up CI/CD** for automatic deployments

## 📞 **Support**

If you encounter issues:
1. Check Vercel documentation
2. Review build logs
3. Test locally first
4. Check environment variables
5. Verify backend connectivity

Your frontend is now ready for Vercel deployment! 🚀


