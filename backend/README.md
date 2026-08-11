

# Agentic RAG Document Search Platform

py -3.11 -m venv venv
venv\Scripts\activate

# To install requirement file
pip install -r requirements.txt

# This will generate full requirements file:
pip freeze > requirements.txt


Install Dependencies

# Requird Packages
# STEP 1
pip install crewai
pip install fastapi
pip install uvicorn
pip install python-dotenv
pip install mysql-connector-python
pip install pydantic
pip install pinecone
pip install pinecone-text
pip install langchain-huggingface
pip install sentence-transformers

or

pip install crewai fastapi uvicorn python-dotenv mysql-connector-python pydantic pinecone pinecone-text langchain-huggingface sentence-transformers

# To run API
uvicorn main:app --reload

# RAGAS Evaluation
pip install ragas==0.2.15
pip install datasets


# Run Ragas Evaluation
python evaluation/evaluate_ragas.py 



# MySQL Production Setup

## Create Database for Chat History
CREATE DATABASE documnet_search_db;

## Create Tables
CREATE TABLE chat_sessions (
    session_id CHAR(36) PRIMARY KEY,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);