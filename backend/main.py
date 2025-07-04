from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.document_processor import extract_text_from_file
from backend.qa_engine import generate_summary, answer_question, evaluate_user_answer
from backend.logic_question_generator import generate_logic_questions
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_text = ""

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global document_text
    document_text = await extract_text_from_file(file)
    summary = generate_summary(document_text)
    return {"summary": summary}

@app.post("/ask")
async def ask_question(payload: dict):
    question = payload.get("question")
    answer, justification = answer_question(document_text, question)
    return {"answer": answer, "justification": justification}

@app.post("/challenge")
async def challenge_me():
    questions = generate_logic_questions(document_text)
    return {"questions": questions}

@app.post("/evaluate")
async def evaluate_answer(payload: dict):
    answers = payload.get("answers", [])
    questions = payload.get("questions", [])
    feedback = []
    for question, user_answer in zip(questions, answers):
        evaluation = evaluate_user_answer(document_text, question, user_answer)
        feedback.append(evaluation["evaluation"])
    return {"feedback": feedback}