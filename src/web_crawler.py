import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

def get_webpage_html(url: str):
    
    # User-Agent for Windows, it simulates browser-like access
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    # User-Agent for MacOS:
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    
    response = requests.Response() # Create an empty Response object

    # PDF file takes so long to download, usually > 15s, so skip it for now
    if(url.endswith(".pdf")):
        return response

    try:
        response = requests.get(url, headers=headers, timeout=8) # the maximum access time is 8s, otherwise discard
        response.encoding = "utf-8"

    except requests.exceptions.Timeout:
        return response
    
    try:
        if response.status_code != 200:
            # for debug only:
            raise Exception("Web-scraper error in get_webpage_page_html fn... error code is: {errcode}; error reason is: {errreason} at url: {url}\n".format(
                errcode=response.status_code, errreason=response.reason, url=url))
        return response
    
    except Exception as e:
        # for debug only:
        # with open("./web-scraper-logs/error.txt", "a+") as error_file:
        #     error_file.write(str(e))
        return response
    
def convert_html_to_soup_obj(html: requests.Response):
    html_string = html.text    
    # html_soup = BeautifulSoup(html_string, "html.parser")
    html_soup = BeautifulSoup(html_string, "lxml")
    return html_soup

def convert_soup_to_text(html_soup: BeautifulSoup):
    html_text_content = html_soup.get_text(strip=True)
    return html_text_content

def extract_page_title_as_text(html_soup: BeautifulSoup):
    html_page_title = html_soup.head.title.string
    return html_page_title + "\n"

def extract_and_format_main_content_as_text(html_soup: BeautifulSoup, rule: int):
    main_content = []

    if(rule == 1):
        tag_rule = re.compile("^(h[1-6]|p|div)") # it'll only be called when the webpage is very non-standard
    else:
        tag_rule = re.compile("^(h[1-6]|p)") # default rule

    # Only the <h1-h6> and <p> tags in an HTML are extracted:
    for tag in html_soup.find_all(tag_rule):
        tag_text = tag.get_text()
        tag_text = tag_text.lstrip().rstrip()

        # Filter out too short content:
        if (tag_text and len(tag_text.split()) > 10):
            main_content.append(tag_text)

    main_content_text = "\n".join(main_content)
    main_content_text = re.sub("\n{2,}", "\n", main_content_text) # remove consecutive blank lines

    return main_content_text

def extract_time_stamp(html_soup: BeautifulSoup):
    time_tag = html_soup.find("time")

    if time_tag:
        time_stamp = time_tag.get("datetime")
        # datetime_obj = datetime.fromisoformat(time_stamp)
        return time_stamp
    else:
        return None

def extract_page_contents(url: str, rule: int):
    webpage_html = get_webpage_html(url)
    soup = convert_html_to_soup_obj(webpage_html)
    main_content = extract_and_format_main_content_as_text(soup, rule)
    time_stamp = extract_time_stamp(soup)
    return main_content, time_stamp

# Testing this code:
if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/Apple_Inc." # note this site requires a VPN
    main_content, time_stamp = extract_page_contents(test_url, 0)
    
    print(main_content)
    print(time_stamp)
    