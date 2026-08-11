

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


# Ragas Evaluation
python evaluation/evaluate_ragas.py 