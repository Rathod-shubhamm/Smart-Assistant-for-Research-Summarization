from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

def generate_logic_questions(text: str):
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    prompt = f"Document:\n{text[:4000]}\n\nGenerate three logic-based or comprehension questions derived from the content of this document. Response should only consists three questions . Do not include any explanations, commentary, or introductory phrases."
    messages = [
        SystemMessage(content="You are a tutor designing logic-based reading comprehension questions."),
        HumanMessage(content=prompt)
    ]
    result = llm.invoke(messages).content
    questions = [q.strip() for q in result.strip().split("\n") if q.strip()]
    return questions[:3]