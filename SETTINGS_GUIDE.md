# ⚙️ Settings & Configuration Guide

## Overview

The poker simulator now has a **Settings Panel** where you can:
1. Configure game parameters (stack size, blinds)
2. Add LLM API keys to enable AI players
3. Customize your poker experience

---

## 🎮 Accessing Settings

### Two Ways to Open Settings:

1. **From Main Screen**: Click the "⚙️ Settings" button in the top-right corner
2. **From Game Setup**: Click "Edit ⚙️" next to "Game Settings"

---

## 💰 Game Configuration

### Starting Stack
- **Default**: $1,000
- **Range**: $100 - $100,000+
- **Tip**: Set to 100-200× the big blind for standard play

### Small Blind
- **Default**: $5
- **Range**: $1+
- **Tip**: Usually half of the big blind

### Big Blind
- **Default**: $10
- **Range**: $2+
- **Tip**: Should be 2× the small blind

### Example Configurations:

| Game Type | Stack | SB | BB | Description |
|-----------|-------|----|----|-------------|
| **Micro Stakes** | $500 | $2 | $5 | Quick games |
| **Standard** | $1,000 | $5 | $10 | Default setup |
| **High Stakes** | $5,000 | $25 | $50 | Longer games |
| **Tournament** | $10,000 | $50 | $100 | Deep stack |

---

## 🤖 LLM API Configuration

### How to Add API Keys:

1. **Open Settings** (⚙️ button)
2. **Scroll to "LLM API Keys"** section
3. **Click "👁️ Show Keys"** to reveal input fields
4. **Paste your API keys** into the respective fields
5. **Click "Save Settings"**
6. **Refresh the page** (optional, but recommended)

### Supported LLM Providers:

#### 1. **OpenAI (GPT-4)**
- **Models**: GPT-4o-mini, GPT-4o
- **Get Key**: https://platform.openai.com/api-keys
- **Format**: `sk-...`
- **Cost**: ~$0.01-0.05 per hand
- **Best For**: Strategic play

#### 2. **DeepSeek**
- **Model**: deepseek-chat
- **Get Key**: https://platform.deepseek.com/
- **Format**: `sk-...`
- **Cost**: ~$0.001 per hand (very cheap!)
- **Best For**: Budget-friendly testing

#### 3. **Anthropic (Claude)**
- **Model**: Claude 3.5 Sonnet
- **Get Key**: https://console.anthropic.com/
- **Format**: `sk-ant-...`
- **Cost**: ~$0.02-0.10 per hand
- **Best For**: Advanced reasoning

#### 4. **Google Gemini**
- **Model**: Gemini Pro
- **Get Key**: https://makersuite.google.com/app/apikey
- **Format**: `AIza...`
- **Cost**: FREE tier available!
- **Best For**: Free testing

#### 5. **xAI Grok**
- **Model**: Grok Beta
- **Get Key**: https://console.x.ai/
- **Format**: `xai-...`
- **Cost**: TBD (new service)
- **Best For**: Experimental

---

## 🔄 How It Works

### After Saving Settings:

1. **API keys are stored** in your browser's local storage
2. **Keys are sent to backend** to initialize LLM strategies
3. **AI Strategy dropdown updates** to show available LLMs
4. **You can now select LLM strategies** when creating games!

### Example:
```
Before: [Aggressive, Conservative, Random]
After:  [Aggressive, Conservative, Random, GPT-4 Mini, DeepSeek, Claude]
```

---

## 🎯 Quick Start with LLMs

### Option 1: Free Testing (Gemini)
1. Get free Gemini API key
2. Add to settings
3. Save
4. Select "💎 Gemini" as AI strategy
5. Create game!

### Option 2: Best Performance (GPT-4)
1. Get OpenAI API key (requires payment)
2. Add to settings
3. Save
4. Select "🤖 GPT-4o" as AI strategy
5. Watch it play strategic poker!

### Option 3: Budget Testing (DeepSeek)
1. Get DeepSeek API key
2. Add to settings
3. Save
4. Select "🧠 DeepSeek" as AI strategy
5. Very cheap, good quality!

---

## 🎮 Using Custom Settings in Games

### Creating a Game with Custom Settings:

1. **Configure settings** (stack, blinds, API keys)
2. **Save settings**
3. **Go to "Create New Game"**
4. **Notice**: Game Settings section shows your custom values
5. **Select AI strategy** (including LLMs if configured)
6. **Create game** - it will use your settings!

### Example Game Setup:
```
Your Name: John
Number of AI Opponents: 2
AI Strategy: 🤖 GPT-4 Mini

Game Settings:
• Starting stack: $5,000
• Small Blind: $25
• Big Blind: $50
```

---

## 🔒 Security & Privacy

### Where Are Keys Stored?
- **Browser Local Storage**: Keys saved in your browser only
- **Not in cookies**: More secure
- **Not sent to external servers**: Only to your local backend

### Best Practices:
1. ✅ Use API keys with spending limits
2. ✅ Monitor usage on provider dashboards
3. ✅ Rotate keys periodically
4. ✅ Don't share your keys
5. ❌ Never commit keys to git

### Clearing Keys:
1. Open Settings
2. Delete the key text
3. Save Settings
4. The LLM strategy will be removed

---

## 🐛 Troubleshooting

### "LLM strategies not showing up"
- ✅ Check you saved settings
- ✅ Refresh the page
- ✅ Check backend console for errors
- ✅ Verify API key format is correct

### "API call failed" during game
- ✅ Verify API key is valid
- ✅ Check you have credits/quota
- ✅ Check internet connection
- ✅ Try a different LLM provider

### Settings not persisting
- ✅ Check browser allows local storage
- ✅ Try a different browser
- ✅ Clear cache and try again

### "Invalid API key" error
- ✅ Copy key again from provider
- ✅ Check for extra spaces
- ✅ Verify key hasn't expired
- ✅ Check key has correct permissions

---

## 💡 Tips & Tricks

### Optimal Game Settings:
- **Quick games**: Stack = 50× BB
- **Standard games**: Stack = 100× BB
- **Deep stack**: Stack = 200× BB

### Testing LLMs:
1. **Start with Watch Mode** to see LLMs play
2. **Use cheap LLMs** (DeepSeek/Gemini) for testing
3. **Compare strategies** by creating multiple games
4. **Monitor costs** on provider dashboards

### Best Strategy Combinations:
- **Human vs GPT-4**: Challenge yourself!
- **GPT-4 vs Claude**: Battle of the titans
- **DeepSeek vs Conservative**: Budget vs basic
- **All Random**: Chaos mode!

---

## 📊 Comparing LLM Performance

### Watch Mode Experiment:
1. Enable Watch Mode
2. Set 3+ AI players
3. Mix LLM strategies (GPT-4, Claude, DeepSeek)
4. Watch them compete!
5. See which LLM plays better poker

### Metrics to Track:
- Win rate
- Final stack size
- Aggression level
- Bluffing frequency
- Decision quality

---

## 🎉 Have Fun!

Now you can:
- ✅ Customize game parameters
- ✅ Add LLM API keys
- ✅ Play against AI that actually thinks
- ✅ Watch LLMs battle each other
- ✅ Experiment with different settings

**Enjoy your poker games!** 🎰🤖

---

## 📝 Quick Reference

### Settings Button Locations:
1. Top-right corner of main screen
2. "Edit ⚙️" in game setup panel

### Required Fields:
- **For playing**: Name (unless Watch Mode)
- **For LLMs**: At least one API key

### Optional Fields:
- All game settings have defaults
- API keys are optional (basic AIs work without them)

**Everything is saved automatically in your browser!**

