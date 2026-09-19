from fastapi import FastAPI,HTTPException,status
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel,Field
from typing import Literal
from backend.Agent.graph import rag_agent
from backend.project_pull.pull import repo_pull
import os
import logging
from config import settings
os.environ['LANGSMITH_API_KEY']=settings.LANGSMITH_API_KEY
os.environ['LANGSMITH_ENDPOINT']=settings.LANGSMITH_ENDPOINT
os.environ['LANGSMITH_PROJECT']=settings.LANGSMITH_PROJECT
os.environ['LANGSMITH_TRACING']=settings.LANGSMITH_TRACING
class agent_request(BaseModel):
    github_repo:str
    goal:str
    id:str
    
app=FastAPI()
@app.post('/agent')
async def agent(request:agent_request):
    config = {
    "configurable": {
        "thread_id": request.id
    }
    }
    try:
        codebase=await run_in_threadpool(repo_pull,request.github_repo)
        result=await rag_agent.ainvoke({'codebase':codebase,'goal':request.goal,'repo_url':request.github_repo},config=config)

    except Exception as e:
        logging.exception(f"error happend for {request.id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return result['final_post']
        
        
        

