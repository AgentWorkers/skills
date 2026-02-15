---
slug: "vector-search"
display_name: "Vector Search"
description: "为建筑数据实现语义向量搜索功能。利用嵌入技术和向量数据库（如 Qdrant、ChromaDB）构建基于人工智能的搜索系统，以实现对规范、标准和项目文档的智能查询。"
---

# 建筑领域的向量搜索技术

## 概述

本技术基于DDC方法论（第4.4章）实现了对建筑相关数据的语义向量搜索功能。它超越了简单的关键词匹配，能够根据数据的实际含义来查找文档和信息，而不仅仅是基于文字内容。

**参考书籍**：《Современные технологии работы с данными》（《现代数据技术》）

> “向量数据库能够找到在语义上相似的文档，即使这些文档使用了不同的术语。”  
> — DDC书籍，第4.4章

## 快速入门

```python
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create Qdrant client (in-memory for demo)
client = QdrantClient(":memory:")

# Create collection
client.create_collection(
    collection_name="construction_docs",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Sample construction documents
documents = [
    "Concrete mix design for C30 grade with water-cement ratio 0.45",
    "Steel reinforcement specifications for structural columns",
    "Waterproofing membrane installation for basement walls",
    "Fire-rated door specifications for escape routes"
]

# Index documents
for idx, doc in enumerate(documents):
    embedding = model.encode(doc).tolist()
    client.upsert(
        collection_name="construction_docs",
        points=[PointStruct(id=idx, vector=embedding, payload={"text": doc})]
    )

# Search
query = "basement moisture protection"
query_vector = model.encode(query).tolist()
results = client.search(
    collection_name="construction_docs",
    query_vector=query_vector,
    limit=3
)

for result in results:
    print(f"Score: {result.score:.3f} - {result.payload['text']}")
```

## 向量数据库的设置

### Qdrant的设置

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct,
    Filter, FieldCondition, MatchValue
)
import uuid

class ConstructionVectorDB:
    """Vector database for construction documents and data"""

    def __init__(self, host="localhost", port=6333, in_memory=False):
        if in_memory:
            self.client = QdrantClient(":memory:")
        else:
            self.client = QdrantClient(host=host, port=port)

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collections = {}

    def create_collection(self, name, description=None):
        """Create a new collection"""
        self.client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=384,  # Dimension for all-MiniLM-L6-v2
                distance=Distance.COSINE
            )
        )
        self.collections[name] = description

    def index_documents(self, collection_name, documents, metadata=None):
        """Index documents with embeddings"""
        points = []

        for idx, doc in enumerate(documents):
            embedding = self.model.encode(doc).tolist()

            payload = {"text": doc}
            if metadata and idx < len(metadata):
                payload.update(metadata[idx])

            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload
            ))

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

        return len(points)

    def search(self, collection_name, query, limit=5, filters=None):
        """Semantic search"""
        query_vector = self.model.encode(query).tolist()

        search_filter = None
        if filters:
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filters.items()
            ]
            search_filter = Filter(must=conditions)

        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=search_filter
        )

        return [
            {
                'score': r.score,
                'text': r.payload.get('text'),
                'metadata': {k: v for k, v in r.payload.items() if k != 'text'}
            }
            for r in results
        ]

    def hybrid_search(self, collection_name, query, keyword_filter=None, limit=5):
        """Combine semantic search with keyword filtering"""
        # First semantic search
        semantic_results = self.search(collection_name, query, limit=limit*2)

        # Then keyword filter if provided
        if keyword_filter:
            filtered = [
                r for r in semantic_results
                if keyword_filter.lower() in r['text'].lower()
            ]
            return filtered[:limit]

        return semantic_results[:limit]
```

### ChromaDB的替代方案

```python
import chromadb
from chromadb.utils import embedding_functions

