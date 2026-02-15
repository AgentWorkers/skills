---
name: google-search
description: 使用 Google 自定义搜索引擎（PSE）在网络上进行搜索。当您需要实时信息、文档，或者研究某些主题时，而内置的 web_search 功能无法满足需求时，可以使用此工具。
---

# Google 搜索技能

该技能允许 OpenClaw 代理通过 Google 的自定义搜索 API（PSE）执行网页搜索。

## 设置

1. **Google Cloud 控制台：** 创建一个项目并启用“自定义搜索 API”功能。
2. **API 密钥：** 生成一个 API 密钥。
3. **搜索引擎 ID (CX)：** 在 [cse.google.com](https://cse.google.com/cse/all) 上创建一个可编程搜索引擎，并获取您的 CX ID。
4. **环境配置：** 将您的凭据存储在工作区的 `.env` 文件中：
    ```
    GOOGLE_API_KEY=your_key_here
    GOOGLE_CSE_ID=your_cx_id_here
    ```

## 工作流程
...（文件其余部分）

## 示例用法
```bash
GOOGLE_API_KEY=xxx GOOGLE_CSE_ID=yyy python3 skills/google-search/scripts/search.py "OpenClaw documentation"
```