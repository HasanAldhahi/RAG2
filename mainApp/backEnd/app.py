from flask import Flask, jsonify, render_template, request, json
from ctransformers import AutoModelForCausalLM
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_bad_secret_key'
limit_input_tokens=4096
model_path = './stablebeluga-7b.Q4_K_M.gguf'

# Function to initialize the model
def initialize_model():
	# os.path.abspath is important, otherwise AutoModelForCausalLM won't understand it
	# model_path = os.path.abspath(model_dir)
	llm = AutoModelForCausalLM.from_pretrained(model_path,
						local_files_only=True,
						gpu_layers=200,
						context_length=limit_input_tokens,
						max_new_tokens = 2048)
	return llm

@app.route('/')
def index():
    return render_template('../frontEnd/client.html')

@app.route('/send_message', methods=['POST'])
def send_message():
	# recieve message from the user
	data = request.get_json()

	# ensure message is converted to json if it was recieved as str
	if isinstance(data, str):
		data = json.loads(data)

	# extract text of the message
	query = data['message']

	# invoke beluga llm
	llm_answer = llm(query, top_k=40, top_p=0.4, temperature=0.5)
	response = {'message': llm_answer}

	return jsonify(response)


if __name__ == "__main__":
	# initialize llm model
	llm = initialize_model()
	app.run()