# 📚 Educational Content Generator - Multi-Agent AI System

An intelligent, AI-powered system that automatically generates grade-appropriate educational content using a **multi-agent architecture**. The system employs two specialized agents (Generator and Reviewer) that work together to create high-quality, age-appropriate educational materials.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Free](https://img.shields.io/badge/Cost-100%25%20Free-success.svg)

## 🎯 Project Overview

This project demonstrates a **production-ready multi-agent system** that:
- ✅ Generates educational explanations and multiple-choice questions
- ✅ Automatically reviews content for age-appropriateness and quality
- ✅ Refines content based on feedback in a single iteration
- ✅ Works **100% FREE** with no API costs or hidden charges

### 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                        │
│            (User Input → Display Results)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐           ┌────────▼────────┐
│   Generator    │           │    Reviewer     │
│     Agent      │──────────▶│     Agent       │
│                │           │                 │
│ • Creates      │           │ • Evaluates     │
│   content      │           │   quality       │
│ • Structured   │           │ • Checks age-   │
│   output       │           │   appropriate   │
│ • Uses HF API  │           │ • Provides      │
│   (free)       │           │   feedback      │
└────────────────┘           └─────────────────┘
        │                             │
        └──────────┬──────────────────┘
                   │
           ┌───────▼────────┐
           │  Refinement    │
           │  Loop (1 pass) │
           └────────────────┘
```

## 🚀 Features

### 🤖 Dual-Agent System

**1. Generator Agent**
- Generates grade-specific educational content
- Creates clear explanations adapted to student age
- Produces 3 multiple-choice questions per topic
- Uses Hugging Face's free inference API
- Fallback to template-based generation if API is unavailable

**2. Reviewer Agent**
- Evaluates content for age-appropriateness
- Checks sentence complexity and vocabulary level
- Validates MCQ quality and correctness
- Provides structured, actionable feedback
- Pass/Fail decision based on quality criteria

### 🔄 Intelligent Refinement

- Automatic content improvement if review fails
- Feedback-driven regeneration
- Single refinement iteration (as per requirements)
- Ensures high-quality output

### 🌟 Advanced Features (Production-Ready)

**📊 Real-Time Analytics**
- Track generation performance
- Monitor pass rates and timing
- View historical trends
- Grade distribution analysis
- Performance improvement tracking

**🎯 Advanced Validation System**
- Flesch-Kincaid reading level analysis
- Content structure validation
- MCQ quality assessment
- Topic appropriateness checking
- 15+ automated quality checks

**💾 Multi-Format Export**
- JSON (machine-readable)
- Plain Text (formatted documents)
- Markdown (GitHub-ready)
- Study Guide (student-optimized)
- Teacher Version (with answer keys)

**📈 Performance Monitoring**
- Session analytics logging
- Time tracking (generation, review, total)
- Quality metrics dashboard
- Success rate visualization

### 💡 Additional Features

- 📊 **Interactive UI**: Clean, modern Streamlit interface
- 📥 **Export Options**: Download in 5 different formats
- 🎨 **Visual Feedback**: Color-coded status indicators
- 📈 **Progress Tracking**: Real-time pipeline status
- 🆓 **Zero Cost**: No API keys, no subscriptions, completely free

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/educational-content-generator.git
cd educational-content-generator
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! Only 2 dependencies needed.

## 🎮 Usage

### Running Locally

1. Navigate to the project directory:
```bash
cd educational-content-generator
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser and go to: `http://localhost:8501`

### Using the Application

1. **Select Grade Level** (1-12)
2. **Enter Topic** (e.g., "Types of angles", "Photosynthesis", "Fractions")
3. **Click "Generate Educational Content"**
4. **View Results** in three tabs:
   - 🤖 Initial Generation
   - 🔍 Review & Feedback
   - 🔄 Refinement (if needed)

### Example Input

```json
{
  "grade": 4,
  "topic": "Types of angles"
}
```

### Example Output

**Generated Content:**
```json
{
  "explanation": "Angles are everywhere around us! When two lines meet...",
  "mcqs": [
    {
      "question": "What does a right angle look like?",
      "options": ["A) Like the corner of a book", "B) Like a full circle", ...],
      "answer": "A"
    }
  ]
}
```

**Review Result:**
```json
{
  "status": "pass",
  "feedback": ["Content looks good!"]
}
```

## 🛠️ Project Structure

```
educational-content-generator/
│
├── agents/
│   ├── generator_agent.py      # Generator Agent implementation
│   └── reviewer_agent.py       # Reviewer Agent implementation
│
├── utils/
│   ├── analytics.py            # Performance tracking & analytics
│   ├── export.py               # Multi-format document export
│   └── validator.py            # Advanced content validation
│
├── app.py                       # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 🔧 Technical Details

### Generator Agent

**Input Structure:**
```python
{
    "grade": int,      # 1-12
    "topic": str       # Educational topic
}
```

**Output Structure:**
```python
{
    "explanation": str,           # Age-appropriate explanation
    "mcqs": [
        {
            "question": str,      # Question text
            "options": [str],     # 4 options (A, B, C, D)
            "answer": str         # Correct answer (A/B/C/D)
        }
    ]
}
```

### Reviewer Agent

**Evaluation Criteria:**
- ✅ Age-appropriate vocabulary
- ✅ Sentence complexity matching grade level
- ✅ Conceptual correctness
- ✅ Clear and engaging explanations
- ✅ Valid MCQ structure
- ✅ Relevant questions testing understanding

**Output Structure:**
```python
{
    "status": "pass" | "fail",
    "feedback": [str]              # List of improvement suggestions
}
```

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (FREE)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

**Benefits:**
- ✅ Completely free
- ✅ Automatic HTTPS
- ✅ Easy updates via Git
- ✅ No server management

### Option 2: Local Deployment

Perfect for:
- Testing and development
- Running on your own machine
- No internet required (uses fallback mode)

```bash
streamlit run app.py
```

### Option 3: Hugging Face Spaces (FREE)

1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Space with Streamlit
3. Upload your files
4. App goes live automatically!

## 🆓 Cost Breakdown

| Component | Cost |
|-----------|------|
| Hugging Face API (free tier) | $0 |
| Streamlit | $0 |
| Python | $0 |
| Deployment (Streamlit Cloud) | $0 |
| **TOTAL** | **$0** |

**No hidden charges. No credit card required. No API keys needed.**

## 🎓 Educational Use Cases

- 📖 **Teachers**: Generate lesson materials quickly
- 👨‍🏫 **Tutors**: Create practice questions for students
- 👨‍👩‍👧‍👦 **Parents**: Help with homework and study materials
- 🏫 **Schools**: Supplement curriculum with custom content
- 📚 **EdTech**: Integrate into learning platforms

## 🔒 Privacy & Safety

- ✅ No data collection
- ✅ Runs locally or on trusted platforms
- ✅ No user tracking
- ✅ Open source code (audit yourself!)

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Known Limitations

1. **API Rate Limits**: Hugging Face free tier has rate limits. Fallback mode activates if exceeded.
2. **Model Performance**: Free models may occasionally produce less optimal content.
3. **Single Refinement**: System performs only one refinement iteration (as per requirements).

## 💡 Future Enhancements

- [ ] Support for more subjects and topics
- [ ] Multi-language content generation
- [ ] Image/diagram generation
- [ ] Export to PDF/Word formats
- [ ] Batch content generation
- [ ] Custom evaluation criteria

## 📧 Support

For questions or issues:
- 🐛 Open an issue on GitHub
- 💬 Start a discussion in the repository
- 📧 Contact: [suvroneelnatha213@gmail.com]

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co) for free AI model access
- [Streamlit](https://streamlit.io) for the amazing framework
- [Python](https://python.org) community for excellent libraries

## ⭐ Show Your Support

If this project helped you, please give it a ⭐ on GitHub!

---

**Built with ❤️ for educators and students worldwide**

**100% Free | 100% Open Source | 100% Awesome**
