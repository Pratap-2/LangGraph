from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
import datetime
from langchain_core.output_parsers.openai_tools import PydanticToolsParser,JsonOutputToolsParser
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from schema import QuestionAnswer,ReviseAnswer
load_dotenv()

pydantic_parser = PydanticToolsParser(tools=[QuestionAnswer])
parser = JsonOutputToolsParser(return_id=True)

actor_prompt_template=ChatPromptTemplate.from_messages([
        (
            "system",
            """You are expert AI researcher.
            Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

first_respond_prompt_template=actor_prompt_template.partial(
    first_instruction="Provide a detailed response of 100 words answer"
)

llm=ChatOpenAI(model='gpt-4o-mini')

chain=first_respond_prompt_template | llm.bind_tools(tools=[QuestionAnswer],tool_choice='QuestionAnswer')
validator=PydanticToolsParser(tools=[QuestionAnswer])

# Revisor section

revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

chain2=actor_prompt_template.partial(first_instruction=revise_instructions) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")