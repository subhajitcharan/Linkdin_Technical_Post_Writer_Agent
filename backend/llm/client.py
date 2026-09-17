from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAI
from config import settings
from langchain_core.output_parsers import StrOutputParser
from backend.llm.structure import review
llm=ChatGoogleGenerativeAI(model=settings.MODEL,api_key=settings.API_KEY)|StrOutputParser()
llm2=ChatGoogleGenerativeAI(model=settings.MODEL,api_key=settings.API_KEY)
structure_llm=llm2.with_structured_output(review)