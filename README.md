# 🎓 AI Study Companion

An AI-powered study assistant that analyzes your PDF lecture notes, summarizes them, generates quizzes, flashcards, and helps you study smarter.

🔗 **Live Demo:** https://ai-study-companion-gkw6l42jybe8qx4jnjyr2a.streamlit.app/

---

## ✨ Features

- 📝 **Smart Summarization** — 6 different modes (normal, friend-style, technical, quick, exam mode, last-night mode)
- ❓ **Quiz Generation** — Auto-generated multiple choice questions with instant feedback
- 🃏 **Flashcards** — Interactive flashcards with flip animation
- 💬 **Chat with PDF** — Ask anything about your document
- 🧠 **Smart Analysis:**
  - Difficulty analysis
  - Key concept extraction
  - Formula extractor
  - Concept map
  - Exam question prediction
  - Motivation coach

---

## 🛠️ Technologies Used

- **Python** — Core language
- **Streamlit** — Web interface
- **Groq API** — AI model (LLaMA 3.3 70B)
- **PyMuPDF** — PDF text extraction
- **python-dotenv** — Secure API key management

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/aysegulmuhtac/ai-study-companion.git
cd ai-study-companion

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_api_key_here > .env

# Run the app
streamlit run app.py
```

---

## ⚠️ Known Limitations

- This project uses the **Groq API** free tier, which has a daily token limit of 100,000 tokens. Heavy usage may temporarily limit responses.
- PDF files with complex formatting or scanned images may not extract text perfectly.
- Concept map works best with structured academic content.

---

## 📸 Screenshots

*Coming soon*

---

## 👩‍💻 Author

**Ayşegül Muhtaç** — [GitHub](https://github.com/aysegulmuhtac)

---

*Built with ❤️ using Groq & Streamlit*