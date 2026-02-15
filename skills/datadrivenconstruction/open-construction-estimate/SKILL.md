---
name: "open-construction-estimate"
description: "访问并使用开放的建筑工程定价数据库。将 BIM 元素与标准化的工作项进行匹配，利用包含 55,000 多个工作项的公共单价数据库来计算成本。"
---

# 开源建筑估算工具

## 概述

该工具利用开源的建筑定价数据库来实现自动成本估算。通过将项目元素与标准化的工种进行匹配，并使用公开可用的单价来计算成本。

**数据来源：**
- OpenConstructionEstimate（包含55,000多个工种）
- RSMeans Online（需订阅）
- 政府定价数据库
- 地区成本指数

> “这些开源的定价数据库包含了超过55,000个工种的信息，能够为大多数项目实现自动化的预算编制。”
> — DDC LinkedIn

## 快速入门

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load work items database
work_items = pd.read_csv("open_construction_estimate.csv")
print(f"Loaded {len(work_items)} work items")

# Simple matching function
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
item_vectors = vectorizer.fit_transform(work_items['description'])

def find_matching_items(query, top_n=5):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, item_vectors)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]

    return work_items.iloc[top_indices][['code', 'description', 'unit', 'unit_price']]

# Find matches
matches = find_matching_items("reinforced concrete wall 300mm")
print(matches)
```

## 开源数据库结构

### 数据库模式

```python
# Standard work items database structure
WORK_ITEMS_SCHEMA = {
    'code': 'Work item code (e.g., 03.31.13.13)',
    'description': 'Full description of work',
    'short_description': 'Abbreviated description',
    'unit': 'Unit of measure (m³, m², ton, pcs)',
    'unit_price': 'Base unit price',
    'labor_cost': 'Labor component per unit',
    'material_cost': 'Material component per unit',
    'equipment_cost': 'Equipment component per unit',
    'labor_hours': 'Labor hours per unit',
    'crew_size': 'Typical crew size',
    'productivity': 'Units per day',
    'category_l1': 'Primary category (CSI Division)',
    'category_l2': 'Secondary category',
    'category_l3': 'Detailed category',
    'region': 'Geographic region',
    'year': 'Price year',
    'source': 'Data source'
}

# CSI MasterFormat Divisions
CSI_DIVISIONS = {
    '03': 'Concrete',
    '04': 'Masonry',
    '05': 'Metals',
    '06': 'Wood, Plastics, Composites',
    '07': 'Thermal and Moisture Protection',
    '08': 'Openings',
    '09': 'Finishes',
    '10': 'Specialties',
    '21': 'Fire Suppression',
    '22': 'Plumbing',
    '23': 'HVAC',
    '26': 'Electrical',
    '31': 'Earthwork',
    '32': 'Exterior Improvements',
    '33': 'Utilities'
}
```

## 工种匹配引擎

### 语义匹配系统

```python
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Tuple
import re

