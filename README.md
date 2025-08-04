# 🎥 Multi-Platform Video Downloader Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue.svg)](https://core.telegram.org/bots/api)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful Telegram bot that downloads videos from **Instagram**, **YouTube**, and **TikTok** with smart caching, admin panel, and queue management. Built with modern async Python using Aiogram and Telethon.

## ✨ Features

### 🎯 Multi-Platform Support
- **Instagram**: Reels, Posts, IGTV, Stories, Carousel posts
- **YouTube**: Videos, Shorts with quality selection (360p/480p/720p/MP3)
- **TikTok**: Videos and Reels

### 🚀 Advanced Features
- ✅ **Smart Caching System** - No duplicate downloads
- ✅ **Format Selection** - Choose quality for YouTube videos
- ✅ **Queue Management** - Process requests efficiently
- ✅ **Admin Panel** - Statistics, user management, broadcasting
- ✅ **Mandatory Subscriptions** - Channel subscription enforcement
- ✅ **Comprehensive Logging** - Detailed error tracking and monitoring
- ✅ **Rate Limiting Protection** - Avoid API restrictions
- ✅ **Session Management** - Secure authentication handling

## 🏗️ Architecture

The system uses a **modular architecture** with three main components:

1. **🤖 Telegram Bot (Aiogram)** - Handles user interactions and serves cached content
2. **👤 Userbot (Telethon)** - Downloads videos from source platforms
3. **💾 SQLite Database** - Manages caching, users, and statistics

## 📁 Project Structure

```
downloader/
├── bot/
│   ├── handlers.py         # Message handlers and callbacks
│   ├── main.py            # Bot application core
│   └── middleware.py      # Custom middleware
├── userbot/
│   └── client.py          # Telethon userbot client
├── db/
│   └── database.py        # SQLite database operations
├── logs/                  # Application logs (auto-created)
├── config.py              # Configuration management
├── utils.py               # URL validation utilities
├── setup.py               # Initial setup script
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🚀 Installation

### 1. Clone or Download

Download all files to your desired directory.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

1. Copy `.env` file and fill in your credentials:

```env
# Telegram API credentials (get from https://my.telegram.org/apps)
API_ID=your_api_id
API_HASH=your_api_hash

# Bot token from @BotFather
BOT_TOKEN=your_bot_token

# Private channel ID where videos will be stored
STORAGE_CHANNEL_ID=-1001234567890

# Session name for Telethon userbot
SESSION_NAME=userbot_session

# Database path
DATABASE_PATH=./db/videos.db

# Logging level
LOG_LEVEL=INFO
```

### 4. Required Setup Steps

#### Get Telegram API Credentials
1. Go to https://my.telegram.org/apps
2. Log in with your phone number
3. Create a new application
4. Copy `API_ID` and `API_HASH`

#### Create a Bot
1. Message @BotFather on Telegram
2. Use `/newbot` command
3. Follow instructions to create a bot
4. Copy the bot token

#### Create Storage Channel
1. Create a private channel in Telegram
2. Add your bot as an administrator
3. Get the channel ID (you can use @userinfobot)
4. The ID should be negative (e.g., -1001234567890)

### 5. Run Setup

```bash
python setup.py
```

This will:
- Validate your configuration
- Authenticate your userbot account (one-time)
- Test all connections
- Create necessary session files

## 🎯 Usage

### Start the Bot

```bash
python main.py
```

### Send Instagram URLs

1. Start a chat with your bot
2. Send any Instagram Reels/Video URL
3. The bot will:
   - Check if the video is already cached
   - If cached: instantly send the video
   - If not cached: download via userbot and cache it

### Supported URL Formats

- `https://instagram.com/p/ABC123/`
- `https://instagram.com/reel/XYZ789/`
- `https://www.instagram.com/p/ABC123/`
- `https://www.instagram.com/reel/XYZ789/`

## 🔧 Advanced Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_ID` | Telegram API ID | Required |
| `API_HASH` | Telegram API Hash | Required |
| `BOT_TOKEN` | Bot token from @BotFather | Required |
| `STORAGE_CHANNEL_ID` | Private channel ID for storage | Required |
| `SESSION_NAME` | Userbot session filename | `userbot_session` |
| `DATABASE_PATH` | SQLite database path | `./db/videos.db` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |

### Logging

Logs are written to:
- Console (formatted output)
- `logs/bot.log` (rotating log file, 10MB max, 7 days retention)

### Database Management

The SQLite database automatically:
- Creates tables on first run
- Handles URL normalization
- Prevents duplicate entries
- Can be cleaned up with `cleanup_old_records()` method

## 🛠️ Troubleshooting

### Common Issues

**"User is not authorized"**
- Run `python setup.py` again
- Make sure you completed the authentication process

**"Cannot access storage channel"**
- Verify the channel ID is correct (negative number)
- Ensure the bot is added as administrator to the channel
- Check that the userbot account has access to the channel

**"@instagrambot access failed"**
- The userbot account might be restricted
- Try starting a conversation with @instagrambot manually
- Wait some time if you hit rate limits

**"Rate limited" errors**
- The system respects Telegram rate limits
- Wait for the specified time before retrying
- Consider reducing request frequency

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in `.env`:

```env
LOG_LEVEL=DEBUG
```

### Manual Database Cleanup

```python
from db.database import Database
import asyncio

async def cleanup():
    db = Database('./db/videos.db')
    await db.cleanup_old_records(days=30)  # Remove records older than 30 days

asyncio.run(cleanup())
```

## 📊 Performance

- **Response Time**: 
  - Cached videos: ~1-2 seconds
  - New videos: ~30-60 seconds (depends on @instagrambot)
- **Storage**: Videos are stored in Telegram (unlimited cloud storage)
- **Database**: Lightweight SQLite with minimal storage footprint

## 🔒 Security Notes

- Session files contain authentication data - keep them secure
- The userbot uses your personal Telegram account
- Only use with trusted Instagram content
- Consider running on a dedicated server for 24/7 operation

## 📈 Monitoring

The system provides comprehensive logging for:
- Request processing times
- Error rates and types
- Database operations
- Userbot activities
- Rate limiting events

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Respect Instagram's Terms of Service and rate limits.

## 💡 Tips

1. **First Run**: Always run `setup.py` before starting the bot
2. **Storage**: Keep the storage channel private and secure
3. **Monitoring**: Check logs regularly for any issues
4. **Updates**: Keep dependencies updated for security
5. **Backup**: Consider backing up the session files and database

## 🚨 Important Notes

- This bot uses your personal Telegram account (userbot)
- Respect rate limits to avoid account restrictions
- Use responsibly and in accordance with Telegram's ToS
- The system is designed to minimize @instagrambot usage through caching

---

**Need help?** Check the logs in `logs/bot.log` for detailed error information.
