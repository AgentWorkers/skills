---
name: "presearch-search"
description: "一款可用于生产环境的分散式AI代理搜索系统。该系统以用户隐私为核心设计，通过分布式节点基础设施提供无审查的网页搜索服务。"
---
# Presearch 搜索 API

**端点:** `https://na-us-1.presearch.com/v1/search`  
**方法:** GET  
**认证方式:** 承载令牌（Bearer Token）  
**请求速率限制:** 每分钟 100 次请求

## 认证  
```http
Authorization: Bearer YOUR_API_KEY_HERE
```

## 参数  
| 参数 | 类型 | 是否必填 | 默认值 | 描述 |  
|---------|------|---------|-------------|  
| `q` | 字符串 | ✅ | - | 搜索查询内容 |  
| `lang` | 字符串 | ❌ | en-US | 语言代码 |  
| `time` | 字符串 | ❌ | 任意值 | 时间范围（天、周、月、年） |  
| `page` | 字符串 | ❌ | 1 | 页码 |  
| `safe` | 字符串 | ❌ | 1 | 安全搜索模式（屏蔽不适宜的内容） |  

## 响应  
```json
{
  "data": {
    "standardResults": [
      {
        "title": "string",
        "link": "string",
        "description": "string"
      }
    ],
    "pagination": {
      "current_page": 1,
      "has_next": true
    }
  }
}
```

## 错误代码  
- 401: API 密钥无效  
- 402: 需要支付费用  
- 422: 参数无效  
- 429: 超过请求速率限制  

## 使用方法  
```python
# Python
with PresearchSkill(api_key) as skill:
    results = skill.search("AI agents")
```

## 隐私保护特性  
- 不会进行用户追踪或数据收集  
- 基于去中心化的节点网络运行  
- 数据传输采用加密方式  
- 提供未经审查的搜索结果  

---

（注：由于代码示例、注释等部分在提供的文档中缺失，因此对应的中文翻译内容也相应地进行了省略。在实际应用中，这些部分需要根据具体的代码实现来填写。）