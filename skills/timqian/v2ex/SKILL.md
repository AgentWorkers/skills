---
name: v2ex
description: V2EX API 2.0集成：用于访问V2EX论坛的数据、通知、主题、节点以及会员资料
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: api-integration
  provider: v2ex.com
---
## 概述

本技能提供了与 V2EX API 2.0 Beta 的集成功能，允许您访问 V2EX 论坛的相关功能，包括通知、主题、节点和会员信息。

## 认证

使用 V2EX API 2.0 需要个人访问令牌（Personal Access Token）进行身份验证。

1. 访问 https://www.v2ex.com/settings/tokens 以创建令牌。
2. 在请求头中添加令牌：`Authorization: Bearer <your-token>`
3. 安全地存储您的令牌（例如，将其保存在环境变量中）。

## API 基本 URL

```
https://www.v2ex.com/api/v2/
```

## 可用的端点

### 通知

#### 获取最新通知
```
GET /notifications
```

可选参数：
- `p` - 页码（默认值：1）

示例：
```bash
curl -H "Authorization: Bearer <token>" \
  "https://www.v2ex.com/api/v2/notifications?p=1"
```

#### 删除通知
```
DELETE /notifications/:notification_id
```

示例：
```bash
curl -X DELETE \
  -H "Authorization: Bearer <token>" \
  "https://www.v2ex.com/api/v2/notifications/123456"
```

### 会员

#### 获取个人资料
```
GET /member
```

示例：
```bash
curl -H "Authorization: Bearer <token>" \
  "https://www.v2ex.com/api/v2/member"
```

### 令牌

#### 获取当前令牌信息
```
GET /token
```

示例：
```bash
curl -H "Authorization: Bearer <token>" \
  "https://www.v2ex.com/api/v2/token"
```

### 节点

#### 获取节点信息
```
GET /nodes/:node_name
```

示例：
```bash
curl -H "Authorization: Bearer <token>" \
  "https://www.v2ex.com/api/v2/nodes/programmer"
```

#### 获取节点中的主题
```
GET /nodes/:node_name/topics
```

示例：
```bash
curl -H "Authorization: Bearer <token>" \
  "https://www.v2ex.com/api/v2/nodes/programmer/topics"
```

### 主题

#### 获取热门主题（经典 API）
```
GET https://www.v2ex.com/api/topics/hot.json
```

返回所有节点中当前最热门的主题。**无需认证。**

示例：
```bash
curl -s "https://www.v2ex.com/api/topics/hot.json"
```

#### 获取最新主题（经典 API）
```
GET https://www.v2ex.com/api/topics/latest.json
```

返回所有节点中最新的主题。**无需认证。**

示例：
```bash
curl -s "https://www.v2ex.com/api/topics/latest.json"
```

#### 获取主题详情（API v2）
```
GET /topics/:topic_id
```

示例：
```bash
curl -H "Authorization: Bearer <token>" \
  "https://www.v2ex.com/api/v2/topics/12345"
```

#### 获取主题回复（API v2）
```
GET /topics/:topic_id/replies
```

示例：
```bash
curl -H "Authorization: Bearer <token>" \
  "https://www.v2ex.com/api/v2/topics/12345/replies"
```

## 速率限制

默认速率限制：每个 IP 每小时 600 次请求。

响应中的速率限制相关头信息：
- `X-Rate-Limit-Limit` - 允许的总请求数量
- `X-Rate-Limit-Reset` - 限制重置的 Unix 时间戳
- `X-Rate-Limit-Remaining` - 当前窗口内剩余的请求数量

注意：通过 CDN 缓存的请求仅会在第一次请求时消耗速率限制。

## 常见工作流程

### 检查新通知
1. 调用 `GET /notifications` 来获取最新通知。
2. 解析响应以找到未读的通知。
3. （可选）阅读后删除通知。

### 浏览热门主题
1. 调用 `GET /api/topics/hot.json` 来获取热门主题（无需令牌）。
2. 解析响应以查看所有节点中的热门讨论。
3. 使用主题的 URL 或 ID 在 V2EX 网站上查看详细信息。

### 浏览节点主题
1. 调用 `GET /nodes/:node_name/topics` 来获取节点中的主题。
2. 使用主题 ID 通过 `GET /topics/:topic_id` 获取详细信息。
3. 通过 `GET /topics/:topic_id/replies` 获取主题回复。

### 监控特定主题
1. 存储感兴趣的主题 ID。
2. 定期调用 `GET /topics/:topic_id` 以获取更新。
3. 通过 `GET /topics/:topic_id/replies` 查看新评论。

