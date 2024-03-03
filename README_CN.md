集成实时网页浏览功能的 GPT-4
========================

Languages / 语言: [中文](https://github.com/Wilson-ZheLin/GPT-4-Web-Browsing/blob/main/README_CN.md) | [English](https://github.com/Wilson-ZheLin/GPT-4-Web-Browsing)

GPT-4的知识库涉及领域丰富、涵盖范围广泛，但是一直有一定的实效滞后，例如最新的GPT-4知识更新截止于2023年4月。为了解决这个限制，我们将实时的网络浏览集成到了 GPT-4 中，将具有时效性的信息结合大语言模型先进的语言处理能力，并且速度要快于网页端 GPT-4 自带的网络浏览。🔗

您可以将这个项目看作 `new Bing` 和 `Bard` 的一个小型实现，结合了Q&A和搜索引擎的能力。🌟

功能
---
* 通过 [Serper (Google API)](https://serper.dev) 进行快速实时网络搜索

* 根据输入自动调整 **搜索地区** 和 **响应语言**

* **多线程** 提取网页主体内容，减少 token 数量的花费

* 使用 [OpenAI Embedding](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings) 和 [ChromaDB](https://www.trychroma.com) 进行语义搜索

* LLM 生成的响应中附带参考列表和网络信息的来源

* 支持自定义[模型](https://platform.openai.com/docs/models)，**AI的角色**，和**输出格式**

* 将 LLM 响应中的每个引用句子与源网站的**标题**、**摘要**和**链接**匹配


架构&流程
--------

![Project Architecture](https://github.com/Wilson-ZheLin/GPT-4-Web-Browsing/assets/145169519/d313835d-5b57-4391-8b79-be81fdd4fa8a)

运行效果
-------

https://github.com/Wilson-ZheLin/GPT-4-Web-Browsing/assets/145169519/6406d20c-efec-4cb9-ad51-510f51ce5212


安装
----

### 环境&前置准备

运行 `main.py` 或者 `llm_answer.py`, 首先需要:
* 稳定的网络连接可以访问到 OpenAI
* [Python 3.11.5](https://www.python.org/downloads/) (不一定完全相同)
* [Serper API Key](https://serper.dev)
    * Serper: 提供 2,500 次免费查询（额度充足且响应快速）
* [OpenAI API Key](https://openai.com/blog/openai-api)
    * OpenAI: 新帐户包含 $5 的免费额度 (推荐使用 GPT-3.5-turbo-16k)
    
### 安装和运行
1. 安装所需的依赖包 (中国大陆可以附加 `-i https://pypi.tuna.tsinghua.edu.cn/simple`):

```
pip install -r requirements.txt
```

2. 保存你的 **API Keys** 到 `config.yaml`

3. 运行 `main.py` 或者 `llm_answer.py`, 查询关键词可以在这两个文件中修改

