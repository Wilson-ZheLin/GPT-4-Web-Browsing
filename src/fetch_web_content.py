import threading
import time
import os
from web_crawler import extract_page_contents
from serper_service import serper, extract_components_from_serper

def fetch_web_content(query: str):

    # 定义每个线程的最大重试次数
    MAX_RETRIES = 1

    # 创建一个锁，用于在多线程中安全地操作共享的结果列表
    web_contents_lock = threading.Lock()
    web_contents = []

    # 创建一个锁，用于在多线程中安全地操作共享的错误URL列表
    error_urls_lock = threading.Lock()
    error_urls = []

    def web_crawler_thread(thread_id: int, urls: list):
        # Initialize the logger:
        # logging.basicConfig(level=logging.INFO)
        # logger = logging.getLogger(__name__)
        attempts = 0
        while attempts < MAX_RETRIES:
            try:
                print("Starting web crawler thread {}".format(thread_id))
                start_time = time.time()  # mark start time

                url = urls[thread_id]  # get the current url

                # Call the web-crawler functions:
                content_from_one_page, time_stamp = extract_page_contents(url, 0)

                # If the length is too short, the webpage is very non-standard
                if (0 < len(content_from_one_page) < 800):
                    content_from_one_page, time_stamp = extract_page_contents(url, 1)  # extend the crawl rules

                # 如果成功获取内容并且满足条件，将结果添加到共享列表
                if len(content_from_one_page) > 300:
                    with web_contents_lock:
                        web_contents.append({"url": url, "content": content_from_one_page, "time": time_stamp if time_stamp is not None else ""})
                    end_time = time.time()  # mark end time
                    print("Thread {} completed! Time comsumed: {}s".format(thread_id, end_time - start_time))
                    break  # 跳出重试循环
                else:
                    time.sleep(1)  # 等待2秒后重试
                    attempts += 1

            except Exception as e:
                # 如果发生异常，记录错误URL并等待一段时间后重试
                with error_urls_lock:
                    error_urls.append(url)
                print(f"Thread {thread_id}: Error crawling {url}: {e}")
                time.sleep(2)  # 等待2秒后重试
                attempts += 1

            # If the length is too short, the webpage content may not be obtained properly
            #if (0 < len(content_from_one_page) < 800):
            #    content_from_one_page = unstructured_crawler(url)  # call the backup crawler

            # Acquire the lock to safely append the result to the shared list
            #with lock:
            #    if (len(content_from_one_page) > 300):
            #        web_contents.append({"url": url, "content": content_from_one_page})

    def serper_launcher(query: str):

        # 定义一个函数来执行任务
        def perform_serper_task(query):
            try:
                serper_results = serper(query)
                return serper_results  # 如果成功，返回结果
            except Exception as e:
                print(f"Serper API 执行错误：{e}")
                return None  # 如果失败，返回None

        # 循环尝试执行任务直到成功或达到最大尝试次数
        attempts = 0
        while attempts < MAX_RETRIES:
            serper_results = perform_serper_task(query)
            if serper_results is not None:
                # 如果成功，跳出循环
                break
            else:
                # 如果失败，等待一段时间后重试
                attempts += 1
                time.sleep(1)  # 等待2秒后重试

        if serper_results is not None:
            # 在这里可以继续处理成功的结果
            serper_response = extract_components_from_serper(serper_results)
        else:
            print("达到最大尝试次数，任务仍然失败。")

        return serper_response

    def crawl_threads_launcher(url_list: list):
        
        # Create and start threads:
        threads = []

        for i in range(len(url_list)):
            thread = threading.Thread(target=web_crawler_thread, args=(i, url_list))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    serper_response = serper_launcher(query)
    url_list = serper_response["links"]
    crawl_threads_launcher(url_list) # this line updates the "web_contents" list

    # 下面这行代码可能有点长，它是把爬到内容list的顺序按照「Serper返回url的顺序」排列了一下
    # next是为了留空没有爬到到网页的位置，以保证网页内容的顺序与url_list的严格一致
    ordered_contents = [next((single_page['content'] for single_page in web_contents if single_page['url'] == url), '') for url in url_list]
    # 对网页的时间戳同理：
    ordered_time = [next((single_page['time'] for single_page in web_contents if single_page['url'] == url), '') for url in url_list]
    serper_response['time'] = ordered_time

    return ordered_contents, serper_response

# Testing this code:
if __name__ == "__main__":
    query = "Tencent Games Global Market Share"
    # query = "Tell me about the recent trends in cryptocurrency prices."
    web_contents, serper_response = fetch_web_content(query)
    
    # print("当前工作目录:", os.getcwd())  # 打印当前工作目录
    print(web_contents, '\n\n')
    print(serper_response)

    #with open("web_contents.txt", "w", encoding="utf-8") as file:
    #    file.write("Query: " + query + "\n\n\n")
    #    for i in range(len(results)):
    #        file.write("Website " + str(i) + ": "+results[i]["url"] + "\n\n" + results[i]["content"] + "\n\n\n")