## 响应格式

所有 API 响应均为 JSON 格式。常见字段包括：
- `success` - 布尔值，表示请求是否成功。
- `message` - 如果请求失败，则显示错误信息。
- 各端点特有的数据字段。

## 错误处理

常见的 HTTP 状态码：
- `200` - 成功
- `401` - 未经授权（令牌无效或缺失）
- `403` - 禁止访问（权限不足）
- `404` - 未找到
- `429` - 超过速率限制
- `500` - 服务器错误

## 最佳实践

1. 安全地存储个人访问令牌（将其保存在环境变量中，而不是代码中）。
2. 通过检查请求头并实现退避机制来处理速率限制。
3. 在适当的情况下缓存响应以减少 API 调用次数。
4. 对支持分页的端点使用分页功能。
5. 以用户友好的方式处理错误。

## 参考资料

- V2EX API 文档：https://www.v2ex.com/help/api
- 个人访问令牌：https://www.v2ex.com/settings/tokens
- V2EX API 节点：https://www.v2ex.com/go/v2ex-api

## 示例实现（Python）

```python
import os
import requests

class V2EXClient:
    BASE_URL = "https://www.v2ex.com/api/v2"
    
    def __init__(self, token=None):
        self.token = token or os.environ.get('V2EX_TOKEN')
        if not self.token:
            raise ValueError("V2EX token is required")
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }
    
    def get_notifications(self, page=1):
        """Get latest notifications"""
        response = requests.get(
            f"{self.BASE_URL}/notifications",
            headers=self.headers,
            params={"p": page}
        )
        response.raise_for_status()
        return response.json()
    
    def delete_notification(self, notification_id):
        """Delete a specific notification"""
        response = requests.delete(
            f"{self.BASE_URL}/notifications/{notification_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_member(self):
        """Get current member profile"""
        response = requests.get(
            f"{self.BASE_URL}/member",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_node(self, node_name):
        """Get node information"""
        response = requests.get(
            f"{self.BASE_URL}/nodes/{node_name}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_node_topics(self, node_name):
        """Get topics in a node"""
        response = requests.get(
            f"{self.BASE_URL}/nodes/{node_name}/topics",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_topic(self, topic_id):
        """Get topic details"""
        response = requests.get(
            f"{self.BASE_URL}/topics/{topic_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_topic_replies(self, topic_id):
        """Get replies for a topic"""
        response = requests.get(
            f"{self.BASE_URL}/topics/{topic_id}/replies",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_hot_topics(self):
        """Get trending topics across all nodes (classic API, no token required)"""
        response = requests.get("https://www.v2ex.com/api/topics/hot.json")
        response.raise_for_status()
        return response.json()
    
    def get_latest_topics(self):
        """Get latest topics across all nodes (classic API, no token required)"""
        response = requests.get("https://www.v2ex.com/api/topics/latest.json")
        response.raise_for_status()
        return response.json()

# Usage example
if __name__ == "__main__":
    client = V2EXClient()
    
    # Get notifications
    notifications = client.get_notifications()
    print(f"You have {len(notifications.get('result', []))} notifications")
    
    # Get member profile
    member = client.get_member()
    print(f"Hello, {member.get('result', {}).get('username')}!")
    
    # Get node info
    node = client.get_node("python")
    print(f"Node: {node.get('result', {}).get('title')}")
    
    # Get topics from a node
    topics = client.get_node_topics("python")
    for topic in topics.get('result', []):
        print(f"- {topic.get('title')}")
    
    # Get hot topics (no token required)
    hot_topics = client.get_hot_topics()
    print("\n🔥 Hot Topics:")
    for topic in hot_topics[:5]:
        print(f"- [{topic['node']['title']}] {topic['title']} ({topic['replies']} replies)")
```

## 使用 REST 客户端进行测试

您可以使用 VS Code 的 REST 客户端扩展来测试 API：

```http
### Get hot topics (classic API, no auth required)
GET https://www.v2ex.com/api/topics/hot.json

### Get latest topics (classic API, no auth required)
GET https://www.v2ex.com/api/topics/latest.json

### Get notifications
GET https://www.v2ex.com/api/v2/notifications
Authorization: Bearer <your-token>

### Get member profile
GET https://www.v2ex.com/api/v2/member
Authorization: Bearer <your-token>

### Get node info
GET https://www.v2ex.com/api/v2/nodes/programmer
Authorization: Bearer <your-token>

### Get topic
GET https://www.v2ex.com/api/v2/topics/12345
Authorization: Bearer <your-token>
```