class ChromaConstructionDB:
    """ChromaDB-based vector search for construction"""

    def __init__(self, persist_directory=None):
        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.Client()

        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

    def create_collection(self, name):
        """Create or get collection"""
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=self.embedding_fn
        )

    def index_specifications(self, collection_name, specs):
        """Index construction specifications"""
        collection = self.create_collection(collection_name)

        ids = [f"spec_{i}" for i in range(len(specs))]
        documents = [s['text'] for s in specs]
        metadatas = [{k: v for k, v in s.items() if k != 'text'} for s in specs]

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        return len(specs)

    def search(self, collection_name, query, n_results=5, where=None):
        """Search specifications"""
        collection = self.create_collection(collection_name)

        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

        return [
            {
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i] if results['distances'] else None
            }
            for i in range(len(results['ids'][0]))
        ]
```

## 建筑领域特定的应用

### 规范搜索

```python
class SpecificationSearchEngine:
    """Search engine for construction specifications"""

    def __init__(self, db: ConstructionVectorDB):
        self.db = db
        self.collection = "specifications"

    def index_specifications(self, specs_df):
        """Index specifications from DataFrame"""
        self.db.create_collection(self.collection, "Construction specifications")

        documents = specs_df['description'].tolist()
        metadata = specs_df.drop('description', axis=1).to_dict('records')

        return self.db.index_documents(self.collection, documents, metadata)

    def find_similar_specs(self, query, category=None, limit=5):
        """Find similar specifications"""
        filters = {'category': category} if category else None
        return self.db.search(self.collection, query, limit=limit, filters=filters)

    def find_related_materials(self, material_name, limit=10):
        """Find specifications related to a material"""
        query = f"specifications for {material_name} materials"
        return self.db.search(self.collection, query, limit=limit)

    def search_by_requirement(self, requirement, limit=5):
        """Search by performance requirement"""
        query = f"specification meeting requirement: {requirement}"
        return self.db.search(self.collection, query, limit=limit)
```

### 标准和代码搜索

```python
class StandardsSearchEngine:
    """Search engine for building standards and codes"""

    def __init__(self, db: ConstructionVectorDB):
        self.db = db
        self.collection = "standards"

    def index_standards(self, standards):
        """Index building standards

        Args:
            standards: List of dicts with 'code', 'title', 'section', 'text'
        """
        self.db.create_collection(self.collection, "Building standards and codes")

        documents = [s['text'] for s in standards]
        metadata = [{k: v for k, v in s.items() if k != 'text'} for s in standards]

        return self.db.index_documents(self.collection, documents, metadata)

    def find_applicable_standards(self, context, limit=5):
        """Find standards applicable to a given context"""
        return self.db.search(self.collection, context, limit=limit)

    def search_fire_codes(self, query):
        """Search fire safety codes"""
        full_query = f"fire safety code requirement: {query}"
        return self.db.search(
            self.collection,
            full_query,
            limit=10,
            filters={'category': 'fire_safety'}
        )

    def search_accessibility(self, query):
        """Search accessibility standards (ADA, etc.)"""
        full_query = f"accessibility requirement: {query}"
        return self.db.search(
            self.collection,
            full_query,
            limit=10,
            filters={'category': 'accessibility'}
        )
