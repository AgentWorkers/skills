---
name: volcengine-ai-entry-ark
description: **Volcengine ARK模型调用与路由的基础技能**  
当用户希望使用ARK模型进行开发时，本技能提供了必要的支持。内容包括：  
- 请求模板的设计与使用  
- 端点的配置与管理  
- 模型的路由机制  
- 身份认证问题的排查与解决  

适用于需要了解如何使用ARK模型、请求处理流程、端点设置以及模型路由规则的用户。
---

# volcengine-ai-entry-ark

该模块负责将针对ARK模型的通用请求路由到相应的任务特定技能，并提供一个可运行的基本起点。

## 需要收集的输入参数

- `ARK_API_KEY`：ARK API密钥
- 模型端点ID（例如：`ep-xxxx`）
- 任务类型（聊天、摘要生成、代码编写、翻译）
- 可选的生成参数（`temperature`、`max_tokens`、`top_p`）

## 最小请求模板

```bash
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ep-xxxx",
    "messages": [
      {"role":"system","content":"You are a helpful assistant."},
      {"role":"user","content":"Hello"}
    ],
    "temperature": 0.2
  }'
```

## 故障排查指南

- 401：验证`ARK_API_KEY`及其权限范围
- 404：检查端点所在的区域/域名以及端点ID是否正确
- 429：降低请求频率，并采用退避策略进行重试
- 5xx：增加请求间隔时间并保留请求日志以供支持团队排查

## 参考资料

- `references/sources.md`