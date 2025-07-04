
![Uploading Screenshot 2025-07-04 at 11.27.05 PM.png…]()

# GenAI Q&A Assistant

A GenAI-powered assistant that reads user-uploaded documents and can:
- Answer questions that require comprehension and inference
- Pose logic-based questions to users and evaluate their responses
- Justify every answer with a reference from the document

---

## Features

- **Document Upload:** Supports PDF and TXT files (e.g., research papers, reports).
- **Ask Anything:** Users can ask free-form questions about the document; the assistant answers with contextual understanding and cites the source.
- **Challenge Me:** The system generates three logic-based or comprehension-focused questions from the document, evaluates user answers, and provides feedback with justification.
- **Auto Summary:** Provides a concise summary (≤ 150 words) of the uploaded document.
- **Web Interface:** Clean, intuitive interface built with Streamlit.
- **Backend:** FastAPI-based API for document processing, Q&A, and logic question generation.
- **LLM Integration:** Uses Groq’s Llama-3.3-70b-versatile model via LangChain for all reasoning tasks.
- **Rate Limiting:** Enforces 29 requests per minute and 999 requests per day to avoid API overuse.

---

## Architecture

```
+-------------------+         +-------------------+         +-------------------+
|                   |         |                   |         |                   |
|   Streamlit UI    +-------->+   FastAPI Backend +-------->+   Groq LLM (via   |
|                   |  HTTP   |                   |  LLM    |   LangChain)      |
+-------------------+         +-------------------+         +-------------------+
        |                            |                                 |
        |  File Upload, Q&A,         |  Document Processing,           |  Model Inference
        |  Challenge Me, Summary     |  Q&A, Challenge, Evaluation     |
        +----------------------------+---------------------------------+
```

### Reasoning Flow

1. **Document Upload**
   - User uploads a PDF/TXT file via the Streamlit UI.
   - The file is sent to the FastAPI backend, which extracts and stores the text.

2. **Auto Summary**
   - The backend uses the LLM to generate a concise summary of the document.

3. **Ask Anything**
   - User submits a question.
   - The backend prompts the LLM with the document and question, instructing it to answer using only the document and to cite the relevant paragraph or section.
   - The LLM’s response is parsed and both the answer and justification are shown to the user.

4. **Challenge Me**
   - The backend generates three logic-based questions from the document using the LLM.
   - User answers each question in the UI.
   - The backend evaluates each answer with the LLM, providing feedback and citing the relevant part of the document.

5. **Rate Limiting**
   - All LLM calls are rate-limited to 29 per minute and 999 per day to comply with Groq’s API limits.

---

## Setup & Usage

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Q&A assistant
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

- Create a `.env` file in the project root:
  ```
  GROQ_API_KEY=your-groq-api-key
  ```

### 5. Run the Backend

```bash
uvicorn backend.main:app --reload
```

### 6. Run the Frontend

```bash
streamlit run streamlit_app.py
```

### 7. Open the App

- Go to `http://localhost:8501` in your browser.

---

## File Structure

```
Q&A assistant/
  backend/
    main.py                  # FastAPI app and endpoints
    qa_engine.py             # LLM-powered Q&A, summary, evaluation
    logic_question_generator.py # LLM-powered logic question generation
    document_processor.py    # PDF/TXT text extraction
    utils.py                 # Text cleaning and utility functions
  streamlit_app.py           # Streamlit frontend
  requirements.txt           # Python dependencies
  .env                       # Environment variables (not committed)
```

---

## Customization

- **Change LLM Model:**  
  Edit the model name in `qa_engine.py` and `logic_question_generator.py` to use a different Groq-supported model.
- **Rate Limits:**  
  Adjust the limits in `qa_engine.py` as needed.

---

## Notes

- This project is for local use and demonstration. For production, consider persistent storage, authentication, and distributed rate limiting.
- The rate limiting is in-memory and per-process; it will reset if the backend restarts.

---

## License

MIT License

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [Groq](https://console.groq.com/)
```
