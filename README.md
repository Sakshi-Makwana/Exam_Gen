# Exam-Gen: AI Question Paper Generator

**Exam-Gen** is an intelligent **Streamlit web application** designed to assist educators by automating the creation of diverse and well-structured exam papers.  
Powered by a sophisticated **Retrieval-Augmented Generation (RAG)** pipeline, this tool analyzes source documents (like textbook chapters or notes) and generates a **unique question paper with a detailed answer key** based on user-defined parameters.

This project moves beyond simple text generation to create a practical, real-world tool that saves educators hours of manual effort — ensuring **exam quality, fairness, and comprehensive syllabus coverage.**



## Key Features

- **Multi-Document Support:** Upload multiple PDF files simultaneously to form a unified knowledge base for question generation.  
- **Dynamic Exam Structure:** Full control over the exam’s composition — specify the exact number of questions for 1, 2, 3, 4, 5, or 10 marks.  
- **Intelligent Topic Diversity:** Automatically identifies main topics using BERTopic and cycles through them during generation to ensure topic balance.  
- **Semantic Uniqueness Filter:** Prevents repetitive or similar questions by over-generating a pool and applying semantic similarity filtering to keep only unique ones.  
- **PDF Export:** Instantly download the generated **Question Paper** and **Answer Key** as separate, cleanly formatted PDF files.  
- **Modern & Intuitive UI:** A clean, responsive, and user-friendly interface built with Streamlit for a seamless experience.  



## System Architecture: The RAG Pipeline

Exam-Gen is built on a modern, multi-stage **Retrieval-Augmented Generation (RAG)** architecture that ensures all generated content is **factually grounded** in the provided material.

### 1. Ingestion & Processing
Extracts and chunks text from uploaded PDFs using PyMuPDF and LangChain’s text splitters.

### 2. Topic Modeling
Uses **BERTopic** to identify key themes, ensuring question diversity and topic coverage.

### 3. Embedding and Indexing
Converts text chunks into **semantic vectors** via Sentence-Transformers and stores them in **ChromaDB**, a lightweight vector database.

### 4. Intelligent Retrieval
Queries the vector store for the most relevant context using a **global topic cycler** to prevent topic lock-on.

### 5. Constrained Generation
Feeds the retrieved context into **Google Gemini LLM** with dynamically engineered prompts that adjust by mark value and complexity.

### 6. Uniqueness Filtering
Applies **cosine similarity filtering** to remove semantically similar questions.

### 7. PDF Output
Formats the final, curated questions and answers into **professional PDF documents** ready for distribution.



## Technology Stack

| Category | Technology / Library | Purpose |
|-----------|----------------------|----------|
| **Web Framework** | Streamlit | Building the interactive user interface |
| **AI/NLP Framework** | LangChain | Core logic for text splitting and orchestration |
| **Generative LLM** | Google Gemini API (Flash) | Generating questions and answers |
| **Embedding Model** | Sentence-Transformers | Creating semantic text embeddings |
| **Vector Database** | ChromaDB | Storing and retrieving text embeddings |
| **Topic Modeling** | BERTopic | Identifying key topics for question diversity |
| **PDF Handling** | PyMuPDF, FPDF2 | Text extraction and PDF generation |
| **Data Science** | Scikit-learn, NLTK | Cosine similarity, stop word removal, and NLP utilities |



## Setup and Local Installation

Follow these steps to run Exam-Gen locally on your system.

### Prerequisites
- Python 3.8+
- Git installed
- A [Google AI for Developers (Gemini)](https://ai.google.dev) API key
- (Optional) A GitHub account for deployment



### Installation Steps

#### Clone the Repository
```bash
git clone https://github.com/014-Jayal/Exam-Gen.git
cd Exam-Gen
```

#### Create and Activate a Virtual Environment
```bash
python -m venv venv

# On Windows
.env\Scriptsctivate

# On macOS/Linux
source venv/bin/activate
```

#### Install Required Dependencies
```bash
pip install -r requirements.txt
```

#### Set Up Your API Key
Create a `.env` file in the project root and add your Gemini API key:
```bash
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

#### Run the Streamlit Application
```bash
streamlit run app.py
```

Once the server starts, the app will open automatically in your default web browser.



## How to Use

1. **Upload Documents:** Use the sidebar to upload one or more PDF files as the knowledge base.  
2. **Define Structure:** Specify the number of questions for each mark category (1, 2, 3, 4, 5, or 10 marks).  
3. **Generate:** Click **"Generate Now!"** to start the process.  
4. **Review and Download:** Preview the generated questions and answers in separate tabs, or download them directly as PDFs.  
5. **Start Over:** Use the **"Start Over"** button to clear the session and begin a new exam generation process.



## Example Output

- **Question Paper:**  
  A structured set of diverse questions across all specified marks.  
- **Answer Key:**  
  A detailed, AI-generated marking scheme corresponding to each question.



> *"Exam-Gen" empowers educators by transforming hours of manual question paper preparation into a matter of minutes - combining AI intelligence with human intention.*
