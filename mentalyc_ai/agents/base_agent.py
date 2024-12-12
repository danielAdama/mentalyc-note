import dotenv
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
from typing import List, Union
from pydantic import BaseModel, Field, field_validator
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os

class BaseAgent:
    def __init__(
        self,
        name: str,
        model: str, 
        temperature: float,
        schema: Union[BaseModel, None] = None,
        system_message: Union[str, None] = None,
        tools: Union[list, None] = None
        ):
        self.name = name
        self.schema = schema
        self.tools = tools if tools is not None else []
        self.system_message = system_message
        self.llm = ChatGroq(model=model, temperature=temperature, api_key=os.environ.get("GROQ_API_KEY"))

    def create_prompt(self) -> ChatPromptTemplate:
        """Create and return the ChatPromptTemplate."""
        raise NotImplementedError("Subclasses should implement this method.")

    def get_agent(self):
        """Return the configured agent."""
        prompt = self.create_prompt()
        if self.tools:
            return prompt | self.llm.bind_tools(self.tools)
        return prompt | self.llm