class WorkItemMatcher:
    """Match BIM elements to standardized work items"""

    def __init__(self, database_path: str, use_embeddings: bool = True):
        self.db = pd.read_csv(database_path)

        # TF-IDF for fast initial filtering
        self.tfidf = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=10000,
            stop_words='english'
        )
        self.tfidf_matrix = self.tfidf.fit_transform(self.db['description'])

        # Sentence embeddings for semantic matching
        self.use_embeddings = use_embeddings
        if use_embeddings:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            self.embeddings = self.embedder.encode(
                self.db['description'].tolist(),
                show_progress_bar=True
            )

    def match(self, query: str, top_n: int = 5,
              category: str = None) -> List[Dict]:
        """Find matching work items for a query"""
        # Filter by category if specified
        if category:
            mask = self.db['category_l1'].str.contains(category, case=False, na=False)
            search_db = self.db[mask]
            search_matrix = self.tfidf_matrix[mask]
        else:
            search_db = self.db
            search_matrix = self.tfidf_matrix

        if self.use_embeddings:
            return self._semantic_match(query, search_db, top_n)
        else:
            return self._tfidf_match(query, search_db, search_matrix, top_n)

    def _tfidf_match(self, query: str, db: pd.DataFrame,
                     matrix, top_n: int) -> List[Dict]:
        """TF-IDF based matching"""
        query_vec = self.tfidf.transform([query])
        similarities = cosine_similarity(query_vec, matrix)[0]

        top_indices = similarities.argsort()[-top_n:][::-1]

        results = []
        for idx in top_indices:
            row = db.iloc[idx]
            results.append({
                'code': row['code'],
                'description': row['description'],
                'unit': row['unit'],
                'unit_price': row['unit_price'],
                'similarity': float(similarities[idx]),
                'category': row.get('category_l1', '')
            })

        return results

    def _semantic_match(self, query: str, db: pd.DataFrame,
                        top_n: int) -> List[Dict]:
        """Semantic embedding based matching"""
        query_embedding = self.embedder.encode([query])

        # Get indices for filtered db
        indices = db.index.tolist()
        filtered_embeddings = self.embeddings[indices]

        similarities = cosine_similarity(query_embedding, filtered_embeddings)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]

        results = []
        for i, idx in enumerate(top_indices):
            row = db.iloc[idx]
            results.append({
                'code': row['code'],
                'description': row['description'],
                'unit': row['unit'],
                'unit_price': row['unit_price'],
                'similarity': float(similarities[idx]),
                'category': row.get('category_l1', '')
            })

        return results

    def match_bim_element(self, element: Dict) -> List[Dict]:
        """Match a BIM element to work items"""
        # Build query from element properties
        query_parts = []

        if element.get('material'):
            query_parts.append(element['material'])
        if element.get('category'):
            query_parts.append(element['category'])
        if element.get('description'):
            query_parts.append(element['description'])

        # Add dimensions if available
        if element.get('thickness'):
            query_parts.append(f"{element['thickness']}mm thick")
        if element.get('height'):
            query_parts.append(f"{element['height']}m high")

        query = ' '.join(query_parts)

        # Determine category from element type
        category = self._get_category_from_element(element)

        return self.match(query, top_n=3, category=category)

    def _get_category_from_element(self, element: Dict) -> Optional[str]:
        """Map BIM element type to CSI category"""
        element_mapping = {
            'IfcWall': 'Concrete|Masonry',
            'IfcSlab': 'Concrete',
            'IfcColumn': 'Concrete|Metals',
            'IfcBeam': 'Concrete|Metals',
            'IfcDoor': 'Openings',
            'IfcWindow': 'Openings',
            'IfcRoof': 'Thermal',
            'IfcStair': 'Concrete',
            'IfcPipeSegment': 'Plumbing',
            'IfcDuctSegment': 'HVAC'
        }

        elem_type = element.get('ifc_type', '')
        return element_mapping.get(elem_type)
