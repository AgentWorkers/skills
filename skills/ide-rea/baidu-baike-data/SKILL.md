---
name: baidu-baike-data
description: 百度百科组件是一种知识服务工具，旨在为用户查询各种名词的权威百科解释。其核心功能是：当用户提供一个特定的“名词”（如物体、人物、地点、概念、事件等）时，该工具会返回来自百度百科的标准化、详细的条目解释。
homepage: https://baike.baidu.com/
metadata: { "openclaw": { "emoji": "📖", "requires": { "bins": ["python3"] ,"env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 百度百科

从百度百科中查询百科条目。

## 两种使用场景

### 场景 1：直接搜索
获取关键词对应的默认匹配条目。
```bash
python3 scripts/baidu_baike.py --search_type=lemmaTitle --search_key="keyword"
```

### 场景 2：同名词解析
当某个词有多个条目时，列出所有条目并让用户通过 ID 进行选择。
```bash
# List entries with same name
python3 scripts/baidu_baike.py --search_type=lemmaList --search_key="keyword" --top_k=5

# Get specific entry by ID
python3 scripts/baidu_baike.py --search_type=lemmaId --search_key="entry_id"
```

## API
- LemmaList：列出具有相同标题的条目
- LemmaContent：根据标题或 ID 获取条目详情

## 设置
```bash
export BAIDU_API_KEY="your_api_key"
```

## 工作流程
1. 从查询中提取名词
2. 对于含义模糊的词，先调用 LemmaList
3. 用户从列表中选择所需的条目
4. 使用选定的 ID 调用 LemmaContent
5. 返回结构化数据