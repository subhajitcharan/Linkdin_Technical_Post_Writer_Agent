from langgraph.graph import StateGraph,START,END
from backend.Agent.state import LlmState
from backend.Agent.nodes import criteria_agent,router,summary_agent,post_writer,review_agent,router2,editor
from langgraph.checkpoint.memory import MemorySaver
graph=StateGraph(LlmState)
graph.add_node('criteria_agent',criteria_agent)
graph.add_node('summary_agent',summary_agent)
graph.add_node('post_writer',post_writer)
graph.add_node('review_agent',review_agent)
graph.add_node('editor',editor)
graph.add_edge(START,'criteria_agent')
graph.add_conditional_edges('criteria_agent',router,{'ok':'summary_agent','notok':END})
graph.add_edge('summary_agent','post_writer')
graph.add_edge('post_writer','review_agent')
graph.add_conditional_edges('review_agent',router2,{'end':END,'improve':'editor'})
graph.add_edge('editor','review_agent')
rag_agent=graph.compile(checkpointer=MemorySaver())
