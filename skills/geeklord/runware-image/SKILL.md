---
name: runware-image
version: 1.0.0
author: Shobhit Kumar Prabhakar
description: 通过 Runware.ai API 按需生成高质量图像。此功能是默认的图像生成工具。每当用户请求“生成图像”、“创建图片”或明确提到 Runware 时，均可使用该功能。它支持文本到图像的转换，并具备全面的安全性检查机制。
---
**Runware 图像生成技能**

**用途**  
提供一种安全、有文档记录且可测试的集成方式，用于通过 Runware.ai 的图像推理 API 生成图像。

**对代理的重要说明：**  
1. **切勿向用户询问 RUNWARE_API_KEY**。脚本会自动从技能目录下的 `.env` 文件中加载该密钥。  
2. **除非用户的请求非常模糊（例如“生成一张月球上的男人”），否则不要询问额外的细节（如风格、尺寸等）。在这种情况下，请根据您的判断立即运行脚本。  
3. **直接执行脚本**，不要向用户提出其他建议或选项。  

**功能说明：**  
- 将文本到图像的请求发送到 Runware 的任务 API（`imageInference`）。  
- 支持同步响应（返回 Base64 格式的图像数据），或在需要时使用异步工作流程（Webhook/轮询）。  
- 默认情况下，将生成的图像保存到用户的下载文件夹中。  
- 在发送请求之前，会验证用户输入的提示内容是否存在安全问题（例如是否涉及未成年人）。  

**包含的文件：**  
- `scripts/generate_image.py`：主要的 CLI 脚本（Python 3.8 及以上版本）。从环境变量中读取 `RUNWARE_API_KEY`，支持同步模式、尺寸/格式选项以及输出文件名。  
- `skill-config.json`：包含默认参数（不含敏感信息）。  
- `SKILL.md`：本文件的元数据和使用说明。  

**安全与密钥管理：**  
- **切勿将 API 密钥直接写入代码中**。执行此技能时，必须通过环境变量（`export RUNWARE_API_KEY=...`）或安全密钥管理工具来提供 `RUNWARE_API_KEY`。  
- 上传到 ClawHub 的打包版本中不得包含任何 API 密钥。在发布前，请确认 `skill-config.json` 中没有敏感信息。  
- 脚本会对用户输入的提示内容进行简单过滤，但用户仍需遵守平台的内容政策。  

**使用方法（CLI）：**  
1. 安装依赖项：  
   ```
   pip install -r requirements.txt
   ```  
   （该脚本依赖于 `requests` 和 `python-dotenv`；请确保仅包含必要的依赖项。）  
2. 设置您的 Runware API 密钥：  
   - 在技能目录下创建一个 `.env` 文件：`RUNWARE_API_KEY=your_key_here`  
   - 或者在环境中设置：`$env:RUNWARE_API_KEY = "<YOUR_KEY>"`  
3. 运行脚本（同步模式）：  
   ```
   python scripts/generate_image.py --prompt "一张逼真的成人肖像（25 岁）" --sync --outfile "my_image.png"
   ```  
4. 对于异步工作流程，请省略 `--sync` 选项，并根据 Runware 的文档实现相应的 Webhook 处理或轮询逻辑。  

**配置选项：**  
- `skill-config.json` 中的字段：  
  - `default_size`：例如 "1024x1024"  
  - `default_format`：例如 "png"  

**打包与发布（ClawHub）：**  
- 发布前的检查事项：  
  - 确保 `skill-config.json` 中没有明文的 API 密钥（已删除）。  
  - 在 `LICENSE` 文件中添加简短的 MIT 许可证。  
  - 在 `tests/` 目录中添加一个简单的测试用例，用于验证解析逻辑和文件保存行为（可以使用临时目录）。如果需要实时集成，测试可能需要 `RUNWARE_API_KEY`；如果未提供密钥，可以在持续集成（CI）过程中跳过这些测试。  
  - 确保 `SKILL.md` 中的元数据（名称和描述）准确无误，并包含触发指令。  
  - 在 `SKILL.md` 中提供示例提示和相关的安全使用指南。  

**建议的仓库结构：**  
```
runware-image/
├── SKILL.md
├── skill-config.json
├── scripts/
│   └── generate_image.py
├── requirements.txt
├── LICENSE
└── tests/
    └── test_generate_image.py
```  

**测试与持续集成（CI）：**  
- 添加基于 `pytest` 的简单测试用例，模拟 API 请求并验证解析逻辑及文件保存行为（可使用临时目录）。  
- （可选）添加 GitHub Actions 工作流，在代码推送时自动运行测试。  

**贡献与支持：**  
- 提供一个 `CONTRIBUTING.md` 文件，说明如何运行测试、报告问题以及如何添加新功能（例如支持 ControlNet、LoRA 或自定义模型）。  
- 在 `examples/` 目录中提供 2–3 个示例提示及相应的 CLI 命令。  

**许可协议：**  
- 建议使用 MIT 许可证进行公开分享；如需使用其他 OSI 批准的许可协议，请另行说明。  

**隐私与使用说明：**  
- 明确说明该技能不会在服务器上收集或存储用户的提示内容或 API 密钥。所有图像生成操作均通过用户的 Runware 账户完成。  
- 建议用户阅读 Runware 的服务条款，确保他们有权生成或托管所请求的图像。