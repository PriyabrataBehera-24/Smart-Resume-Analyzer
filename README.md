# Smart Resume Analyzer

## Overview
The Smart Resume Analyzer is a web application designed to enhance the recruitment process using machine learning and artificial intelligence. It allows users to upload resumes and input job descriptions to identify the most relevant resumes based on their similarity to the job description. The system leverages TF-IDF and cosine similarity techniques for precise matching and includes an interactive chatbot that provides personalized suggestions for resume improvement by extracting and analyzing key terms from job descriptions

## Technologies Used
- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn (TF-IDF, Cosine Similarity)
- **Text Extraction:** PyPDF2, docx2txt

## Features
1. **Resume Upload:**
   - Users can upload resumes in PDF, DOCX, or TXT format.

2. **Job Description Input:**
   - Users can input a job description to be matched with the uploaded resumes.

3. **Resume Matching:**
   - Utilizes TF-IDF and cosine similarity to rank resumes based on their relevance to the job description.

4. **Chatbot Integration:**
   - A chatbot provides suggestions for improving resumes based on keyword extraction from the job description.

## Instructions
1. **Setup:**
   - Ensure you have the required Python libraries installed: `Flask`, `PyPDF2`, `docx2txt`, `scikit-learn`.
   - Create an `uploads` folder for saving resumes.

2. **Run the Application:**
   - Start the Flask application with `python <filename>.py`.

3. **Usage:**
   - Upload resumes and enter a job description.
   - View the top matching resumes and their similarity scores.
   - Interact with the chatbot for tips on improving or tailoring your resume based on the job description.

