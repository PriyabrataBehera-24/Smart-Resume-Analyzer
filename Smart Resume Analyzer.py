from flask import Flask, request, render_template, jsonify
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Helper functions
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting text from TXT: {e}")
        return ""

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        return ""

def extract_keywords(job_description):
    words = re.findall(r'\b\w+\b', job_description)
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([" ".join(words)])
    scores = tfidf_matrix.toarray()[0]
    word_score = dict(zip(vectorizer.get_feature_names_out(), scores))
    sorted_words = sorted(word_score.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in sorted_words[:10]]
    return top_keywords

@app.route("/")
def atschecker():
    return render_template('atstracker.html')

@app.route("/matcher", methods=['GET', 'POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form.get('job_description')
        resume_files = request.files.getlist('resumes')
        
        if not job_description or not resume_files:
            return render_template('atstracker.html', message="Please Upload Resume and Job Description")
        
        # Text extraction and similarity calculation
        resumes_text = []
        for resume_file in resume_files:
            if resume_file and allowed_file(resume_file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
                try:
                    resume_file.save(filename)
                    resumes_text.append(extract_text(filename))
                except Exception as e:
                    return render_template('atstracker.html', message=f"Error saving or processing file: {e}")
            else:
                return render_template('atstracker.html', message="Unsupported file type.")
        
        # Vectorizing and calculating cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english')
        job_vector = vectorizer.fit_transform([job_description])
        resume_vectors = vectorizer.transform(resumes_text)
        similarities = cosine_similarity(job_vector, resume_vectors).flatten()
        
        # Sort by top similarities
        top_indices = similarities.argsort()[-3:][::-1]
        top_resumes = [resume_files[i].filename for i in top_indices]
        similarity_scores = [round(similarities[i] * 100, 2) for i in top_indices]

        return render_template('atstracker.html', message="Top matching resumes:", top_resumes=top_resumes, similarity_scores=similarity_scores)

    return render_template('atstracker.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

@app.route("/chat", methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = generate_chatbot_response(user_input)
    return jsonify({"response": response})

def generate_chatbot_response(user_input):
    # Check if the input seems like a job description
    if "job description:" in user_input.lower():
        # Extract keywords from the provided job description
        job_description = user_input.split("job description:", 1)[1].strip()
        keywords = extract_keywords(job_description)
        return f"Based on the provided job description, consider including these keywords: {', '.join(keywords)}."
    elif "improve" in user_input.lower():
        # Provide guidance on resume improvement
        example_job_description = """
        We are looking for a software engineer with experience in Python, Java, and cloud technologies.
        The ideal candidate should have strong problem-solving skills, knowledge of machine learning, and familiarity with DevOps practices.
        """
        keywords = extract_keywords(example_job_description)
        return f"To improve your resume, make sure to highlight relevant skills and experiences. Consider including these keywords: {', '.join(keywords)}."
    elif "tailor" in user_input.lower():
        return "Tailor your resume by matching your skills and experiences with the job requirements. Use the same keywords found in the job description."
    else:
        return "I can help with suggestions on how to improve your resume or tailor it to a specific job description. Ask me how!"

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
