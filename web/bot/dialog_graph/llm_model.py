from langchain import PromptTemplate, HuggingFaceHub, LLMChain


def chain_setup():
    template = """<|prompter|>{question}<|endoftext|><|assistant|>"""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5")
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    return llm_chain


def get_response_oasst(question: str, llm_chain=chain_setup()):
    response = llm_chain.run(question)
    return response if response != 'None' else None
