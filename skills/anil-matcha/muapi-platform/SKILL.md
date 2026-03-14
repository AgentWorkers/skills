---
slug: muapi-platform
name: muapi-platform
version: "0.1.0"
description: >
  **muapi.ai 的设置与辅助脚本**  
  ——配置 API 密钥、测试连接性以及获取异步生成结果  
  这些脚本用于帮助您快速配置 muapi.ai 的 API 密钥、验证网络连接，并定期检查异步生成的文件或数据。  
  **主要功能包括：**  
  1. **配置 API 密钥**：为您的 muapi.ai 账户生成并设置 API 密钥。  
  2. **测试连接性**：检查您的应用程序是否能够成功连接到 muapi.ai 服务器。  
  3. **获取异步结果**：定期查询 muapi.ai 服务器，以获取您请求的异步生成内容（如文件、数据等）。  
  **使用说明：**  
  - 首先，确保您已安装 muapi.ai 的相关 SDK 或客户端工具。  
  - 根据脚本中的说明，修改配置文件（如 `config.json`）以适应您的具体需求。  
  - 运行相应的脚本（如 `setup.py` 或 `test_connection.py`），按照提示完成配置和测试。  
  - 对于需要实时获取异步结果的应用程序，您可能需要定期运行 `poll_results.py` 脚本。  
  **注意：**  
  - 请确保您的系统环境满足脚本运行要求（如 Python 版本、依赖库等）。  
  - 如有技术问题，请查阅官方文档或联系技术支持。  
  **示例脚本结构：**  
  ```markdown
  # setup.py  
  # 配置 API 密钥  
  api_key = "YOUR_API_KEY"  
  # 其他配置参数...  
  # 测试与 muapi.ai 的连接性  
  def test_connection():  
      # 发送请求并检查响应  
      pass  
  # 定期获取异步生成结果  
  def poll_results():  
      # 向 muapi.ai 服务器请求数据  
      pass  
  ```
  请根据实际需求修改示例脚本，并按照提供的说明进行操作。
acceptLicenseTerms: true
---
# ⚙️ MuAPI平台工具

**用于muapi.ai平台的配置和数据轮询工具。**

您可以配置API密钥，验证连接是否正常，并轮询异步生成的结果。

## 可用的脚本

| 脚本 | 描述 |
| :--- | :--- |
| `setup.sh` | 配置API密钥，显示配置信息，测试密钥的有效性 |
| `check-result.sh` | 根据请求ID轮询异步生成的结果 |

## 快速入门

```bash
# Save your API key
bash setup.sh --add-key "YOUR_MUAPI_KEY"

# Show current configuration
bash setup.sh --show-config

# Test API key validity
bash setup.sh --test

# Poll for a result (waits for completion)
bash check-result.sh --id "your-request-id"

# Check once without polling
bash check-result.sh --id "your-request-id" --once
```

## 所需软件

- `curl`