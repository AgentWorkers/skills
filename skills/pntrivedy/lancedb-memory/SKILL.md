```python
#!/usr/bin/env python3
"""
LanceDB集成用于长期记忆管理，提供向量搜索和语义记忆功能。"""

import os
import json
import lancedb
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

class LanceMemoryDB:
    """LanceDB的封装类，用于长期记忆的存储和检索。"""

    def __init__(self, db_path: str = "/Users/prerak/clawd/memory/lancedb"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(self.db_path)
        
        # 确保记忆表存在
        if "memory" not in self.db.table_names():
            self._create_memory_table()
    
    def _create_memory_table(self):
        """创建记忆表并设置相应的表结构。"""
        schema = [
            {"name": "id", "type": "int", "nullable": False},
            {"name": "timestamp", "type": "timestamp", "nullable": False},
            {"name": "content", "type": "str", "nullable": False},
            {"name": "category", "type": "str", "nullable": True},
            {"name": "tags", "type": "str[]", "nullable": True},
            {"name": "importance", "type": "int", "nullable": True},
            {"name": "metadata", "type": "json", "nullable": True},
        ]
        
        self.db.create_table("memory", schema=schema)
    
    def add_memory(self, content: str, category: str = "general", tags: List[str] = None, 
                   importance: int = 5, metadata: Dict[str, Any] = None) -> int:
        """添加新的记忆记录。"""
        table = self.db.open_table("memory")
        
        # 获取下一个可用ID
        max_id = table.to_pandas()["id"].max() if len(table) > 0 else 0
        new_id = max_id + 1
        
        # 插入新记录
        memory_data = {
            "id": new_id,
            "timestamp": datetime.now(),
            "content": content,
            "category": category,
            "tags": tags or [],
            "importance": importance,
            "metadata": metadata or {}
        }
        
        table.add([memory_data])
        return new_id
    
    def search_memories(self, query: str, category: str = None, limit: int = 10) -> List[Dict]:
        """使用向量相似性进行记忆搜索。"""
        table = self.db.open_table("memory")
        
        # 构建搜索条件
        where_clause = []
        if category:
            where_clause.append(f"category = '{category}'")
        
        filter_expr = " AND ".join(where_clause) if where_clause else None
        
        # 执行向量搜索
        results = table.vector_search(query).limit(limit).where(filter_expr).to_list()
        
        return results
    
    def get_memories_by_category(self, category: str, limit: int = 50) -> List[Dict]:
        """按类别获取记忆记录。"""
        table = self.db.open_table("memory")
        df = table.to_pandas()
        filtered = df[df["category"] == category].head(limit)
        return filtered.to_dict("records")
    
    def get_memory_by_id(self, memory_id: int) -> Optional[Dict]:
        """通过ID获取特定的记忆记录。"""
        table = self.db.open_table("memory")
        df = table.to_pandas()
        result = df[df["id"] == memory_id]
        return result.to_dict("records")[0] if len(result) > 0 else None
    
    def update_memory(self, memory_id: int, **kwargs) -> bool:
        """更新记忆记录。"""
        table = self.db.open_table("memory")
        
        valid_fields = ["content", "category", "tags", "importance", "metadata"]
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not updates:
            return False
        
        # 将参数转换为LanceDB支持的格式
        if "tags" in updates and isinstance(updates["tags"], list):
            updates["tags"] = str(updates["tags"].replace("'", '"")
        
        table.update(updates, where=f"id = {memory_id}")
        return True
    
    def delete_memory(self, memory_id: int) -> bool:
        """删除记忆记录。"""
        table = self.db.open_table("memory")
        current_count = len(table)
        table.delete(f"id = {memory_id}")
        return len(table) < current_count
    
    def get_all_categories(self) -> List[str]:
        """获取所有唯一的类别。"""
        table = self.db.open_table("memory")
        df = table.to_pandas()
        return df["category"].dropna().unique().tolist()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆存储的统计信息。"""
        table = self.db.open_table("memory")
        df = table.to_pandas()
        
        return {
            "total_memories": len(df),
            "categories": len(self.get_all_categories()),
            "by_category": df["category"].value_counts().to_dict(),
            "date_range": {
                "earliest": df["timestamp"].min().isoformat() if len(df) > 0 else None,
                "latest": df["timestamp"].max().isoformat() if len(df) > 0 else None
            }
        }

# 全局实例
lancedb_memory = LanceMemoryDB()

def add_memory(content: str, category: str = "general", tags: List[str] = None, 
               importance: int = 5, metadata: Dict[str, Any] = None) -> int:
    """将记忆记录添加到LanceDB中。"""
    return lancedb_memory.add_memory(content, category, tags, importance, metadata)

def search_memories(query: str, category: str = None, limit: int = 10) -> List[Dict]:
    """使用语义相似性搜索记忆记录。"""
    return lancedb_memory.search_memories(query, category, limit)

def get_memories_by_category(category: str, limit: int = 50) -> List[Dict]:
    """按类别获取记忆记录。"""
    return lancedb_memory.get_memories_by_category(category, limit)

def get_memory_stats() -> Dict[str, Any]:
    """获取记忆存储的统计信息。"""
    return lancedb_memory.get_memory_stats()

# 示例用法
if __name__ == "__main__":
    # 测试数据库功能
    print("测试LanceDB的记忆管理集成...")
    
    # 添加一条测试记忆记录
    test_id = add_memory(
        content="这是一条用于测试LanceDB集成的记忆记录",
        category="test",
        tags=["lancedb", "integration", "test"],
        importance=8
    )
    print(f"添加的记忆记录的ID为：{test_id}")
    
    # 搜索记忆记录
    results = search_memories("test memory")
    print(f"搜索结果：找到{len(results)}条记忆记录")
    
    # 获取记忆记录的统计信息
    stats = get_memory_stats()
    print(f"记忆记录的统计信息：{stats}")
```