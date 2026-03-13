---
name: mind-security
description: >
  AI安全工具包——包括深度伪造检测、提示注入扫描、恶意软件/网络钓鱼URL扫描以及AI文本检测功能。适用场景如下：  
  (1) 验证图片、视频或音频是否为深度伪造内容或由AI生成；  
  (2) 检查用户输入是否包含提示注入攻击的代码；  
  (3) 扫描URL以检测是否存在恶意软件、网络钓鱼威胁或域名信誉问题；  
  (4) 判断文本是否由大型语言模型（LLM）生成。
metadata: {"openclaw": {"emoji": "🛡️", "requires": {"bins": ["python3"], "anyBins": ["curl", "wget"]}, "homepage": "https://github.com/mind-sec/mind-security"}}
---
# mind-security

这是一个AI安全工具包，包含四个功能模块。

## 快速参考

| 功能 | 命令 | 文档链接 |
|------|---------|------|
| 深度伪造检测 | `python3 scripts/check_deepfake.py <path_or_url>` | [deepfake-detection.md](references/deepfake-detection.md) |
| 提示注入扫描 | `python3 scripts/checkprompt_injection.py "<text>"` | [prompt-injection.md](references/prompt-injection.md) |
| 恶意软件/网络钓鱼扫描 | `python3 scripts/check_malware.py "https://..."` | [malware-scanning.md](references/malware-scanning.md) |
| AI文本检测 | `python3 scripts/check_ai_text.py "<text>"` | [ai-text-detection.md](references/ai-text-detection.md) |

## 模块介绍

**深度伪造检测**：使用BitMind API（Bittensor Subnet 34）对图像和视频进行深度伪造检测。支持YouTube、Twitter/X、TikTok等平台的URL。对于本地图像，可使用EXIF元数据进行检测。需要设置`BITMIND_API_KEY`（[获取API密钥](https://app.bitmind.ai/api/keys)）。

**提示注入扫描**：采用多层正则表达式模式（即时检测，无需额外依赖）以及LLM Guard机器学习扫描器（可选，需安装`pip install llm-guard`）。能够检测提示注入攻击、上下文篡改等恶意行为。

**恶意软件/网络钓鱼扫描**：整合了VirusTotal（70多种扫描引擎）、URLScan.io（1500多种品牌检测服务）以及Google Safe Browsing功能。即使不使用API密钥，也能通过启发式规则进行检测。

**AI文本检测**：利用GPTZero API对文本进行检测，支持GPT-4/5、Claude、LLaMA等模型，准确率高达99%。需要设置`GPTZERO_API_KEY`（[获取API密钥](https://gptzero.me/dashboard)）。

## API密钥

| 环境变量 | 使用模块 | 是否必需 | 获取方式 |
|---------|---------|----------|--------|
| `BITMIND_API_KEY` | 深度伪造检测 | 是 | [app.bitmind.ai/api/keys](https://app.bitmind.ai/api/keys) |
| `GPTZERO_API_KEY` | AI文本检测 | 是 | [gptzero.me/dashboard](https://gptzero.me/dashboard) |
| `VIRUSTOTAL_API_KEY` | 恶意软件扫描器 | 可选 | [virustotal.com](https://virustotal.com) |
| `URLSCAN_API_KEY` | 恶意软件扫描器 | 可选 | [urlscan.io](https://urlscan.io) |
| `GOOGLE_SAFE_BROWSING_KEY` | 恶意软件扫描器 | 可选 | [console.cloud.google.com](https://console.cloud.google.com) |

## 脚本编写规范

- 脚本格式：`python3 scripts/<script>.py --help`
- 核心功能仅依赖标准Python库（无需安装额外依赖包）。
- 对于提示注入检测功能，可选安装`pip install llm-guard`。
- 所有输出数据（包括JSON结果）写入标准输出（stdout），错误信息写入标准错误输出（stderr）。
- 成功时返回0，失败时返回1。