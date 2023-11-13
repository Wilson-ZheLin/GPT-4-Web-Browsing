import time
import json
from fetch_web_content import fetch_web_content
from llm_answer import getAnswer, format_reference
from retrieval import embeddding_retrieval
from locate_reference import locate_source

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

    reference_cards = locate_source(answer, serper_response)
    json_formatted_cards = json.dumps(reference_cards, indent=4)


    print('\n\n', '='*30, "Reference cards", "="*30, "\n")
    print(json_formatted_cards)