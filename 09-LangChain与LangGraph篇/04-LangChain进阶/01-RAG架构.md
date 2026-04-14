# 09.04.01 - RAG 架构

**RAG (Retrieval-Augmented Generation)：** 检索增强生成，结合文档检索和 LLM 生成答案。

```
RAG 架构：
┌──────────────────────────────────────┐
│  文档 → 分块 → Embedding → Vector Store │
│                                       │
│  用户问题 → Retriever → 相关文档       │
│           ↓                           │
│  文档 + 问题 → LLM → 答案              │
└──────────────────────────────────────┘
```

### 为什么用它？

LLM 只知道预训练知识，无法回答：
- 公司内部文档
- 最新产品信息
- 实时数据

RAG 通过检索相关文档，让 LLM 基于最新信息回答。

---

### RAG 流程

```
RAG 流程：
┌──────────────────────────────────────┐
│  1. 加载文档 (Document Loader)        │
│  2. 分块 (Text Splitter)              │
│  3. 向量化 (Embeddings)               │
│  4. 存储 (Vector Store)               │
│  5. 检索 (Retriever)                  │
│  6. 生成 (LLM)                        │
└──────────────────────────────────────┘
```

### 最简示例：文档加载

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = TextLoader("docs/readme.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,    # 每块最大字符
    chunk_overlap=50,  # 块间重叠
)
chunks = splitter.split_documents(documents)

print(f"文档数: {len(documents)}, 分块数: {len(chunks)}")
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `TextLoader` | 文本文件加载器 | 简单易用 |
| `chunk_size=500` | 每块最大字符 | 平衡检索精度和上下文长度 |
| `chunk_overlap=50` | 块间重叠 | 防止信息被切断 |

---

### 详细示例：完整 RAG

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.messages import HumanMessage, SystemMessage

# 第一步：加载和分块文档
loader = TextLoader("docs/python_basics.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 第二步：创建向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 第三步：创建检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 第四步：检索相关文档
query = "什么是列表？"
relevant_docs = retriever.invoke(query)

# 第五步：生成答案
model = ChatOpenAI(model="gpt-4o-mini")
context = "\n".join([doc.page_content for doc in relevant_docs])

messages = [
    SystemMessage("根据以下文档回答问题：\n" + context),
    HumanMessage(query),
]

response = model.invoke(messages)
print(response.content)
```

---

### Document Loader 类型

```
Document Loader：
┌──────────────────────────────────────┐
│  TextLoader      → 文本文件           │
│  PDFLoader       → PDF 文档           │
│  WebBaseLoader   → 网页内容           │
│  JSONLoader      → JSON 文件          │
│  DirectoryLoader → 目录批量加载       │
└──────────────────────────────────────┘
```

---

### Vector Store 类型

```
Vector Store：
┌──────────────────────────────────────┐
│  Chroma    → 本地向量数据库           │
│  FAISS     → Facebook 向量检索        │
│  Pinecone  → 云向量数据库             │
│  Weaviate  → 开源向量数据库           │
└──────────────────────────────────────┘
```