from typing import List,TypedDict

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph,START

from chains import chain2, chain
from tools import tool_calling

MAX_TERATIONS=2
    

graph = MessageGraph()

graph.add_node("draft",chain)
graph.add_node('execute_tools',tool_calling)
graph.add_node('revisor',chain2)

graph.add_edge(START,"draft")
graph.add_edge("draft","execute_tools")
graph.add_edge("execute_tools",'revisor')

def event_loop(state:List[BaseMessage])->str:
    count_total_visits=sum(isinstance(msg,ToolMessage) for msg in state)
    if count_total_visits >= MAX_TERATIONS:
        return END
    return "execute_tools"

graph.add_conditional_edges("revisor", event_loop)

model=graph.compile()

print(model.get_graph().draw_mermaid_png)

response = model.invoke("Write about how Quantum computing is going to change AI Growth in future?")

print(response[-1].tool_calls[0]["args"]["answer"])