---
slug: "semantic-search-cwicr"
display_name: "Semantic Search CWICR"
description: "在 DDC CWICR 构建数据库中，使用向量嵌入技术进行语义搜索。通过该技术可以找到用于成本估算的相似工作项和资源。"
---

# DDC CWICR 数据库中的语义搜索

## 商业场景

### 问题描述
在估算建筑成本时，需要从庞大的数据库中查找相关的工作项。传统的关键词搜索方法存在以下问题：
- 用户使用自然语言描述工作内容时，搜索效果不佳；
- 不同地区和语言之间的术语存在差异；
- 相似的工作项可能有不同的命名规范。

### 解决方案
DDC CWICR 数据库提供了预计算好的嵌入向量（使用 OpenAI 的 text-embedding-3-large 模型，维度为 3072），支持在 9 种语言中对 55,719 个工作项进行语义相似性搜索。

### 商业价值
- **搜索速度提升 90%**：相比手动搜索，查询速度更快；
- **多语言支持**：支持阿拉伯语、中文、德语、英语、西班牙语、法语、印地语、葡萄牙语和俄语；
- **更高的搜索准确性**：能够找到语义上相似的工作项，而不仅仅是关键词匹配的结果。

## 技术实现

### 先决条件
```bash
pip install qdrant-client openai pandas
```

### 数据库配置
```bash
# Download Qdrant snapshot
wget https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR/releases/download/v0.1.0/qdrant_snapshot_en.tar.gz

# Start Qdrant with Docker
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

### Python 实现
```python
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import openai

class CWICRSemanticSearch:
    def __init__(self, qdrant_host: str = "localhost", port: int = 6333):
        self.client = QdrantClient(host=qdrant_host, port=port)
        self.collection_name = "ddc_cwicr_en"
        self.embedding_model = "text-embedding-3-large"
        self.embedding_dim = 3072

    def get_embedding(self, text: str) -> list:
        """Generate embedding for search query."""
        response = openai.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def search_work_items(self, query: str, limit: int = 10,
                          min_score: float = 0.7) -> pd.DataFrame:
        """Search for similar work items."""
        query_vector = self.get_embedding(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=min_score
        )

        items = []
        for result in results:
            item = result.payload
            item['similarity_score'] = result.score
            items.append(item)

        return pd.DataFrame(items)

    def search_by_category(self, query: str, category: str,
                           limit: int = 10) -> pd.DataFrame:
        """Search within specific category."""
        query_vector = self.get_embedding(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter={
                "must": [{"key": "category", "match": {"value": category}}]
            },
            limit=limit
        )

        return pd.DataFrame([{**r.payload, 'score': r.score} for r in results])

    def estimate_cost(self, work_items: pd.DataFrame,
                      quantities: dict) -> dict:
        """Calculate cost from matched work items."""
        total_cost = 0
        breakdown = []

        for _, item in work_items.iterrows():
            if item['work_item_code'] in quantities:
                qty = quantities[item['work_item_code']]
                cost = qty * item.get('unit_price', 0)
                total_cost += cost
                breakdown.append({
                    'item': item['description'],
                    'quantity': qty,
                    'unit_price': item.get('unit_price', 0),
                    'total': cost
                })

        return {
            'total_cost': total_cost,
            'breakdown': breakdown,
            'currency': 'Regional default'
        }
```

## 使用示例

### 基本搜索
```python
search = CWICRSemanticSearch()

# Natural language query
results = search.search_work_items("brick masonry wall construction")
print(results[['description', 'unit', 'unit_price', 'similarity_score']])
```

### 成本估算
```python
# Find work items for foundation work
foundation_items = search.search_work_items(
    "reinforced concrete foundation excavation and pouring",
    limit=20
)

# Estimate with quantities
quantities = {
    'CONC-001': 150,  # cubic meters
    'EXCV-002': 200,  # cubic meters
}
estimate = search.estimate_cost(foundation_items, quantities)
print(f"Estimated Cost: ${estimate['total_cost']:,.2f}")
```

## 数据库架构

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| work_item_code | string | 唯一标识符 |
| description | string | 工作项描述 |
| unit | string | 计量单位 |
| labor_norm | float | 每单位的劳动时间 |
| material_cost | float | 每单位的材料成本 |
| equipment_cost | float | 每单位的设备成本 |
| unit_price | float | 每单位的总价格 |
| category | string | 工作类别 |
| embedding | vector[3072] | 预计算得到的嵌入向量 |

## 最佳实践
1. **使用具体的查询条件**：例如 “reinforced concrete slab 200mm” 比 “concrete” 更能提高搜索精度；
2. **按类别筛选**：将搜索结果限制在相关的工作类型范围内；
3. **检查相似度得分**：得分低于 0.7 的结果可能需要人工验证；
4. **与工程量清单（QTO）结合使用**：结合 BIM 数据进行自动化成本估算。

## 资源
- **GitHub 项目**：[OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **版本信息**：[v0.1.0 数据库下载链接](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR/releases)
- **Qdrant 文档**：https://qdrant.tech/documentation/