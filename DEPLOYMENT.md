# Deployment Guide 🚀

This guide shows you how to deploy your Roblox Outfit Marketplace Backend to various cloud platforms.

## 🔧 Local Development

For local development with auto-reload and easy access to docs:

```bash
# Option 1: Use the development script
./start_dev.sh

# Option 2: Run uvicorn directly
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
```

**Accessible URLs:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## Quick Start (Recommended for Beginners)

### 1. Railway (Easiest) ⭐

1. Go to [railway.app](https://railway.app)
2. Click "Login with GitHub"
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Click "Deploy"

**That's it!** Railway will:
- Auto-detect Python/FastAPI
- Install dependencies
- Deploy your app
- Give you a public URL

### 2. Render (Great Free Option)

1. Go to [render.com](https://render.com)
2. Connect your GitHub account
3. Click "New Web Service"
4. Select your repository
5. Use these settings:
   - **Name**: `roblox-outfit-backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### 3. Vercel (Serverless)

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel will use the `vercel.json` config automatically
4. Deploy!

## Advanced Deployment Options

### Docker Deployment 🐳

Build and run locally:
```bash
# Build the image
docker build -t roblox-outfit-backend .

# Run the container
docker run -p 8000:8000 roblox-outfit-backend
```

Or use Docker Compose:
```bash
docker-compose up --build
```

### Cloud Platforms

#### Google Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/roblox-outfit-backend

# Deploy to Cloud Run
gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/roblox-outfit-backend --platform managed
```

#### AWS App Runner
1. Push Docker image to ECR
2. Create App Runner service
3. Connect to ECR image

#### DigitalOcean App Platform
1. Connect GitHub repo
2. Select "Web Service"
3. Use Dockerfile for deployment

## Environment Variables

Set these environment variables in your deployment platform:

- `PORT`: The port your app runs on (usually auto-set)
- `PYTHONPATH`: Path to your Python modules (usually `/app`)

## Health Checks

Your API includes a health check endpoint at `/` that returns server information.

## CORS Configuration

The app is configured to accept requests from any origin. In production, you should:

1. Update CORS origins in `server/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourgame.com"],  # Specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Monitoring

Most platforms provide:
- Automatic scaling
- Health monitoring
- Log aggregation
- Performance metrics

## Custom Domain

After deployment, you can:
1. Get your app URL (e.g., `https://your-app.railway.app`)
2. Set up a custom domain in your platform's settings
3. Update DNS records

## Troubleshooting

Common issues and solutions:

1. **Build Fails**: Check your `requirements.txt` file
2. **App Won't Start**: Verify the start command includes `--host 0.0.0.0`
3. **CORS Issues**: Update CORS middleware settings
4. **Performance**: Consider upgrading to paid plans for better resources

## Next Steps

1. Test your deployed API: `https://your-app-url.com/docs`
2. Update your frontend to use the new API URL
3. Set up monitoring and alerts
4. Consider adding authentication for production use

## Support

- Railway: [docs.railway.app](https://docs.railway.app)
- Render: [render.com/docs](https://render.com/docs)
- Vercel: [vercel.com/docs](https://vercel.com/docs)