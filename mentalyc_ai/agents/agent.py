from ..agents.base_agent import BaseAgent
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List

class Agent(BaseAgent):
    def __init__(self, name: str, schema: BaseModel, system_message: str, model: str ="llama-3.3-70b-specdec", temperature=0):
        super().__init__(
            name=name,
            model=model,
            temperature=temperature,
            schema=schema,
            system_message=system_message,
            tools=None
        )
    
    def create_prompt(self) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_message),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        prompt = prompt.partial(
            name=self.name
        )
        return prompt

    def get_agent(self):
        prompt = self.create_prompt()
        if self.schema:
            return prompt | self.llm.with_structured_output(self.schema)
        return prompt | self.llm