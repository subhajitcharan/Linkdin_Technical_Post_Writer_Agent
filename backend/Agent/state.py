from typing import TypedDict,Literal,Annotated
class LlmState(TypedDict):
    repo_url:str
    criteria:Literal['yes','no']
    codebase:str
    summary:str
    goal:str
    itaration:int
    current_post:str
    final_post:str
    improvements:str
    
    
    