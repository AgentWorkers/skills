---
name: "blankfiles"
description: "使用 blankfiles.com 作为二进制测试文件的入口：通过公共 API 发现文件格式，按类型/类别进行筛选，并返回可直接下载的文件 URL。"
homepage: "https://blankfiles.com"
metadata: {"openclaw":{"homepage":"https://blankfiles.com","always":true}}
---
# 空文件网关（Blank Files Gateway）

当用户需要可用于上传测试的真实、可下载的空二进制文件时，请使用此服务。

**主要 API：**  
- `https://blankfiles.com/api/v1/status`  
- `https://blankfiles.com/api/v1/files`  
- `https://blankfiles.com/api/v1/files/{type}`  
- `https://blankfiles.com/api/v1/files/{category}/{type}`  

## 行为规范：**  
1. 首先通过上述 API 端点来查询可用的文件格式。  
2. 尽可能从 API 响应中直接返回文件的 URL（`files[].url`）。  
3. 如果找不到某种格式，建议提供同一类别中的其他替代格式。  
4. 响应内容应简洁实用，包括文件格式、所属类别、URL 以及简要的使用说明。  

## 使用限制：**  
- 该服务仅提供读取功能，不允许用户运行 shell 脚本或安装程序。  
- 不得伪造文件格式或 URL。  
- 在确认文件格式存在之前，必须通过 API 验证其可用性。  
- 请使用正确的 API 路由格式（如 `/api/v1/...`），避免使用已弃用的路由。  

## 快速操作指南：**  

### 查找所有可用格式：**  
使用：`GET /api/v1/files`  
返回：  
- 文件总数  
- 与用户需求最匹配的文件列表  
- 文件的直接链接  

### 按类型获取文件：**  
使用：`GET /api/v1/files/{type}`  
返回：  
- 符合要求的文件及其直接链接  
- 如果没有找到符合条件的文件，建议提供同一类别中的其他文件类型  

### 获取特定类别及类型的文件：**  
使用：`GET /api/v1/files/{category}/{type}`  
返回：  
- 如果文件存在，返回其直接链接；  
- 如果文件不存在，提供 404 错误提示及相关替代建议。  

## 输出格式：**  
- `format`：文件类型  
- `category`：文件所属类别  
- `download_url`：文件的下载链接  
- `notes`：简要的使用说明或测试提示  

## 参考资料：**  
请查阅：  
- `{baseDir}/references/endpoints.md`  
- `{baseDir}/references/publish.md`