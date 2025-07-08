from typing import TypedDict,List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name:str
    values:List[int]
    message:str
    operation:str

def mult_list(vector:List):
    prod=1
    for i in range(len(vector)):
        prod=prod*vector[i]
    return prod


def conditional_output(state:AgentState) -> AgentState:
    if state['operation']=='+':
        state['message']=f"Hii {state['name']}, your answer is {sum(state['values'])}"
    elif state['operation']=='*':
        state['message']=f"Hii {state['name']}, your answer is {(mult_list(state['values']))}"

    return state


graph=StateGraph(AgentState)
graph.add_node('oper',conditional_output)
graph.set_entry_point('oper')
graph.set_finish_point('oper')

model=graph.compile()

rslt=model.invoke({'name':'Jack Sparrow',"values":[1,2,3],"operation":'*'})
print(rslt['message'])

