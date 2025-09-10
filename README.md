# Valuefy AI Portfolio Assistant

A full-stack AI-powered portfolio analysis application built with FastAPI and React.

## 🚀 Features

- **AI-Powered Chat Interface**: Natural language queries about portfolio data
- **Dual Database Support**: MongoDB for client data, MySQL for transactions
- **Real-time Data Visualization**: Interactive charts and graphs
- **Mock Data Fallback**: Works without databases for testing
- **Modern UI**: Beautiful, responsive design with animations

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11
- **AI Integration**: OpenAI GPT-3.5-turbo for natural language processing
- **Databases**: MongoDB (clients) + MySQL (transactions)
- **Deployment**: Render.com

### Frontend (React + Vite)
- **Framework**: React 19 with Vite
- **UI Library**: Framer Motion for animations
- **Charts**: Recharts for data visualization
- **Deployment**: Vercel

## 📁 Project Structure

```
valuefy/
├── backned/                 # Backend API
│   ├── agents/             # AI agents for MongoDB and SQL
│   ├── db/                 # Database connections
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── render.yaml         # Render deployment config
├── frontend/val_frontend/  # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   └── App.jsx         # Main app component
│   ├── package.json        # Node dependencies
│   └── vercel.json         # Vercel deployment config
└── README.md
```

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key (optional for testing)

### Backend Setup
```bash
cd backned
python -m venv myenv
myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend/val_frontend
npm install
npm run dev
```

### Environment Variables
Create `.env` files with:
```bash
# Backend (.env)
OPENAI_API_KEY=your_openai_key
MONGODB_URI=mongodb+srv://...
MYSQL_URI=mysql://...

# Frontend (.env.local)
VITE_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Backend to Render
1. Push to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy automatically

### Frontend to Vercel
1. Connect GitHub repository
2. Set root directory to `frontend/val_frontend`
3. Add environment variable: `VITE_API_URL`
4. Deploy

## 📊 Database Setup

### MongoDB Atlas (Recommended)
1. Create account at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create cluster and database
3. Get connection string
4. Run `setup_mongodb.js` script

### MySQL (Railway/PlanetScale)
1. Create account at [railway.app](https://railway.app) or [planetscale.com](https://planetscale.com)
2. Create MySQL database
3. Get connection string
4. Run `setup_database.sql` script

## 🧪 Testing

### Health Check
- Backend: `http://localhost:8000/health`
- API Docs: `http://localhost:8000/docs`

### Sample Queries
- "Show me clients with high risk appetite"
- "What are the total transactions?"
- "Find clients who invest in stocks"

## 🔧 Configuration

### CORS Settings
Update `backned/main.py` with your frontend domain:
```python
allowed_origins = [
    "http://localhost:5173",
    "https://your-app.vercel.app"
]
```

### Environment Variables
- `OPENAI_API_KEY`: Required for AI features
- `MONGODB_URI`: Optional, uses mock data if not provided
- `MYSQL_URI`: Optional, uses mock data if not provided
- `VITE_API_URL`: Frontend API endpoint

## 📝 API Endpoints

- `GET /` - API status
- `GET /health` - Health check with database status
- `POST /ask` - Send questions to AI assistant

## 🎨 Features

### Chat Interface
- Real-time messaging
- Typing indicators
- Error handling
- Message history

### Data Visualization
- Portfolio analysis charts
- Risk distribution graphs
- Investment trends
- Manager performance

### AI Capabilities
- Natural language processing
- Context-aware responses
- Query classification
- Fallback responses

## 🚨 Troubleshooting

### Common Issues
1. **CORS Errors**: Update allowed origins in backend
2. **Database Connection**: Check environment variables
3. **Build Failures**: Verify Node.js and Python versions
4. **API Timeouts**: Check network connectivity

### Debug Mode
Set `VITE_DEBUG_MODE=true` for frontend debugging

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check environment variables
4. Verify database connections

---

**Built with ❤️ using FastAPI, React, and AI**
