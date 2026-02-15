---
name: get-tldr
description: 提供 get-tldr.com summarize API 返回的摘要内容，无需进一步总结；该技能应负责对 API 输出进行格式化以提升可读性，但不得更改其内容本身。
---

# get-tldr

这是一个快速、可靠的技能，用于使用 get-tldr.com API 概括链接的内容。

**使用方式（针对代理）：**  
- 当用户输入类似 “get-tldr <链接>” 或 “get-tldr” 并后跟一个 URL 时，该技能会被触发。  
- 该技能会调用名为 `get_tldr.py` 的脚本，并将 URL 作为唯一参数传递给该脚本。  

**重要说明：**  
- API 返回的响应本身就已经是一个摘要；该技能不得进一步对内容进行总结或修改，只需获取 JSON 数据中 “summary” 元素的值，并将其格式化为易于阅读的形式。请确保保留所有内容。  
- 如果 API 返回的 JSON 数据中的 “summary” 元素已经是 Markdown 格式，只需直接返回该格式化的内容即可，无需进行任何修改。同时，请确保该内容不会被包裹在代码块中；如果被包裹在代码块中，请将其移除，以确保其能够正确地以 Markdown 格式显示（而不是作为代码块）。  

**包含的文件：**  
- `get_tldr.py`：一个小型 Python 脚本（位于技能文件夹中），该脚本会使用所需的 X-API-Key 头部信息将 `{"input": "<URL>}` 发送到 `https://www.get-tldr.com/api/v1/summarize`，并将 API 的响应输出到标准输出（stdout）。脚本会从 `~/.config/get-tldr/config.json` 文件中读取 API 密钥（推荐配置方式），或者在缺少该文件时从 `GET_TLDR_API_KEY` 环境变量或技能文件夹中的 `.env` 文件中获取 API 密钥。如果没有配置日志文件，脚本会默认使用 `~/.config/get-tldr/skill.log` 作为日志文件。  

**维护者注意事项：**  
- 在 `~/.config/get-tldr/config.json` 文件中创建一个配置文件，其结构如下（JSON 格式）：  

```
{
  "api_token": "<your_key_here>",
  "logfile": "/path/to/logfile.log"
}
```  

- 脚本会使用配置文件中的 “api_token” 字段；如果配置文件缺失，脚本会从 `GET_TLDR_API_KEY` 环境变量或技能文件夹中的 `.env` 文件中获取 API 密钥。  
- 请注意：该技能仅负责对 API 返回的响应进行格式化，不得对内容本身进行任何修改。