```

### 工作项搜索（OpenConstructionEstimate）

```python
class WorkItemSearchEngine:
    """Search engine for construction work items and unit prices"""

    def __init__(self, db: ConstructionVectorDB):
        self.db = db
        self.collection = "work_items"

    def index_work_items(self, items_df):
        """Index work items database

        Args:
            items_df: DataFrame with columns:
                - code: Work item code
                - description: Work description
                - unit: Unit of measure
                - unit_price: Price per unit
                - category: Work category
        """
        self.db.create_collection(self.collection, "Construction work items")

        documents = items_df['description'].tolist()
        metadata = items_df.drop('description', axis=1).to_dict('records')

        return self.db.index_documents(self.collection, documents, metadata)

    def find_similar_work(self, description, limit=10):
        """Find similar work items by description"""
        results = self.db.search(self.collection, description, limit=limit)

        return [
            {
                'description': r['text'],
                'code': r['metadata'].get('code'),
                'unit': r['metadata'].get('unit'),
                'unit_price': r['metadata'].get('unit_price'),
                'similarity': r['score']
            }
            for r in results
        ]

    def estimate_from_description(self, work_description, quantity):
        """Get cost estimate from work description"""
        matches = self.find_similar_work(work_description, limit=3)

        if not matches:
            return None

        best_match = matches[0]
        unit_price = best_match.get('unit_price', 0)

        return {
            'matched_item': best_match['description'],
            'code': best_match['code'],
            'unit': best_match['unit'],
            'unit_price': unit_price,
            'quantity': quantity,
            'total_cost': unit_price * quantity,
            'similarity_score': best_match['similarity']
        }
```

## 建筑领域的RAG（Retrieval Augmented Generation，检索增强生成）

### 文档索引流程

```python
import os
import pdfplumber
from typing import List, Dict

class DocumentIndexingPipeline:
    """Pipeline for indexing construction documents"""

    def __init__(self, vector_db: ConstructionVectorDB):
        self.db = vector_db
        self.chunk_size = 500
        self.chunk_overlap = 50

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            if len(chunk) > 50:  # Skip very small chunks
                chunks.append(chunk)

        return chunks

    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def index_document(self, file_path: str, collection: str, metadata: Dict = None):
        """Index a single document"""
        # Extract text
        if file_path.endswith('.pdf'):
            text = self.extract_pdf_text(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

        # Chunk text
        chunks = self.chunk_text(text)

        # Build metadata for each chunk
        base_metadata = metadata or {}
        base_metadata['source_file'] = os.path.basename(file_path)

        chunk_metadata = [
            {**base_metadata, 'chunk_index': i}
            for i in range(len(chunks))
        ]

        # Index
        return self.db.index_documents(collection, chunks, chunk_metadata)

    def index_directory(self, directory: str, collection: str, extensions=None):
        """Index all documents in a directory"""
        if extensions is None:
            extensions = ['.pdf', '.txt', '.md']

        total_indexed = 0

        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        count = self.index_document(file_path, collection)
                        total_indexed += count
                        print(f"Indexed: {file} ({count} chunks)")
                    except Exception as e:
                        print(f"Error indexing {file}: {e}")

        return total_indexed
```

## 快速参考

| 组件 | 描述 | 使用场景 |
|-----------|-------------|----------|
| Qdrant | 高性能向量数据库 | 生产环境部署 |
| ChromaDB | 简单的嵌入式向量数据库 | 开发/测试 |
| SentenceTransformers | 嵌入式模型 | 将文本转换为向量 |
| RAG | 检索 + 生成 | 基于文档的问答系统 |

## 建筑领域的嵌入模型

```python
# Recommended models by use case
EMBEDDING_MODELS = {
    'general': 'all-MiniLM-L6-v2',           # Fast, 384 dim
    'multilingual': 'paraphrase-multilingual-MiniLM-L12-v2',  # Multi-language
    'quality': 'all-mpnet-base-v2',          # Better quality, 768 dim
    'construction': 'allenai/scibert_scivocab_uncased'  # Technical texts
}
```

## 资源推荐

- **书籍**：Artem Boiko所著的《Data-Driven Construction》，第4.4章
- **网站**：https://datadrivenconstruction.io
- **Qdrant**：https://qdrant.tech
- **ChromaDB**：https://www.trychroma.com
- **SentenceTransformers**：https://www.sbert.net

## 下一步操作

- 请参阅`llm-data-automation`以了解大语言模型（LLM）的集成方法
- 请参阅`document-classification-nlp`以了解文档分类技术
- 请参阅`rag-construction`以了解RAG（检索增强生成）的应用