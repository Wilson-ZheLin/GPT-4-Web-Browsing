import requests
import re
import json

def serper(query: str):
    '''
    Utilize Sperer's API service to obtain Google search results and returng the results in JSON
    '''
    url = "https://google.serper.dev/search"
    serper_settings = {"q": query, "page": 2} 

    if(contains_chinese(query)):
        serper_settings.update({"gl": "cn", "hl": "zh-cn",})

    payload = json.dumps(serper_settings)

    headers = {
        "X-API-KEY": "",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    output = response.json()
    return output

def contains_chinese(query: str):
    '''
    Check if a string contains Chinese characters
    '''
    pattern = re.compile(r'[\u4e00-\u9fff]+')
    return bool(pattern.search(query))

def extract_components_from_serper(serper_response: dict):
    '''
    Extract and store the Sperer contents into a dictionary
    '''
    titles, links, snippets, icons = [], [], [], []

    for item in serper_response.get("organic"):
        if "link" in item:
            links.append(item["link"])
        
        if "title" in item:
            titles.append(item["title"])
        
        if "snippet" in item:
            snippets.append(item["snippet"])
        
        # if "imageUrl" in item:
        #     icons.append(item["imageUrl"])
        # else:
        #     icons.append("") # some webpages don't have icons
    
    query = serper_response.get("searchParameters")["q"]
    count = len(links)
    language = "zh-cn" if contains_chinese(query) else "en-us"
    output_dict = {'query': query, 'language': language, 'count': count, 'titles': titles, 'links': links, 'snippets': snippets}

    return output_dict

# Testing this code:
if __name__ == "__main__":
    query = "Tencent Games global market share"
    serper_response = serper(query)
    serper_components = extract_components_from_serper(serper_response)

    print(serper_components)
    