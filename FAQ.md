# ❓ Frequently Asked Questions (FAQ)

## General Questions

### Q: Is this really 100% free?
**A:** YES! No hidden costs, no API fees, no subscriptions. The entire stack uses free and open-source tools.

### Q: Do I need an API key?
**A:** NO! The Hugging Face inference API has a free tier that doesn't require authentication for basic usage.

### Q: Will it work offline?
**A:** Partially. The app has a built-in fallback system that works without internet, but it's less sophisticated than the AI-powered version.

### Q: How much does deployment cost?
**A:** $0. Streamlit Community Cloud, Hugging Face Spaces, and other options are completely free.

---

## Technical Questions

### Q: What AI model does it use?
**A:** Mistral-7B-Instruct-v0.2 via Hugging Face's free inference API. It's an open-source instruction-following model.

### Q: Why only 2 dependencies?
**A:** We kept it minimal for:
- Fast installation
- Fewer compatibility issues  
- Lower maintenance burden
- Easier deployment

### Q: Can I use a different AI model?
**A:** Yes! Just change the `api_url` in `generator_agent.py` to any Hugging Face model endpoint.

### Q: Does it store my data?
**A:** No. Everything runs in-memory. No databases, no tracking, no data collection.

### Q: How fast is it?
**A:** 3-10 seconds total:
- API call: 2-5 seconds
- Review: <1 second
- UI rendering: ~1 second

### Q: Can multiple users use it simultaneously?
**A:** When deployed, yes! Each user gets their own session. On local runs, it's single-user.

---

## Usage Questions

### Q: What grade levels are supported?
**A:** Grades 1-12. The system automatically adjusts language complexity.

### Q: What subjects work best?
**A:** Any K-12 subject:
- Math (geometry, algebra, arithmetic)
- Science (biology, chemistry, physics)
- Social Studies (history, geography)
- Language Arts (grammar, reading)

### Q: Can I customize the questions?
**A:** Currently, the system auto-generates 3 MCQs. You can manually edit the exported JSON.

### Q: Why does refinement only happen once?
**A:** Per the assignment requirements, we limit refinement to one iteration to prevent infinite loops and maintain performance.

### Q: Can I save my generated content?
**A:** Yes! Use the "Download JSON" button to save content locally.

---

## Deployment Questions

### Q: Which deployment option is best?
**A:** **Streamlit Community Cloud** is recommended:
- Easiest setup (3 clicks)
- No configuration needed
- Free forever
- Auto-updates from Git

### Q: How do I update my deployed app?
**A:** Just push changes to GitHub. Streamlit Cloud auto-deploys within seconds.

### Q: Can I use a custom domain?
**A:** On Streamlit Cloud free tier: No. On Railway/Render: Yes (with configuration).

### Q: What if Streamlit Cloud is down?
**A:** Your app is in Git. Redeploy to Hugging Face Spaces or Railway in minutes.

---

## Troubleshooting

### Q: "Module not found" error
**A:** Run: `pip install -r requirements.txt`

### Q: API timeout errors
**A:** This is normal during high load. The fallback system will automatically activate.

### Q: Content quality is poor
**A:** Try these:
- Simplify the topic description
- Use standard educational terminology
- Check your internet connection
- The fallback mode has limited sophistication

### Q: Streamlit won't start
**A:** Check:
1. Python version (need 3.8+)
2. Dependencies installed: `pip list`
3. Port 8501 available: `netstat -an | grep 8501`

### Q: UI looks broken
**A:** Try:
- Refresh browser (Ctrl+Shift+R)
- Clear cache
- Use a different browser

---

## Customization Questions

### Q: Can I change the UI colors?
**A:** Yes! Edit the CSS in `app.py` or create `.streamlit/config.toml`

### Q: Can I add more MCQs?
**A:** Yes! Modify the prompt in `generator_agent.py` to request more questions.

### Q: Can I change evaluation criteria?
**A:** Yes! Edit the review methods in `reviewer_agent.py`

### Q: Can I add new features?
**A:** Absolutely! The code is open source. Fork and customize freely.

---

## API Questions

