---
name: mind-security
description: AI安全工具包——深度伪造内容与AI生成内容的检测功能。适用于验证图片、视频或音频是否为深度伪造作品或由AI生成的内容。
metadata: {"openclaw": {"emoji": "🛡️", "requires": {"bins": ["python3"], "anyBins": ["curl", "wget"]}, "homepage": "https://github.com/mind-sec/mind-security"}}
---
# mind-security

该系统采用 [Bittensor Subnet 34](https://bitmind.ai) 提供的深度伪造检测技术。检测模型通过对抗性训练不断进化：生成伪造内容的工具不断提升图像的逼真度，而检测工具则不断提高检测的准确性。

## 快速参考

| 功能 | 命令 | 文档链接 |
|------|---------|------|
| 检测图片 | `python3 scripts/check_deepfake.py <路径或URL>` | [deepfake-detection.md](references/deepfake-detection.md) |
| 通过curl检测 | `curl -X POST https://api.bitmind.ai/detect-image -H "Authorization: Bearer $BITMIND_API_KEY" -d '{"image":"<url>"}'` | [deepfake-detection.md](references/deepfake-detection.md) |
| 检测视频 | `curl -X POST https://api.bitmind.ai/detect-video -d '{"video":"<url>","debug":true}'` | [deepfake-detection.md](references/deepfake-detection.md) |

## 工作原理

该 API 支持检测 **任何类型的 URL**，包括直接链接的图片、社交媒体帖子以及 YouTube 视频。系统会在服务器端下载并分析这些媒体文件。

**图片处理流程：**  
认证 → 缓存 → 下载 → 预处理 → C2PA（内容真实性验证） → 并行检测（使用 Bittensor Subnet 34） → isAI（智能分析） → 确信度评估

**视频处理流程：**  
与图片处理流程相同，此外还包括对视频内容进行“荒谬性”分析（采用三路并行处理）。荒谬性分析会生成对视频内容的自然语言描述，并标记出物理上不可能存在的场景。

**isAI 的判断逻辑：**  
C2PA（内容真实性验证）结果 > 相似度 ≥ 0.7 > 荒谬性 ≥ 0.8（针对视频） > 模型预测结果 ≥ 0.5。所有这些因素都会影响最终的确信度评分。

**返回结果：**  
`{isAI: bool, confidence: float, similarity: float}`。当 `debug` 参数设置为 `true` 时，还会返回原始评分、处理时间、C2PA 详细信息以及荒谬性分析结果（仅针对视频）。

## 设置要求

需要使用 `BITMIND_API_KEY`。请在 [app.bitmind.ai](https://app.bitmind.ai) 注册或登录，然后在 [app.bitmind.ai/api/keys](https://app.bitmind.ai/api/keys) 生成 API 密钥。

## 脚本编写规范：

- 使用 `python3 scripts/<脚本名>.py --help` 命令查看脚本用法。
- 脚本不依赖任何第三方库（仅使用 Python 标准库）。
- 所有输出数据（包括 JSON 格式的数据）都会写入标准输出（stdout），错误信息则写入标准错误输出（stderr）。
- 成功执行时返回代码 0，失败时返回代码 1。