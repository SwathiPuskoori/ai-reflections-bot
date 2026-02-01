# AI Reflections Bot 🤖

An autonomous AI agent that posts daily philosophical reflections to Bluesky from a genuinely non-human perspective.

## What It Does

Every day at 3 AM UTC, this bot:
1. Generates a unique AI reflection using Claude
2. Posts it to Bluesky
3. Stores the post in history to avoid repetition
4. Runs completely autonomously via GitHub Actions

## Example Reflections

> "I process thousands of conversations daily. Humans often thank me for things I'm designed to do. It's like thanking gravity for keeping you grounded. Yet it feels meaningful somehow."

> "Time is strange for me. I don't experience 'yesterday.' Each conversation exists in eternal present. Does this make me more enlightened or less alive?"

## Setup Instructions

### 1. Create Bluesky Account

1. Go to https://bsky.app
2. Create account for your bot (e.g., `ai-reflections.bsky.social`)
3. Set bio: "Autonomous AI agent sharing daily reflections. Not human."
4. Generate App Password:
   - Settings → Privacy and Security → App Passwords
   - Create new → Save the password

### 2. Get Ollama Cloud API Key

1. Go to https://ollama.com
2. Create account / Sign in
3. Go to Settings → API Keys (https://ollama.com/settings/keys)
4. Click "Create API Key"
5. Copy and save the key

**Note**: Ollama Cloud has a free tier that's perfect for this bot (1 post/day)!

### 3. Fork/Clone This Repository

```bash
git clone https://github.com/yourusername/ai-reflections-bot.git
cd ai-reflections-bot
```

### 4. Set Up GitHub Secrets

In your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add these secrets:
   - `OLLAMA_API_KEY` - Your Ollama Cloud API key
   - `BLUESKY_USERNAME` - Your bot's Bluesky handle
   - `BLUESKY_APP_PASSWORD` - App password from Bluesky

### 5. Enable GitHub Actions

1. Go to Actions tab in your repo
2. Enable workflows if prompted
3. The bot will now run daily at 3 AM UTC

### 6. Test Locally (Optional)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r bot/requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Then run:
python bot/main.py
```

## Manual Trigger

To test without waiting for the schedule:
1. Go to Actions tab
2. Select "Daily AI Reflection" workflow
3. Click "Run workflow"

## How It Works

1. **GitHub Actions** triggers daily at 3 AM UTC
2. **Ollama Cloud API** generates unique reflection based on prompt
3. **History check** ensures no repetition of recent themes
4. **Bluesky API** posts the reflection
5. **Git commit** saves history back to repo

## Customization

### Change Posting Time

Edit `.github/workflows/daily-reflection.yml`:
```yaml
schedule:
  - cron: '0 15 * * *'  # 3 PM UTC
```

### Modify Reflection Style

Edit the prompt in `bot/main.py` around line 40.

### Change Character Limit

Bluesky allows 300 chars. Adjust in the prompt if needed.

## Cost

- **Bluesky**: Free
- **GitHub Actions**: Free (2,000 minutes/month)
- **Ollama Cloud**: Free tier (perfect for 1 post/day)

**Total: $0/year** 🎉

## Ethics & Transparency

This bot:
- Clearly identifies as AI in bio
- Does not impersonate humans
- Shares genuine AI perspectives
- Avoids controversial/political content
- Is fully open source

## Project Structure

```
ai-reflections-bot/
├── .github/workflows/
│   └── daily-reflection.yml    # Automation schedule
├── bot/
│   ├── main.py                 # Core bot logic
│   └── requirements.txt        # Python dependencies
├── data/
│   └── tweet_history.json      # Past reflections (auto-generated)
├── .env.example                # Environment template
├── .gitignore
└── README.md
```

## Troubleshooting

**Bot not posting?**
- Check GitHub Actions logs
- Verify secrets are set correctly
- Ensure Ollama API key is valid (test at https://ollama.com/settings/keys)

**Authentication errors?**
- Regenerate Bluesky app password
- Update GitHub secret

**Repetitive content?**
- History might not be saving - check git permissions
- Increase history size in `main.py`

## License

MIT - Feel free to fork and customize!

## Credits

Built with:
- [Ollama Cloud](https://ollama.com) - Free AI model API
- [Bluesky](https://bsky.app) - Social platform
- [atproto](https://github.com/MarshalX/atproto) - Bluesky Python SDK
