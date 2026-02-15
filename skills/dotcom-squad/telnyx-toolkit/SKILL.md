---
name: telnyx-toolkit
description: 完整的 Telnyx 工具包——包含即用型工具（STT、TTS、RAG、网络功能）以及适用于 JavaScript、Python、Go、Java 和 Ruby 的 SDK 文档。
metadata: {"openclaw":{"emoji":"📞","requires":{"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx 工具包

这是一个用于构建 Telnyx 应用程序的完整工具包，包含了 **即用型工具** 以及所有 Telnyx API 的 **SDK 文档**。

## 快速入门

```bash
export TELNYX_API_KEY="your_key_here"
```

---

## 🔧 即用型工具

这些是独立的实用程序，其中包含可以直接运行的脚本：

| 工具 | 描述 | 路径 |
|------|-------------|------|
| **Missions** | 人工智能代理任务跟踪、语音/SMS 助手、定时呼叫 | `{baseDir}/tools/missions/` |
| **STT** | 语音转文本（Whisper） | `{baseDir}/tools/stt/` |
| **TTS** | 文本转语音合成 | `{baseDir}/tools/tts/` |
| **CLI** | Telnyx 命令行接口（CLI）包装器和辅助工具 | `{baseDir}/tools/cli/` |
| **Network** | WireGuard 网络组网、公共 IP 配置 | `{baseDir}/tools/network/` |
| **RAG** | 结合 Telnyx 存储和嵌入技术的语义搜索 | `{baseDir}/tools/rag/` |
| **10DLC 注册** | A2P 消息服务的交互式注册工具 | `{baseDir}/tools/10dlc-registration/` |
| **存储备份** | 将工作区备份到 Telnyx 存储 | `{baseDir}/tools/storage-backup/` |
| **Voice SIP** | 基于 SIP 的语音呼叫控制 | `{baseDir}/tools/voice-sip/` |
| **Embeddings** | 语义搜索与文本嵌入（Telnyx 内置功能） | `{baseDir}/tools/embeddings/` |

### 工具使用示例

```bash
# Create a mission and schedule calls
python3 {baseDir}/tools/missions/scripts/telnyx_api.py init "Find contractors" "Call contractors and get quotes" "User request" '[{"step_id": "calls", "description": "Make calls", "sequence": 1}]'

# Transcribe audio
python3 {baseDir}/tools/stt/scripts/telnyx-stt.py /path/to/audio.mp3

# Generate speech  
python3 {baseDir}/tools/tts/scripts/telnyx-tts.py "Hello world" -o output.mp3

# Join mesh network
{baseDir}/tools/network/join.sh

# Index files for RAG
python3 {baseDir}/tools/rag/sync.py

# 10DLC registration wizard
{baseDir}/tools/10dlc-registration/setup.sh

# Semantic search
python3 {baseDir}/tools/embeddings/search.py "your query" --bucket your-bucket

# Index a file for search
python3 {baseDir}/tools/embeddings/index.py upload /path/to/file.md
```

每个工具都有对应的 `SKILL.md` 文件，其中包含详细的用法说明。

---

## 📚 API 文档（SDK 参考）

所有 Telnyx API 的 SDK 文档按语言分类：

| 语言 | 路径 | 文档内容 |
|----------|------|--------|
| **JavaScript** | `{baseDir}/api/javascript/` | 35 个 API 文档 |
| **Python** | `{baseDir}/api/python/` | 35 个 API 文档 |
| **Go** | `{baseDir}/api/go/` | 35 个 API 文档 |
| **Java** | `{baseDir}/api/java/` | 35 个 API 文档 |
| **Ruby** | `{baseDir}/api/ruby/` | 35 个 API 文档 |

### API 分类

每种语言的文档涵盖以下内容：

- **语音**：呼叫、呼叫控制、会议、流媒体传输、数据收集 |
- **消息服务**：短信、多媒体消息（MMS）、用户资料管理、托管消息服务 |
- **号码管理**：号码搜索、购买、配置、合规性检查 |
- **人工智能**：推理、语音助手、文本嵌入技术 |
- **存储**：对象存储（兼容 S3 标准） |
- **SIP**：中继服务、连接管理、集成功能 |
- **视频**：视频会议功能 |
- **传真**：可编程传真服务 |
- **物联网（IoT）**：SIM 卡管理、无线通信功能 |
- **身份验证**：电话验证、双重身份验证（2FA） |
- **账户管理**：账户信息管理、计费功能、报告生成 |
- **端口管理**：端口号码的接入与配置 |
- **10DLC**：A2P 消息服务的注册功能 |
- **TeXML**：TeXML 应用程序开发指南 |
- **网络**：私有网络配置、SETI 协议支持 |
- **WebRTC**：服务器端 WebRTC 实现 |

### 查找 API 文档的方法

```
{baseDir}/api/{language}/telnyx-{capability}-{language}/SKILL.md
```

示例：`{baseDir}/api/python/telnyx-voice-python/SKILL.md`

---

## 📱 WebRTC 客户端 SDK

这些 SDK 用于帮助您在移动设备和网页上开发实时语音应用：

| 平台 | 路径 |
|----------|------|
| **iOS** | `{baseDir}/webrtc-clients/ios/` |
| **Android** | `{baseDir}/webrtc-clients/android/` |
| **Flutter** | `{baseDir}/webrtc-clients/flutter/` |
| **JavaScript (Web)** | `{baseDir}/webrtc-clients/javascript/` |
| **React Native** | `{baseDir}/webrtc-clients/react-native/` |

---

## 工具包结构

```
telnyx-toolkit/
├── SKILL.md              # This file (index)
├── tools/                # Ready-to-use utilities
│   ├── missions/         # AI agent task tracking
│   ├── stt/
│   ├── tts/
│   ├── cli/
│   ├── network/
│   ├── rag/
│   ├── 10dlc-registration/
│   ├── storage-backup/
│   ├── voice-sip/
│   └── embeddings/
├── api/                  # SDK documentation
│   ├── javascript/       # 35 skills
│   ├── python/           # 35 skills
│   ├── go/               # 35 skills
│   ├── java/             # 35 skills
│   └── ruby/             # 35 skills
└── webrtc-clients/       # Mobile/Web SDK guides
    ├── ios/
    ├── android/
    ├── flutter/
    ├── javascript/
    └── react-native/
```

## 相关资源

- [Telnyx API 文档](https://developers.telnyx.com) |
- [Telnyx 官网](https://portal.telnyx.com) |
- [API 参考文档](https://developers.telnyx.com/api/v2/overview)