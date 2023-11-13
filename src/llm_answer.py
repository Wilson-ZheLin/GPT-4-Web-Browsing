import time
import os
from fetch_web_content import fetch_web_content
from retrieval import embeddding_retrieval
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import (
    HumanMessage,
)

TOP_K = 10

def getAnswer(model_name: str, api_key: str, query: str, relevant_docs: str, language: str, output_format: str, profile: str):
    
    llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key, temperature=0.0, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])

    template = \
        r"""
        Web search result:
        {context_str}
        
        Instructions: You are a/an {profile}. Using the provided web search results, write a comprehensive and detailed reply to the given query. 
        Make sure to cite results using [number] notation after the reference.
        At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
        Here is an example of a reference:
            [1] URL: [https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/]
                Quoted sentence: Tencent accounted for roughly 50% of domestic market revenue for the quarter, compared to 40% in Q1 2022.
        
        Answer in language: {language}
        Query: {query}
        Output Format: {format}
        Please organize your output according to the Output Format. If the Output Format is empty, you can ignore it.
        """

    prompt_template = PromptTemplate(
        input_variables=["profile", "context_str", "language", "query", "format"],
        template=template
    )

    profile = "conscientious researcher" if profile == "" else profile
    summary_prompt = prompt_template.format(context_str = relevant_docs, language=language, query=query, format=output_format, profile=profile)
    print("\n\nThe message you sent to LLM:\n", summary_prompt)
    print("\n\n", "="*30, "GPT's Answer: ", "="*30, "\n")
    gpt_answer = llm([HumanMessage(content=summary_prompt)])

    return gpt_answer

def format_reference(relevant_docs_list: list, link_list: list):
    
    reference_url_list = [(relevant_docs_list[i].metadata)['url'] for i in range(TOP_K)]
    reference_content_list = [relevant_docs_list[i].page_content for i in range(TOP_K)]
    reference_index_list = [link_list.index(link)+1 for link in reference_url_list]
    rearranged_index_list = rearrange_index(reference_index_list)
    
    # sorted_contents = [content for _, content in sorted(zip(reference_index_list, reference_content_list))]
    # sorted_index_list = [sorted(set(reference_index_list)).index(i) + 1 for i in reference_index_list]

    formatted_reference = "\n"

    for i in range(TOP_K):
        formatted_reference += ('Webpage[' + str(rearranged_index_list[i]) + '], url: ' + reference_url_list[i] + ':\n' + reference_content_list[i] + '\n\n\n')

    return formatted_reference

def rearrange_index(original_index_list: list):
    index_dict = {}
    rearranged_index_list = []

    for index in original_index_list:
        if index not in index_dict: 
            index_dict.update({index: len(index_dict)+1})
            rearranged_index_list.append(len(index_dict))
        else:
            rearranged_index_list.append(index_dict[index])

    return rearranged_index_list

# Testing this code:
if __name__ == "__main__":

    query = "Tencent Game's Global Market Share"
    model_name = "gpt-3.5-turbo-16k"
    api_key = ""
    output_format = ""
    profile = ""
    
    web_contents, serper_response = fetch_web_content(query)
    relevant_docs_list = embeddding_retrieval(web_contents, serper_response['links'], query)
    formatted_relevant_docs = format_reference(relevant_docs_list, serper_response['links'])

    print(formatted_relevant_docs)

    start = time.time()
    ai_message_obj = getAnswer(model_name, api_key, query, formatted_relevant_docs, serper_response['language'], output_format, profile)
    answer = ai_message_obj.content + '\n' # Necessary for subsequent matching!!
    end = time.time()

    print("\nGPT Answer time:", end - start, "s")
