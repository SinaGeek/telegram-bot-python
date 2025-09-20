# 🤖 WOWDrive Bot

A powerful Telegram bot that uploads files directly to Google Drive with support for large files, progress tracking, and comprehensive file management.

## ✨ Features

- 📤 **File Upload**: Upload any file from Telegram to Google Drive
- 🔄 **Chunked Upload**: Handle large files (>20MB) with progress tracking
- 📊 **Real-time Progress**: Live progress updates every 20 seconds
- 📁 **File Management**: List, rename, and delete files
- 💾 **Storage Stats**: View your Google Drive storage usage
- 🔐 **Secure Auth**: OAuth2 authentication with Google Drive
- ⚡ **Queue System**: Handle multiple uploads efficiently
- 🎯 **Smart Upload**: Direct upload for small files, chunked for large ones

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Google Cloud Project with Drive API enabled

### 2. Installation

```bash
# Clone or download the project
cd FPS

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py
```

### 3. Configuration

#### Telegram Bot Setup
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token

#### Google Drive API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create OAuth2 credentials (Desktop application)
5. Download the `credentials.json` file

#### Environment Configuration
1. Edit `.env` file:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   LOG_LEVEL=INFO
   ```

2. Replace `credentials.json` with your Google Cloud credentials

### 4. Run the Bot

```bash
python run.py
```

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show welcome message |
| `/help` | Show help message and available commands |
| `/login` | Connect your Google Drive account |
| `/stat` | Show your Drive storage usage |
| `/list` | List your recent files |
| `/rename <fileId> <newName>` | Rename a file in Drive |
| `/remove <fileId>` | Delete a file from Drive |
| `/privacy` | View privacy policy and terms |

## 📤 Upload Process

### Small Files (≤20MB)
1. Send file to bot
2. File is queued for upload
3. Direct upload to Google Drive
4. Completion notification with file ID

### Large Files (>20MB)
1. Send file to bot
2. File is queued for upload
3. Chunked upload with progress tracking
4. Progress updates every 20 seconds
5. Completion notification with file ID

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
# File size limits
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB

# Upload settings
CHUNK_SIZE = 1024 * 1024  # 1MB chunks
PROGRESS_UPDATE_INTERVAL = 20  # seconds

# Rate limiting
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_PERIOD = 60  # seconds
```

## 🏗️ Project Structure

```
FPS/
├── bot.py                 # Main bot implementation
├── config.py             # Configuration settings
├── telegram_downloader.py # Telegram file downloader
├── setup.py              # Setup script
├── run.py                # Run script
├── example_usage.py      # Example usage
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .env                 # Environment variables (create this)
├── credentials.json     # Google credentials (add this)
└── uploads/            # Temporary upload folder
```

## 🔐 Security & Privacy

- **OAuth2 Authentication**: Secure Google Drive access
- **No Data Storage**: Files are uploaded directly to your Drive
- **Token Management**: Credentials stored per user
- **Revocable Access**: Revoke access anytime from Google Account
- **Privacy First**: No file content stored on bot server

## 🛠️ Development

### Running Tests
```bash
python example_usage.py
```

### Adding Features
1. Modify `bot.py` for new commands
2. Update `config.py` for new settings
3. Add handlers in the `main()` function

### Debugging
Set `LOG_LEVEL=DEBUG` in `.env` for detailed logs.

## 🚨 Troubleshooting

### Common Issues

**Bot not responding:**
- Check `BOT_TOKEN` in `.env`
- Verify bot is running
- Check logs for errors

**Authentication failed:**
- Verify `credentials.json` is correct
- Check Google Drive API is enabled
- Ensure redirect URI is `urn:ietf:wg:oauth:2.0:oob`

**Upload fails:**
- Check internet connection
- Verify Google Drive storage space
- Try smaller files first

**File too large:**
- Current limit is 2GB
- Modify `MAX_FILE_SIZE` in `config.py`

### Logs
Check console output for detailed error messages and debugging information.

## 📊 File Size Limits

| File Type | Limit | Upload Method |
|-----------|-------|---------------|
| Small files | ≤20MB | Direct upload |
| Large files | >20MB | Chunked upload |
| Maximum | 2GB | Chunked upload |

## 🔄 Upload Queue

The bot uses a queue system to handle multiple uploads:
- Files are processed in order
- Progress tracking for each upload
- Cancel option during upload
- Error handling and retry logic

## 📈 Performance

- **Concurrent Uploads**: One per user
- **Rate Limiting**: 10 requests per minute
- **Chunk Size**: 1MB for optimal performance
- **Progress Updates**: Every 20 seconds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please use responsibly and in accordance with Google Drive Terms of Service.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Contact the bot administrator

---

**Made with ❤️ for seamless file management**
