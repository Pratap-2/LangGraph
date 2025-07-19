from typing import List,Any,Dict
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
import json
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage,ToolMessage

tavily_tool=TavilySearch(max_results=5)
def tool_calling(state : List[BaseMessage]) ->List[BaseMessage]:
    last_Ai_meesage: AIMessage=state[-1]

    # Extract tool calls from the AI message
    if not hasattr(last_Ai_meesage,"tool_calls") or not last_Ai_meesage.tool_calls :
        return []
    
    tool_messages=[]

    # Process the AnswerQuestion or ReviseAnswer tool calls to extract search queries
    for tool_call in last_Ai_meesage.tool_calls:
        if tool_call['name'] in ["ReviseAnswer","QuestionAnswer"]:
            call_id=tool_call['id']
            search_queries=tool_call['args'].get('search_queries',[])
            # Execute each search query using the tavily tool
            query_results = {}
            for query in search_queries:
                rslt = tavily_tool.invoke(query)
                query_results[query] = rslt
             # Create a tool message with the results

            tool_messages.append(
                ToolMessage(
                    content=json.dumps(query_results),
                    tool_call_id=call_id
                )
            )
        return tool_messages
    

            
