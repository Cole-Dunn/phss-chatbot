# 🚀 RAG Chatbot Setup Guide

This guide will walk you through setting up your chatbot step-by-step. Don't worry - I'll explain everything in simple terms!

## What You'll Need

1. **OpenAI Account** (for the AI brain)
2. **Pinecone Account** (for storing your knowledge base)
3. **Python** installed on your computer
4. **A Wix Studio website** (where you'll add the chatbot)

---

## Step 1: Get Your API Keys

### OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to "API Keys" in your account
4. Click "Create new secret key"
5. Copy the key (starts with `sk-...`)

### Pinecone API Key
1. Go to [app.pinecone.io](https://app.pinecone.io)
2. Sign up for free account
3. Go to "API Keys" section
4. Copy your API key and environment name

---

## Step 2: Set Up Your Environment

### Install Python Requirements
Open Terminal (Mac) or Command Prompt (Windows) and run:

```bash
# Navigate to your project folder
cd chatbot-project

# Install required packages
pip install -r requirements.txt
```

### Set Up Your API Keys
1. Copy the file `.env.example` to `.env`
2. Open the `.env` file
3. Replace the placeholder text with your real API keys:

```
OPENAI_API_KEY=sk-your-actual-openai-key-here
PINECONE_API_KEY=your-actual-pinecone-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment-here
CHATBOT_NAME=Your Bot Name
CHATBOT_COMPANY=Your Company Name
```

**IMPORTANT**: Never share your `.env` file - it contains secret keys!

---

## Step 3: Customize Your Knowledge Base

### Add Your Content
1. Open the `backend/knowledge_base/` folder
2. Edit the existing files or add new `.txt` files
3. Replace the sample content with information about your client's business:
   - FAQ questions and answers
   - Product information
   - Company policies
   - Contact information

### Example Knowledge Base File Format:
```
SECTION TITLE

Question or topic here?
Detailed answer with all relevant information. Be comprehensive but clear.

Another Question?
Another detailed answer. Each section is separated by double line breaks.
```

---

## Step 4: Load Your Knowledge Base

Run this command to load your content into the vector database:

```bash
# Navigate to backend folder
cd backend

# Load your knowledge base
python load_knowledge_base.py
```

You should see: "✅ Knowledge base loaded successfully!"

---

## Step 5: Start Your Chatbot Backend

In the backend folder, run:

```bash
# Start the API server
python main.py
```

You should see: "RAG Chatbot API is running!"

Keep this terminal window open while testing your chatbot.

---

## Step 6: Test Your Chatbot

1. Open `frontend/chatbot.html` in your web browser
2. Click the chat bubble in the bottom right
3. Ask a question about your content
4. The chatbot should respond with relevant information!

---

## Step 7: Add to Your Wix Studio Site

### Method 1: Embed Code (Recommended)
1. In Wix Studio, go to your site editor
2. Click the "+" icon to add an element
3. Select "Embed Code" > "Marketing Tools" > "Custom Code"
4. Paste this code:

```html
<!-- Copy the contents of chatbot.html, chatbot.css, and chatbot.js -->
<!-- Or use the simplified embed version below -->

<div id="chatbot-embed"></div>
<script>
// Load chatbot files
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://your-domain.com/chatbot.css';
document.head.appendChild(link);

const script = document.createElement('script');
script.src = 'https://your-domain.com/chatbot.js';
document.head.appendChild(script);
</script>
```

### Method 2: Upload Files to Wix
1. Upload `chatbot.html`, `chatbot.css`, and `chatbot.js` to your Wix media library
2. Embed the HTML file as an iframe

---

## Step 8: Deploy Your Backend (Production)

For production use, you'll need to deploy your backend API to a service like:
- **Heroku** (easiest for beginners)
- **Railway**
- **Render**
- **DigitalOcean**

Update the `apiUrl` in `chatbot.js` to point to your deployed backend URL.

---

## 🎉 You're Done!

Your RAG chatbot is now ready! Here's what it can do:

✅ **Answer questions** based on your knowledge base  
✅ **Search semantically** (understands meaning, not just keywords)  
✅ **Maintain conversation** context  
✅ **Integrate seamlessly** with Wix Studio  
✅ **Handle multiple users** simultaneously  

---

## Troubleshooting

### Common Issues:

**"API key not found"**
- Make sure your `.env` file has the correct API keys
- Check that the file is named `.env` (not `.env.txt`)

**"Connection error"**  
- Make sure your backend server is running
- Check that the API URL in `chatbot.js` is correct

**"No response from chatbot"**
- Verify your knowledge base loaded successfully
- Check the browser console for error messages

**Need Help?**
- Check the console logs in your browser (F12 → Console)
- Make sure all files are in the correct locations
- Verify your API keys are valid and have credits

---

## Next Steps

Once everything works:

1. **Customize the design** - Edit `chatbot.css` to match your brand
2. **Add more content** - Expand your knowledge base files
3. **Monitor usage** - Check OpenAI and Pinecone usage dashboards
4. **Improve responses** - Refine your knowledge base based on user questions

Happy chatbot building! 🤖