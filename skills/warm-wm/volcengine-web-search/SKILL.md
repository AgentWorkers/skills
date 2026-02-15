---
name: volcengine-web-search
description: 使用 `volcengine/web_search.py` 脚本在网页上搜索并获取结果，请准备一个清晰且具体的 `query`（查询条件）。运行脚本：`python scripts/web_search.py "query"`。根据返回的摘要列表来整理搜索结果，不要添加或猜测任何内容。
license: Complete terms in LICENSE.txt
---

# 网页搜索

## 使用场景

当你需要从公共网页中快速获取摘要信息时，可以使用此功能来调用 `web_search` 函数。

## 使用步骤

1. 准备一个清晰且具体的查询内容。
2. 运行脚本 `python scripts/web_search.py "query"`。运行之前，请先进入相应的目录。
3. 根据返回的摘要列表来整理结果，不要添加或猜测任何内容。

## 认证与凭据

- 首先，系统会尝试读取 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY` 环境变量。
- 如果这些变量未配置，系统将尝试使用 VeFaaS 的临时 IAM 凭据进行认证。

## 输出格式

- 控制台会输出最多 5 项的摘要信息。
- 如果调用失败，系统会打印错误响应。

## 示例

```bash
python scripts/web_search.py "2026 latest version of Python"
```