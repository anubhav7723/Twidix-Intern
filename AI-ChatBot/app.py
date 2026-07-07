from flask import Flask, render_template, request, jsonify
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaLLM
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import requests
from dotenv import load_dotenv
import os
from src.prompt import *

app = Flask(__name__)
load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


embeddings = download_hugging_face_embeddings()
index_name = "medicalbot"
docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
retriever = docsearch.as_retriever(
    search_type='similarity',
    search_kwargs={
        'k': 1  
    }
)


llm = OllamaLLM(model="llama2")


prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Context:\n{context}\n\nQuestion: {input}")
])


question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

def trim_to_sentences(text, max_sentences=4):
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    return ' '.join(sentences[:max_sentences])


def extract_topic(msg):
    for kw in ["about", "on", "regarding", "of"]:
        if kw in msg.lower():
            return msg.lower().split(kw)[-1].strip()
    return msg.split()[-1].strip()


def handle_general_question_with_llama_groq(msg):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful and friendly assistant."},
            {"role": "user", "content": msg}
        ],
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 1
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("Groq Error:", e)
        return "⚠️ Sorry, I couldn't process that right now."


def is_general_question(msg):
    keywords = ["your name", "how are you", "my name", "hello", "hi", "bye", "Thank You","thanks", "talk to me"]
    return any(kw in msg.lower() for kw in keywords)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=['GET', 'POST'])
def chat():
    msg = request.form["msg"]
    print("User input:", msg)

    if is_general_question(msg):
        return handle_general_question_with_llama_groq(msg)

    topic = extract_topic(msg)
    refined_input = f"Provide a short and precise explanation about {topic}. Start your answer with: 'Here is the information about {topic}:'"
    print("Formatted prompt for RAG:", refined_input)

    response = rag_chain.invoke({"input": refined_input})
    print("Response:", response["answer"])
    trimmed_answer = trim_to_sentences(response["answer"])
    return trimmed_answer

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
