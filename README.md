AI-Powered Document Processing & Summarization System

📌 Overview

An AI-powered application that processes PDF and DOCX documents and generates concise summaries using NLP and Transformer-based models. Built with a modular architecture for scalability and future enhancements.

✨ Features

- PDF & DOCX processing
- AI-based text summarization
- Secure authentication with bcrypt
- MongoDB 
- Streamlit interactive UI
- Modular project structure

🛠 Tech Stack

- python
- Streamlit
- Transformers & Hugging Face
- PyPDF2 / pdfplumber
- python-docx
- MongoDB 
- bcrypt

🚀 Run Locally

pip install -r requirements.txt
streamlit run frontend/main.py

📁 Structure

Ai_Project/
├── frontend/
├── backend/
├── models/
├── utils/
├── config/
└── tests/

🔐 Security

- Passwords hashed using bcrypt
- API keys stored in .env
- Sensitive files excluded from Git




