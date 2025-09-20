# 🚀 Deployment Guide - Telegram FPS Bot

This guide will help you deploy your Telegram FPS bot to various platforms.

## 📋 Prerequisites

Before deploying, make sure you have:

1. **Telegram Bot Token** - Get from [@BotFather](https://t.me/botfather)
2. **Google Cloud Project** - With Drive API enabled
3. **Google OAuth Credentials** - Web application type
4. **Domain/URL** - For OAuth redirect (if using cloud deployment)

## 🔧 Pre-Deployment Setup

### 1. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp env.example .env
```

Edit `.env` with your settings:

```env
BOT_TOKEN=your_telegram_bot_token_here
FLASK_SECRET_KEY=your_secret_key_here
LOG_LEVEL=INFO
```

### 2. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create OAuth2 credentials (Web application)
5. Add your deployment URL to redirect URIs:
   - For Heroku: `https://your-app-name.herokuapp.com/callback`
   - For VPS: `https://yourdomain.com/callback`
   - For local: `http://localhost:8080/callback`
6. Download credentials and save as `client_secrets.json`

## 🌐 Deployment Options

### Option 1: Heroku (Recommended for beginners)

Heroku is the easiest way to deploy your bot with minimal configuration.

#### Steps:

1. **Install Heroku CLI**
   ```bash
   # Visit https://devcenter.heroku.com/articles/heroku-cli
   # Download and install for your OS
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-bot-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set BOT_TOKEN="your_bot_token"
   heroku config:set FLASK_SECRET_KEY="$(openssl rand -base64 32)"
   heroku config:set REDIRECT_URI="https://your-bot-name.herokuapp.com/callback"
   heroku config:set WEB_URL="https://your-bot-name.herokuapp.com"
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Upload Google Credentials**
   ```bash
   # You'll need to add client_secrets.json to your app
   # This can be done via Heroku dashboard or by including it in your repo
   ```

#### Heroku Features:
- ✅ Automatic deployments from Git
- ✅ Built-in SSL certificates
- ✅ Easy scaling
- ✅ Free tier available
- ❌ File system is ephemeral (tokens stored in memory)

### Option 2: Railway

Railway is a modern alternative to Heroku with better free tier.

#### Steps:

1. **Connect GitHub Repository**
   - Go to [Railway](https://railway.app/)
   - Connect your GitHub account
   - Select your repository

2. **Configure Environment Variables**
   - Add all required environment variables in Railway dashboard
   - Set `REDIRECT_URI` to your Railway domain

3. **Deploy**
   - Railway automatically detects your `Dockerfile`
   - Deploys automatically on git push

### Option 3: DigitalOcean App Platform

#### Steps:

1. **Create App**
   - Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
   - Create new app from GitHub

2. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python src/main.py`

3. **Set Environment Variables**
   - Add all required variables in the app settings

### Option 4: VPS/Server Deployment

For more control and better performance, deploy to a VPS.

#### Recommended VPS Providers:
- **DigitalOcean Droplet** ($5/month)
- **Linode** ($5/month)
- **Vultr** ($3.50/month)
- **AWS EC2** (Pay as you go)

#### Steps:

1. **Set up VPS**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Deploy Application**
   ```bash
   # Clone your repository
   git clone https://github.com/yourusername/telegram-fps-bot.git
   cd telegram-fps-bot
   
   # Copy environment file
   cp env.example .env
   # Edit .env with your settings
   
   # Deploy with Docker Compose
   docker-compose up -d
   ```

3. **Set up Reverse Proxy (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **Set up SSL (Let's Encrypt)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

## 🐳 Docker Deployment

If you prefer Docker, you can use the provided Docker configuration:

### Build and Run Locally
```bash
# Build the image
docker build -t telegram-fps-bot .

# Run the container
docker run -p 8080:8080 --env-file .env telegram-fps-bot
```

### Using Docker Compose
```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## 🔧 Production Configuration

### Environment Variables for Production

```env
# Required
BOT_TOKEN=your_telegram_bot_token
FLASK_SECRET_KEY=your_very_secure_secret_key

# Optional
LOG_LEVEL=INFO
REDIRECT_URI=https://yourdomain.com/callback
WEB_URL=https://yourdomain.com
PORT=8080
FLASK_DEBUG=False
```

### Security Considerations

1. **Use strong secret keys**
   ```bash
   # Generate a secure secret key
   openssl rand -base64 32
   ```

2. **Enable HTTPS** - Always use SSL certificates in production

3. **Set up monitoring** - Use services like:
   - UptimeRobot for uptime monitoring
   - Sentry for error tracking
   - LogRocket for user session recording

4. **Rate limiting** - The bot includes built-in rate limiting

5. **File cleanup** - Temporary files are automatically cleaned up

## 📊 Monitoring and Maintenance

### Health Checks

Your bot includes health check endpoints:
- `GET /` - Main page
- `GET /health` - Health check (if implemented)

### Logs

Monitor your bot logs:
```bash
# Docker
docker-compose logs -f

# Heroku
heroku logs --tail

# Systemd (if running as service)
journalctl -u telegram-bot -f
```

### Updates

To update your bot:
```bash
# Git-based deployment
git pull origin main
git push heroku main  # For Heroku

# Docker deployment
docker-compose down
docker-compose pull
docker-compose up -d
```

## 🚨 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check BOT_TOKEN is correct
   - Verify bot is running
   - Check logs for errors

2. **Authentication fails**
   - Verify Google OAuth credentials
   - Check redirect URI matches your domain
   - Ensure Google Drive API is enabled

3. **Uploads fail**
   - Check Google Drive storage space
   - Verify user has authenticated
   - Check file size limits

4. **Web server not starting**
   - Check port is available
   - Verify environment variables
   - Check logs for errors

### Getting Help

1. Check the logs first
2. Verify all environment variables are set
3. Test locally before deploying
4. Check the troubleshooting section in README.md

## 📈 Scaling

### Horizontal Scaling

For high traffic, consider:
- Load balancer (nginx, HAProxy)
- Multiple bot instances
- Database for shared state
- Redis for session storage

### Vertical Scaling

- Increase server resources
- Optimize code for performance
- Use CDN for static files
- Implement caching

## 🔄 Backup and Recovery

### Important Files to Backup

1. **User tokens** - `token_*.json` files
2. **Configuration** - `.env` file
3. **Google credentials** - `client_secrets.json`
4. **Application code** - Git repository

### Backup Strategy

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "backup_$DATE.tar.gz" token_*.json .env client_secrets.json
```

## 📞 Support

If you need help with deployment:

1. Check this guide first
2. Review the logs
3. Test locally
4. Create an issue on GitHub
5. Contact the bot administrator

---

**Happy Deploying! 🚀**
