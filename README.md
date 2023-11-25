GPT-4 Enhanced with Real-Time Web Browsing
==========================================

GPT-4's extensive knowledge base covers a wide range of topics but is limited to historical data. To address this, we've integrated web browsing into GPT-4, connecting its advanced language processing to the internet. 

This upgrade enables access to the latest information, enhancing the model's relevance and efficiency in real-time data retrieval, and is much faster than web-browsing on the GPT web page.

You may consider this as a tiny implementation of the **new Bing** and **Bard**, primarily for search engines and Q&A.

Please give me a star if you like it! 🌟

Features
--------
* Rapid real-time web search through [Serper (Google API)](https://serper.dev)

* Automatically adjusts web search and response **language** based on input

* Multi-threading to extract main content from web pages, reducing embedding costs

* Semantic search with [OpenAI Embedding](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings) and [ChromaDB](https://www.trychroma.com)

* LLM responses generated with references and web sources

* Supports customization of models, AI roles, and output formats

* Matches each quoted sentence in the AI’s response to the **title, snippet, and link of the source website**


Demo
----


Architecture
------------


Getting Started
---------------

### Prerequisites

To run `main.py` or `llm_answer.py`, you'll need:
* Stable connection to OpenAI (may be instability in China)
* [Python 3.11.5](https://www.python.org/downloads/) (not necessarily the same)
* [Serper API Key](https://serper.dev)
    * Serper: 2,500 free queries (very adequate and fast)
* [OpenAI API Key](https://openai.com/blog/openai-api)
    * OpenAI: First $5 is free (GPT-3.5-turbo-16k  recommended)
    
### Installation
1. Install the required packages (consider adding `-i https://pypi.tuna.tsinghua.edu.cn/simple` in China):

```
pip install -r requirements.txt
```

2. Save your **API Keys** in `config.yaml`

3. run `main.py` or `llm_answer.py`, where you can change the query

License
-------

This project is licensed under the [MIT License](./LICENSE).
