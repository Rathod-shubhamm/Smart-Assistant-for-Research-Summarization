from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
import time

# Simple in-memory rate limiting (per process)
minute_window = 60  # seconds
minute_limit = 29
minute_requests = []

day_window = 24 * 60 * 60  # seconds
day_limit = 999
day_requests = []

def check_rate_limit():
    now = time.time()
    # Clean up old minute requests
    global minute_requests, day_requests
    minute_requests[:] = [t for t in minute_requests if now - t < minute_window]
    day_requests[:] = [t for t in day_requests if now - t < day_window]
    if len(minute_requests) >= minute_limit:
        raise Exception(f"Rate limit exceeded: {minute_limit} requests per minute allowed.")
    if len(day_requests) >= day_limit:
        raise Exception(f"Rate limit exceeded: {day_limit} requests per day allowed.")
    minute_requests.append(now)
    day_requests.append(now)


def generate_summary(text: str) -> str:
    check_rate_limit()
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Summarize the following document in under 150 words:\n\n{text[:4000]}"
    messages = [
        SystemMessage(content="You are a concise academic summarizer."),
        HumanMessage(content=prompt)
    ]
    return llm.invoke(messages).content

def answer_question(text: str, question: str):
    check_rate_limit()
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Document:\n{text[:4000]}\n\nQuestion: {question}\n\nAnswer the question using only the document content. Justify your answer with the paragraph or section reference. In your answer quote the paragraph or section that justifies the answer at the end of answer in a new line. "
    messages = [
        SystemMessage(content="You are a helpful assistant that only uses document context."),
        HumanMessage(content=prompt)
    ]
    answer = llm.invoke(messages).content
    return answer, " Based on the given document context."

def evaluate_user_answer(text: str, question: str, user_answer: str):
    check_rate_limit()
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Document:\n{text[:4000]}\n\nQuestion: {question}\nUser's Answer: {user_answer}\n\nEvaluate the user's answer. Is it correct based on the document? Explain why or why not and cite relevant part of the text."
    messages = [
        SystemMessage(content="You are a strict evaluator that uses only the document to grade answers."),
        HumanMessage(content=prompt)
    ]
    evaluation = llm.invoke(messages).content
    return {"evaluation": evaluation}

def get_questions(text: str) -> list:
    check_rate_limit()
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Extract three well-formed questions from the following text:\n\n{text[:4000]}"
    messages = [
        SystemMessage(content="You are a helpful assistant that extracts questions from text."),
        HumanMessage(content=prompt)
    ]
    result = llm.invoke(messages).content
    questions = [q.strip() for q in result.strip().split("\n") if q.strip()]
    return questions[:3]  # Only return the first 3 non-empty questions