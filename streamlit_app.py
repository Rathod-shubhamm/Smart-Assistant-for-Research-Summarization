import streamlit as st
import requests

st.set_page_config(page_title="GenAI Q&A Assistant", layout="wide")
st.title("GenAI Q&A Assistant")

# Sidebar for document upload and mode selection
st.sidebar.header("Upload Document")
doc_file = st.sidebar.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])

if doc_file:
    st.sidebar.success(f"Uploaded: {doc_file.name}")
    # Send file to backend for processing (replace with your backend URL)
    files = {"file": (doc_file.name, doc_file, doc_file.type)}
    response = requests.post("http://localhost:8000/upload", files=files)
    if response.status_code == 200:
        doc_id = response.json().get("doc_id")
        summary = response.json().get("summary")
        st.subheader("Document Summary (≤ 150 words)")
        st.write(summary)

        mode = st.sidebar.radio("Choose Interaction Mode", ["Ask Anything", "Challenge Me"])

        if mode == "Ask Anything":
            st.header("Ask Anything")
            user_question = st.text_input("Enter your question about the document:")
            if st.button("Ask") and user_question:
                qa_resp = requests.post(
                    "http://localhost:8000/ask", 
                    json={"doc_id": doc_id, "question": user_question}
                )
                if qa_resp.status_code == 200:
                    answer = qa_resp.json().get("answer")
                    justification = qa_resp.json().get("justification")
                    st.markdown(f"**Answer:** {answer}")
                    st.markdown(f"**Justification:** {justification}")
                else:
                    st.error("Failed to get answer from backend.")

        elif mode == "Challenge Me":
            st.header("Challenge Me")
            # Only fetch questions if not already in session_state or if doc_id changed
            if "challenge_questions" not in st.session_state or st.session_state.get("last_doc_id") != doc_id:
                ch_resp = requests.post(
                    "http://localhost:8000/challenge", 
                    json={"doc_id": doc_id}
                )
                if ch_resp.status_code == 200:
                    st.session_state["challenge_questions"] = ch_resp.json().get("questions", [])
                    st.session_state["last_doc_id"] = doc_id
                else:
                    st.error("Failed to get challenge questions from backend.")
                    st.session_state["challenge_questions"] = []
            questions = st.session_state.get("challenge_questions", [])
            user_answers = []
            for idx, q in enumerate(questions):
                user_answer = st.text_input(f"Q{idx+1}: {q}", key=f"challenge_{idx}")
                user_answers.append(user_answer)
            if st.button("Submit Answers"):
                eval_resp = requests.post(
                    "http://localhost:8000/evaluate", 
                    json={"doc_id": doc_id, "questions": questions, "answers": user_answers}
                )
                if eval_resp.status_code == 200:
                    feedback = eval_resp.json().get("feedback", [])
                    for idx, fb in enumerate(feedback):
                        st.markdown(f"**Q{idx+1} Feedback:** {fb}")
                else:
                    st.error("Failed to get feedback from backend.")
else:
    st.info("Please upload a PDF or TXT document to begin.") 