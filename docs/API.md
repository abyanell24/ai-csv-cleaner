# API Configuration

This document explains the API keys used in the application.

## Overview

The AI CSV Cleaner uses Cerebras AI for inference. An API key is required to connect to the Cerebras API.

## Current Configuration

The application currently has a built-in API key for demonstration purposes. This key may have rate limits.

For production or heavy usage, it is recommended to use your own API key.

## Getting Your Own API Key

### Step 1: Visit Cerebras

Navigate to: https://cloud.inference.ai/

### Step 2: Sign Up

1. Click "Get Started for Free"
2. Sign up with your email (Google, GitHub, or email)
3. No credit card required for free tier

### Step 3: Get API Key

1. After signing in, go to the dashboard
2. Navigate to "API Keys" section
3. Copy your API key (starts with `csk-`)

## Updating the API Key

### Method 1: Edit the Client File

1. Open `utils/cerebras_client.py`
2. Find line with API key:
   ```python
   self.client = Cerebras(api_key="csk-your-key-here")
   ```
3. Replace with your new key

### Method 2: Environment Variable (Recommended)

Set the API key as an environment variable:

```bash
# Linux/Mac
export CEREBRAS_API_KEY="csk-your-key-here"

# Windows (Command Prompt)
set CEREBRAS_API_KEY="csk-your-key-here"

# Windows (PowerShell)
$env:CEREBRAS_API_KEY="csk-your-key-here"
```

Then update the code to use environment variable:

```python
import os
api_key = os.environ.get("CEREBRAS_API_KEY", "csk-default-key")
self.client = Cerebras(api_key=api_key)
```

## Rate Limits

### Free Tier

| Limit | Value |
|-------|-------|
| Tokens per day | ~1M tokens |
| Requests | Varies |
| Model | llama-3.1-8b |

### Paid Tier

For higher limits, visit: https://cloud.inference.ai/pricing

## Troubleshooting

### Rate Limit Exceeded

**Error**: `429 - Rate limit exceeded`

**Solution**:
1. Wait a few minutes
2. Use your own API key (see above)
3. Upgrade to paid tier

### Invalid API Key

**Error**: `401 - Invalid API key`

**Solution**:
1. Verify your API key is correct
2. Check for extra spaces or characters
3. Generate a new key from dashboard

### Network Error

**Error**: Connection failed

**Solution**:
1. Check your internet connection
2. Firewall may be blocking - try different network

---

## Alternative APIs

If you need to use a different AI provider:

### OpenAI

1. Get API key from https://platform.openai.com/
2. Modify `cerebras_client.py` to use `openai` library

### Groq

1. Get API key from https://console.groq.com/
2. Create similar client using `groq` library

---

## Support

For Cerebras-specific issues:
- Documentation: https://inference-docs.cerebras.ai/
- Support: https://cloud.inference.ai/support

---

## Security Notes

| Note | Description |
|------|-------------|
| Never commit API keys | Add to .gitignore |
| Use environment variables | Recommended for production |
| Rotate keys periodically | Good security practice |
| Limit key permissions | Use least privilege principle |