```

## 成本估算引擎

### 自动估算器

```python
class OpenConstructionEstimator:
    """Generate cost estimates using open databases"""

    def __init__(self, matcher: WorkItemMatcher, region: str = 'default'):
        self.matcher = matcher
        self.region = region
        self.regional_factors = self._load_regional_factors()
        self.estimates = []

    def _load_regional_factors(self) -> Dict[str, float]:
        """Load regional cost adjustment factors"""
        return {
            'default': 1.0,
            'northeast_us': 1.15,
            'southeast_us': 0.92,
            'midwest_us': 0.95,
            'west_us': 1.08,
            'moscow': 1.20,
            'spb': 1.10,
            'regions_ru': 0.85
        }

    def estimate_element(self, element: Dict) -> Dict:
        """Estimate cost for a single element"""
        # Get matching work items
        matches = self.matcher.match_bim_element(element)

        if not matches:
            return {
                'element_id': element.get('id'),
                'status': 'no_match',
                'estimated_cost': 0
            }

        best_match = matches[0]
        quantity = element.get('quantity', 1)
        unit_price = best_match['unit_price']

        # Apply regional factor
        regional_factor = self.regional_factors.get(self.region, 1.0)
        adjusted_price = unit_price * regional_factor

        # Calculate total
        total_cost = adjusted_price * quantity

        estimate = {
            'element_id': element.get('id'),
            'element_type': element.get('ifc_type'),
            'element_description': element.get('description', ''),
            'matched_code': best_match['code'],
            'matched_description': best_match['description'],
            'match_confidence': best_match['similarity'],
            'unit': best_match['unit'],
            'quantity': quantity,
            'unit_price': unit_price,
            'regional_factor': regional_factor,
            'adjusted_unit_price': adjusted_price,
            'total_cost': total_cost
        }

        self.estimates.append(estimate)
        return estimate

    def estimate_project(self, elements: List[Dict]) -> Dict:
        """Estimate entire project"""
        for element in elements:
            self.estimate_element(element)

        df = pd.DataFrame(self.estimates)

        # Summary by category
        if not df.empty:
            summary = df.groupby('element_type').agg({
                'total_cost': 'sum',
                'element_id': 'count',
                'match_confidence': 'mean'
            }).rename(columns={'element_id': 'count'})
        else:
            summary = pd.DataFrame()

        total = df['total_cost'].sum() if not df.empty else 0

        return {
            'total_cost': total,
            'element_count': len(elements),
            'matched_count': len(df[df['match_confidence'] > 0.5]) if not df.empty else 0,
            'summary_by_type': summary.to_dict() if not summary.empty else {},
            'details': self.estimates
        }

    def export_estimate(self, output_path: str) -> str:
        """Export estimate to Excel"""
        df = pd.DataFrame(self.estimates)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary = pd.DataFrame({
                'Metric': ['Total Cost', 'Elements', 'Matched', 'Avg Confidence'],
                'Value': [
                    df['total_cost'].sum() if not df.empty else 0,
                    len(df),
                    len(df[df['match_confidence'] > 0.5]) if not df.empty else 0,
                    df['match_confidence'].mean() if not df.empty else 0
                ]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)

            # Details
            if not df.empty:
                df.to_excel(writer, sheet_name='Details', index=False)

                # By type
                by_type = df.groupby('element_type')['total_cost'].sum()
                by_type.to_excel(writer, sheet_name='By_Type')

        return output_path

    def get_missing_items(self) -> List[Dict]:
        """Get elements that couldn't be matched"""
        df = pd.DataFrame(self.estimates)
        if df.empty:
            return []

        low_confidence = df[df['match_confidence'] < 0.5]
        return low_confidence.to_dict('records')
```

## 数据库管理

### 创建和更新数据库

```python
class OpenDatabaseManager:
    """Manage open construction pricing database"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = self._load_or_create()

    def _load_or_create(self) -> pd.DataFrame:
        """Load existing or create new database"""
        try:
            return pd.read_csv(self.db_path)
        except FileNotFoundError:
            return pd.DataFrame(columns=list(WORK_ITEMS_SCHEMA.keys()))

    def add_items(self, items: List[Dict]):
        """Add new work items"""
        new_df = pd.DataFrame(items)
        self.db = pd.concat([self.db, new_df], ignore_index=True)
        self.db.drop_duplicates(subset=['code'], keep='last', inplace=True)

    def update_prices(self, updates: pd.DataFrame, year: int):
        """Update prices with new data"""
        for _, row in updates.iterrows():
            mask = self.db['code'] == row['code']
            if mask.any():
                self.db.loc[mask, 'unit_price'] = row['unit_price']
                self.db.loc[mask, 'year'] = year

    def apply_inflation(self, rate: float):
        """Apply inflation adjustment"""
        self.db['unit_price'] = self.db['unit_price'] * (1 + rate)

    def export_subset(self, category: str, output_path: str):
        """Export subset of database"""
        subset = self.db[
            self.db['category_l1'].str.contains(category, case=False, na=False)
        ]
        subset.to_csv(output_path, index=False)

    def save(self):
        """Save database"""
        self.db.to_csv(self.db_path, index=False)

    def get_statistics(self) -> Dict:
        """Get database statistics"""
        return {
            'total_items': len(self.db),
            'categories': self.db['category_l1'].nunique(),
            'avg_price': self.db['unit_price'].mean(),
            'price_range': (self.db['unit_price'].min(), self.db['unit_price'].max()),
            'latest_year': self.db['year'].max() if 'year' in self.db else None
        }
```

## 快速参考

| 类别 | CSI分类 | 典型工种 |
|----------|--------------|---------------|
| 混凝土 | 03 | 墙体、楼板、柱子、梁 |
| 砌体 | 04 | 砖块、砌块、石材 |
| 金属 | 05 | 结构钢、其他金属 |
| 装饰材料 | 09 | 石膏板、油漆、地板 |
| MEP（机电工程） | 21-26 | 给排水系统、暖通空调、电气系统 |
| 土木工程 | 31-33 | 挖掘、铺路、公用设施 |

## 资源

- **OpenConstructionEstimate**：一个开源的数据库项目
- **CSI MasterFormat**：https://www.csiresources.org/standards/masterformat
- **DDC官方网站**：https://datadrivenconstruction.io

## 下一步操作

- 查看 `vector-search` 以了解语义工种匹配的功能
- 查看 `cost-prediction` 以了解基于机器学习的估算方法
- 查看 `qto-report` 以了解数量提取的功能