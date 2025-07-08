from typing import TypedDict
from langgraph.graph import StateGraph

class complemnter(TypedDict):
    message:str

def complement_message(state: complemnter) -> complemnter:
    state['message'] =(f"Hii {state['message']} , you are doing really well after all you are learnign langgraph ") 
    return state

graph = StateGraph(complemnter)
graph.add_node('greeter',complement_message)
graph.set_entry_point('greeter')
graph.set_finish_point('greeter')

model=graph.compile()
print(model.invoke({'message':'Pratap'}))