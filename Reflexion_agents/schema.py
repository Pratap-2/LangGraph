from pydantic import BaseModel,Field
from typing import TypedDict ,List

class Reflection(BaseModel):
    missing : str = Field(description='Critique of what is missing')
    superfluous:str= Field(description='Critique of what is superfluous')

class QuestionAnswer(BaseModel):
    """Answer the question."""

    answer:str=Field(description='Write the detailed answer in approx. 100 words')
    queries:List[str]=Field(description='1-3 search queries for researching improvements to address the critique of your current answer.')
    reflection:Reflection = Field(description='Your reflection of the final answer')

class ReviseAnswer(QuestionAnswer):
    """Revise your original answer to your question."""

    refrences: List[str]= Field(description='Citations motivating your updated answer.')