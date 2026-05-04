# 🔍 AI Research Agent

An autonomous AI agent that searches the web and generates structured research reports on any topic — in seconds.

## 🤖 What It Does

You type a topic. The agent searches the internet, reads through real sources, and writes a clean research report. No copy-pasting. No tab-switching. Just results.

## ✨ Features

- 🔍 Searches the real web using Tavily
- 🧠 Reads and understands articles using LLaMA 4 on Groq
- 📝 Generates structured reports (Introduction → Key Findings → Trends → Conclusion)
- ⏳ Shows live progress while searching
- 📏 Short / Medium / Detailed length control
- 📎 Displays all sources used
- 📄 Download report as PDF

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| LangChain | Agent orchestration |
| Tavily | Real-time web search |
| Groq (LLaMA 4 Scout) | Fast LLM inference |
| Streamlit | Interactive UI |
| Streamlit Cloud | Free deployment |

## 🚀 Live Demo

👉 [ai-research-agent-jk.streamlit.app](https://ai-research-agent-jk.streamlit.app/)

## ⚙️ Run Locally

1. Clone the repo
```bash
git clone https://github.com/yourusername/ai-research-agent.git
cd ai-research-agent
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Add your API keys — create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
```

4. Run the app
```bash
streamlit run app.py
```

## 🔑 API Keys

| Service | Get it here |
|---|---|
| Groq | [console.groq.com](https://console.groq.com) |
| Tavily | [app.tavily.com](https://app.tavily.com) |

Both are free! No credit card needed.

## 📌 Coming Soon

- 💬 Chat with the report
- ⚖️ Compare two topics
- 🤖 Multi-agent architecture

## 🙋‍♂️ Author

Built by **Khasim Khaleel Basha**  
[LinkedIn](https://linkedin.com/in/yourprofile) • [GitHub](https://github.com/yourusername)
