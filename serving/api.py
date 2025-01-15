from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.responses import JSONResponse

from sentence_transformers import SentenceTransformer

import os

from pinecone import Pinecone
from pydantic import BaseModel

from transformers import pipeline

app = FastAPI()

models = {}

pinecone_client = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
pinecone_index = pinecone_client.Index('open-domain-qa-project')

class ContextRequest(BaseModel):
    context:str
    question:str

class OpenDomainRequest(BaseModel):
    question:str

def load_open_domain_vector_qa():
    model_name = "cquentin48/open_domain_vector_qa"
    return SentenceTransformer(model_name)

def load_context_model():
    model_name = "cquentin48/context_based_qa"
    model = pipeline("question-answering", model=model_name, tokenizer=model_name)
    return model

@asynccontextmanager
async def lifespan(app: FastAPI):
    models["context_based_qa"] = load_context_model()
    models["open_domain_vector_qa"] = load_open_domain_vector_qa()

    yield

    models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def index():
    return {
        'message':'Open domain QA successfully set!'
    }

@app.post("/ask/open")
def ask_open_domain_question(request:OpenDomainRequest):
    question = request.question
    xq = models['open_domain_vector_qa'].encode([question]).tolist()
    xc = pinecone_index.query(
        vector=xq,
        top_k=1,
        include_values=False,
        include_metadata=True
    )
    result = xc['matches'][0]['metadata']['text']
    answer = {'answer':result}
    return JSONResponse(content=answer)

@app.post("/ask/context")
def ask_context_question(request:ContextRequest):
    input = {
        'question':request.question,
        'context':request.context
    }
    result = models["context_based_qa"].predict(input)
    answer = {'answer':result['answer']}
    return JSONResponse(content=answer)