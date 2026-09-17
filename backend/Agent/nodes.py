from backend.llm.client import llm,structure_llm
from backend.Agent.state import LlmState
from langsmith import traceable
@traceable(nsme='criteria agent')
def criteria_agent(state:LlmState):
    prompt=f"you check criteria for a agent that writes a technical post.check what the project does and determain if it is a genuine goal or not.if genuine return only yes and if fake or empty return no.goal->{state['goal']}"
    result=llm.invoke(prompt)
    state['criteria']=result
    return state
@traceable(nsme='router')
def router(state:LlmState):
    if state['criteria']=='yes':
        return 'ok'
    else:
        return 'notok'
@traceable(nsme='summary agent')
def summary_agent(state:LlmState):
    content=state['codebase']
    prompt=f"you are a technical summary generation agent. you generate a summary based on the project code and project goal.mention the technologies used in it properly.codefiles->{content}.project goal->{state['goal']}"
    result=llm.invoke(prompt)
    state['summary']=result
    return state
@traceable(nsme='post writer')
def post_writer(state:LlmState):
    prompt=f"""write an linkdin post based on a summary of a project.here are some examples->\n
    example1:\n
    Sometimes the best way to understand an abstraction is to build it yourself.
    I recently spent time stripping away the frameworks to build a neural network from scratch using only Python and NumPy. While we have incredible tools for deep learning today, implementing the math manually forces a deeper understanding of the underlying mechanics.

    In this repository, I implemented:
    • Dense layers and forward passes
    • Custom activation functions
    • Categorical cross-entropy loss
    • Numerical gradient checking for backpropagation validation

    If you are looking to demystify what happens inside the "black box" of a neural net, the code is well-commented and easy to step through.

    Link to the repo is in the comments below. Let me know if you spot any areas for optimization!

    #MachineLearning #Python #NumPy #DeepLearning #SoftwareEngineering.

    Example2:
    A question that comes up frequently in AI engineering right now: If we can easily add tools to agents using LangChain, why do we need Model Context Protocol (MCP) servers?

    I put together a new repository to explore exactly that.

    While LangChain provides an excellent client-side approach for agent tooling, I wanted to map out where MCP fits into the broader architectural picture. The repository contains a side-by-side implementation comparing the two approaches.

    Key takeaway: It comes down to standardization and reusability. MCP effectively decouples the tools from the specific orchestration framework, allowing you to build a server-side tool once and expose it to multiple different agent architectures securely.

    I've included architecture diagrams and code samples for both patterns in the repo. Would love to hear how other engineers are balancing client-side tools vs. dedicated MCP servers right now.

    #AI #SystemArchitecture #LangChain #SoftwareDevelopment #GenerativeAI.
    summary of the project->{state['summary']}.github link->{state['repo_url']}.only one post is enough.return only post
    """
    result=llm.invoke(prompt)
    state['current_post']=result
    return state
@traceable(nsme='review agent')
def review_agent(state:LlmState):
    prompt=f"""you are critic that judges linkdin posts.post->{state['current_post']}"""
    itaration=state.get('itaration',0)
    
    post=state['current_post']
    result=structure_llm.invoke(prompt)
    
    if result.approved or itaration>1:
        return {'final_post':post,'itaration':2}
    
    return {'improvements':result.improvement}
@traceable(nsme='router 2')
def router2(state:LlmState):
    if state.get('itaration',0)>1:
        return 'end'
    else:
        return 'improve'
@traceable(nsme='editor')
def editor(state:LlmState):
    itaration=state.get('itaration',0)

    current_post=state['current_post']
    improvements=state['improvements']
    prompt=f'improve the post based on the improvements needed.post->{current_post}.improvements->{improvements}'
    result=llm.invoke(prompt)
    itaration+=1
    return {'current_post':result,'itaration':itaration}