from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = ChatGroq(model=os.getenv("MODEL"))