---
name: replicate
description: "**ML平台复制工具**  
- 运行AI模型  
- 管理预测结果  
- 浏览模型集合  
- 搜索所需模型  
**ML推理命令行工具（ML Inference CLI）**"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🤖", "requires": {"env": ["REPLICATE_API_TOKEN"]}, "primaryEnv": "REPLICATE_API_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🤖 复制（Replicate）

通过 API 运行机器学习模型——包括模型预测、模型搜索以及模型集合管理。

## 功能

- **模型**：浏览和搜索模型
- **预测**：创建、获取、取消预测结果
- **模型集合**：管理精选的模型
- **硬件**：可用的 GPU 资源

## 需求

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `REPLICATE_API_TOKEN` | ✅ | 用于访问 Replicate API 的密钥/令牌 |

## 快速入门

```bash
python3 {baseDir}/scripts/replicate.py search "text to image"
python3 {baseDir}/scripts/replicate.py run <version> '{"prompt":"a cat"}'
python3 {baseDir}/scripts/replicate.py predictions
python3 {baseDir}/scripts/replicate.py me
```

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
本功能属于 OpenClaw 代理的 **AgxntSix 技能套件** 的一部分。

📅 **需要帮助为您的企业设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)