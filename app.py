from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import pdfplumber
import os
import tempfile
#app.py
app = Flask(__name__)

# Load models (loaded once at startup)
print("Loading summarization model...")
summarizer = pipeline("summarization", model="t5-small")

print("Loading Q&A model...")
qa_model = pipeline("question-answering", model="deepset/minilm-uncased-squad2")
print("All models loaded!")

# Store the last extracted text in memory (simple approach for mini project)
extracted_text_store = {"text": ""}


def chunk_text(text, max_chunk=1000):
    """Split long text into chunks for summarization."""
    words = text.split()
    chunks = []
    current = []
    for word in words:
        current.append(word)
        if len(" ".join(current)) >= max_chunk:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    text = ""

    # Handle PDF upload
    if 'pdf_file' in request.files and request.files['pdf_file'].filename != '':
        pdf_file = request.files['pdf_file']
        
        # 1. Create the temp file and save it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_file.save(tmp.name)
            tmp_path = tmp.name  # Store the path to use outside this block

        try:
            # 2. Open and extract text (This 'with' ensures pdfplumber closes properly)
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        finally:
            # 3. NOW it is safe to delete because all 'with' blocks are closed
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    # Handle plain text input
    else:
        text = request.form.get('text', '').strip()

    if not text:
        return jsonify({"error": "No input provided."}), 400

    # Store text for Q&A
    extracted_text_store["text"] = text

    # Summarize in chunks to handle long text
    chunks = chunk_text(text)
    summaries = []
    for chunk in chunks:
        if len(chunk.split()) < 30:
            summaries.append(chunk)
            continue
        result = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summaries.append(result[0]['summary_text'])

    final_summary = " ".join(summaries)
    return jsonify({"summary": final_summary, "original": text[:500] + "..." if len(text) > 500 else text})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    context = extracted_text_store.get("text", "")

    if not question:
        return jsonify({"error": "Please enter a question."}), 400
    if not context:
        return jsonify({"error": "Please summarize some notes first before asking questions."}), 400

    # Use only the first 2000 chars as context (roberta has token limits)
    context_chunk = context[:2000]
    result = qa_model(question=question, context=context_chunk)
    return jsonify({"answer": result["answer"], "score": round(result["score"], 3)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)