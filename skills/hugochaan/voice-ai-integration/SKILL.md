---
name: voice-ai-integration
description: 集成 Shengwang（Agora）产品：ConvoAI 语音代理、RTC 音频/视频功能、RTM 消息传递、云录制服务以及令牌生成功能。当用户提到 Shengwang、Agora、声网（Voice Network）、ConvoAI、RTC、RTM、语音代理、AI 代理、视频通话、实时流媒体、录制、令牌或任何与 Agora 相关的产品功能时，可以使用这些集成服务。
license: MIT
metadata:
  author: shengwang
  version: "1.0.0"
---
# Shengwang 集成

## 工作流程

### 第 0 步：确保文档索引存在（强制要求）

> **⚠️ 此步骤不可协商。请在任何路由处理、信息收集或代码生成之前执行。**

检查 `references/docs.txt` 文件是否存在。如果不存在（或者这是一个新项目），请立即下载该文件：
```bash
bash skills/voice-ai-integration/scripts/fetch-docs.sh
```
该文件是文档索引，所有文档查找都依赖于它。
在文件存在或下载完成之前，请勿进入第 1 步。
如果下载失败，请使用本地参考文档和备用 URL 继续操作。

### 第 1 步：收集项目启动所需的信息

使用 [intake](intake/README.md) 来收集项目启动所需的信息。
仅询问用户尚未提供的详细信息。

仅收集解决实施障碍所需的详细信息：
- 用户的使用场景/目标解决方案
- 主要使用的 Shengwang/Agora 产品
- 平台或客户端技术栈
- 如有必要，提供后端编程语言
- 已知的可能影响路由处理或实现的关键技术细节

采用对话式的交流方式：
- 每次只问一个简单的问题
- 在安全的情况下，从用户的请求中推断出明显的上下文
- 仅询问下一个最需要的缺失信息
- 一旦收集到足够的信息，即可停止提问

对于特定产品的配置选项（例如 ConvoAI 供应商），不要强制用户一次性提供所有配置信息。
可以给出推荐的默认值作为建议，但对于 ConvoAI，用户仍需明确回答或确认以下所有字段：
- 自动语音识别（ASR）相关设置
- ASR 使用的语言
- 大语言模型（LLM）
- 文本转语音（TTS）相关设置

“使用默认值”也是一种有效的确认方式。
请逐一收集这些确认信息，不要一次性填写完整的表格。

如果用户已经提供了足够的信息，请不要重复提问。
生成一份简明的项目启动信息总结，然后自动继续下一步，除非还有必要的详细信息缺失。

### 第 2 步：使用本地参考文档

根据项目启动信息总结以及下面的路由表，选择正确的本地参考模块。
如果现有信息足够，可以使用 `references/` 目录下的本地文档开始实施。

| 功能 | 对应的参考文档路径 |
|-------------|----------------------|
| 新请求、信息模糊或缺失 | [intake](intake/README.md)       |
| 认证信息、AppID、REST 认证 | [general](references/general/credentials-and-auth.md) |
| 下载 SDK、示例项目、Token Builder、GitHub 仓库 | 相关产品模块的文档 |
| 生成 Token、Token 服务器、AccessToken2、RTC/RTM 认证 | [token-server](references/token-server/README.md) |
| ConvoAI 相关操作（已知详细信息） | [conversational-ai](references/conversational-ai/README.md) |
| RTC SDK 集成 | [rtc](references/rtc/README.md)       |
| RTM 消息传递/信号处理 | [rtm](references/rtm/README.md)       |
| 云录制功能 | [cloud-recording](references/cloud-recording/README.md) |

如果第 2 步提供的信息足以开始实施，请继续下一步。
如果仍缺少关键信息或本地参考文档不足，请进入第 3 步。

### 第 3 步：通过文档获取更多信息

使用 [references/doc-fetching.md](references/doc-fetching.md) 来获取更详细的文档。
仅在第 2 步之后、本地参考文档不足以满足实施需求时才执行此步骤。

查找顺序：
1. 本技能相关的本地参考文档
2. 通过 `doc-fetching` 工作流程获取的文档
3. 仅在文档获取后仍需时，才进行网络搜索

一旦第 3 步提供了足够的信息，即可继续实施。

## 下载规则

- 使用 `git clone --depth 1 <url>` 进行下载——GitHub URL 必须指向仓库根目录（不要包含分支或子目录路径）
- 如果下载失败，请报告错误并提供手动下载的 URL，切勿直接跳过下载过程

## 链接

- 控制台：https://console.shengwang.cn/
- 文档（中文版）：https://doc.shengwang.cn/
- GitHub：https://github.com/Shengwang-Community