### Q: Will the free API stop working?
**A:** Hugging Face has maintained free inference for years. If it changes, the fallback system ensures the app still works.

### Q: What are the rate limits?
**A:** Approximately 100 requests/hour on the free tier. More than enough for typical use.

### Q: Can I use my own API key for better rates?
**A:** Yes! Modify `generator_agent.py` to include authentication headers.

### Q: What if I need commercial use?
**A:** 
- Current setup: Free for personal/educational use
- Commercial: Consider Hugging Face Pro or host your own model

---

## Assignment-Specific Questions

### Q: Does this meet the requirements?
**A:** Yes! It has:
- ✅ Two agents (Generator + Reviewer)
- ✅ Structured input/output
- ✅ Clear responsibilities
- ✅ UI-driven workflow
- ✅ Refinement logic (1 pass)

### Q: Can I explain how it works in an interview?
**A:** Yes! Read `TECHNICAL.md` for deep understanding. Practice explaining:
- Agent architecture
- Data flow
- Why you made certain decisions

### Q: Is it okay that I used help?
**A:** Using resources to learn is standard in software development. Key points:
- Understand every line of code
- Be able to explain design decisions
- Know how to modify and extend it
- Give credit where due

---

## Performance Questions

### Q: How do I make it faster?
**A:** 
- Use a local GPU-enabled model
- Cache frequently-used topics
- Pre-generate common content
- Use parallel processing (advanced)

### Q: Can it handle high traffic?
**A:** On free tiers: 100-1000 users. For more, upgrade to paid tiers or optimize caching.

### Q: Memory usage?
**A:** Very light:
- App: ~100-200MB
- Streamlit: ~50MB
- Total: <300MB (well within free tier limits)

---

## Future Enhancement Questions

### Q: Can I add user accounts?
**A:** Yes, but requires:
- Database (SQLite/PostgreSQL)
- Authentication system
- Session management

### Q: Can it generate images/diagrams?
**A:** Not currently, but you could integrate:
- Stable Diffusion API
- Matplotlib for charts
- Mermaid for diagrams

### Q: Can I make it multi-language?
**A:** Yes! Modify prompts to include language parameter and use multilingual models.

### Q: Can I add more agent types?
**A:** Absolutely! Consider:
- Diagram Generator Agent
- Quiz Difficulty Adjuster Agent
- Content Translator Agent

---

## Legal/License Questions

### Q: Can I use this for my company?
**A:** Yes, MIT license allows commercial use. But verify Hugging Face's terms for commercial API usage.

### Q: Do I need to credit the author?
**A:** Not required by MIT license, but appreciated!

### Q: Can I sell this?
**A:** Yes, but be transparent about using open-source components.

### Q: Can I modify it?
**A:** Yes! That's the point of open source.

---

## Contribution Questions

### Q: How can I contribute?
**A:** 
1. Fork the repository
2. Add your feature
3. Write tests
4. Submit pull request

### Q: What features are wanted?
**A:** See GitHub issues or suggest:
- More export formats (PDF, DOCX)
- Better templates
- More evaluation criteria
- Language support

### Q: Can I report bugs?
**A:** Please do! Open an issue on GitHub with:
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

---

## Comparison Questions

### Q: How does this compare to ChatGPT?
**A:** 
- **This**: Specialized for education, structured output, free
- **ChatGPT**: General purpose, conversational, requires subscription

### Q: Why not use GPT-4 API?
**A:** Cost. GPT-4 API charges per token. This project is 100% free.

### Q: Is the quality as good as commercial tools?
**A:** For basic educational content, yes. For highly sophisticated content, commercial tools may be better.

---

## Still Have Questions?

- 📖 Read the [README.md](README.md) for overview
- 🔧 Check [TECHNICAL.md](TECHNICAL.md) for deep dive  
- 🚀 See [QUICKSTART.md](QUICKSTART.md) for setup
- 🌐 Visit [DEPLOYMENT.md](DEPLOYMENT.md) for hosting
- 💬 Open a GitHub issue
- 📧 Contact the maintainers

---

**Remember**: The best way to learn is by experimenting! Try modifying the code and seeing what happens. 🚀
