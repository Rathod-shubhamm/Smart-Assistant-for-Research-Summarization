import re
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

def clean_text(text: str) -> str:
    # Simple text cleaner to remove excessive whitespace and control characters
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def generate_summary(text: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Summarize the following document in under 150 words:\n\n{text[:4000]}"
    messages = [
        SystemMessage(content="You are a concise academic summarizer."),
        HumanMessage(content=prompt)
    ]
    return llm.invoke(messages).content

def answer_question(text: str, question: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Document:\n{text[:4000]}\n\nQuestion: {question}\n\nAnswer the question using only the document content. Justify your answer with the paragraph or section reference."
    messages = [
        SystemMessage(content="You are a helpful assistant that only uses document context."),
        HumanMessage(content=prompt)
    ]
    return llm.invoke(messages).content

def evaluate_user_answer(text: str, question: str, user_answer: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Document:\n{text[:4000]}\n\nQuestion: {question}\nUser's Answer: {user_answer}\n\nEvaluate the user's answer. Is it correct based on the document? Explain why or why not and cite relevant part of the text."
    messages = [
        SystemMessage(content="You are a strict evaluator that uses only the document to grade answers."),
        HumanMessage(content=prompt)
    ]
    return llm.invoke(messages).content

def generate_logic_questions(text: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Document:\n{text[:4000]}\n\nGenerate three logic-based or comprehension questions derived from the content of this document."
    messages = [
        SystemMessage(content="You are a tutor designing logic-based reading comprehension questions."),
        HumanMessage(content=prompt)
    ]
    return llm.invoke(messages).content