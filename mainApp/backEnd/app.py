from flask import Flask, jsonify, request
import os
import google.generativeai as genai
import numpy as np
from FlagEmbedding import FlagModel

app = Flask(__name__)

# Set up Gemini API
genai.configure(api_key="AIzaSyBwtKbwZNGMuzJQ1QolielQE7XNIIkRefE")
model = genai.GenerativeModel('gemini-pro')

# Set up RAG components
embeddings_model_bge = FlagModel('BAAI/bge-base-en-v1.5', use_fp16=True)
# reranker = FlagReranker('BAAI/bge-reranker-large', use_fp16=True)

# Load and preprocess the dataset
filename = './dataset_gwdg.txt'
with open(filename, 'r') as f:
    document = f.read()
document_chunks = document.split('########')
embeddings_bge = embeddings_model_bge.encode(document_chunks)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data['message']

    try:
        # RAG process
        emb_bge_query = embeddings_model_bge.encode([user_message])
        scores = emb_bge_query @ embeddings_bge.T
        scores = np.squeeze(scores)
        max_idx = np.argsort(-scores)
        
        context_chunks_init = []
        context_scores = []
        for idx in max_idx[:3]:
            context_chunks_init.append(document_chunks[idx])
            context_scores.append(scores[idx])
        
        context_chunks_as_str = '\n###\n'.join([str(elem) for elem in context_chunks_init])
        
        prompt_template = """You are a Senior Software Developer at Microsoft. Use the context to answer the question at the end. Give a very detailed answer. Never mention about context and where information comes from.

Context: {context}

Question: {question}

Answer:"""
        
        llm_full_query = prompt_template.format(context=context_chunks_as_str, question=user_message)
        
        # Call Gemini API with the augmented query
        response = model.generate_content(llm_full_query)

        # Extract the assistant's reply
        assistant_reply = response.text

        return jsonify({'message': assistant_reply})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == "__main__":
    app.run(debug=True)