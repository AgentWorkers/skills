---
name: ifttt
description: "IFTTT（If This Then That）自动化工具：通过IFTTT的Webhooks和API来触发Webhooks、管理Applets以及执行各种事件。利用简单的“如果-那么”逻辑，您可以连接800多种服务，触发自定义事件，并在服务之间传递数据。该工具专为AI代理设计，仅依赖Python标准库，没有任何外部依赖。适用于简单的自动化任务、Webhook触发、物联网集成、智能家居控制以及跨服务事件处理。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔀", "requires": {"env": ["IFTTT_WEBHOOK_KEY"]}, "primaryEnv": "IFTTT_WEBHOOK_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🔀 IFTTT

IFTTT（If This Then That）自动化工具——通过IFTTT的Webhook和API来触发Webhook、管理Applets以及执行各种操作。

## 主要功能

- **Webhook触发**：能够使用数据触发自定义事件。
- **事件数据**：每次触发最多可传递3个值。
- **服务查询**：检查服务的连接状态。
- **用户信息**：获取已认证用户的详细信息。
- **Applet管理**：列出并管理Applets（通过Connect API进行操作）。
- **触发历史记录**：查看最近的Webhook活动。
- **多事件触发**：可以按顺序触发多个事件。
- **JSON数据传输**：通过Webhook发送结构化数据。

## 使用要求

| 变量 | 必需条件 | 说明 |
|----------|----------|-------------|
| `IFTTT_WEBHOOK_KEY` | ✅ | IFTTT的API密钥/令牌 |

## 快速入门

```bash
# Fire a webhook event
python3 {baseDir}/scripts/ifttt.py trigger my_event --value1 "Hello" --value2 "World"
```

```bash
# Fire with JSON payload
python3 {baseDir}/scripts/ifttt.py trigger-json my_event '{"value1":"data1","value2":"data2","value3":"data3"}'
```

```bash
# Check webhook connectivity
python3 {baseDir}/scripts/ifttt.py status
```

```bash
# Get user info (Connect API)
python3 {baseDir}/scripts/ifttt.py user
```

## 命令

### `trigger`  
触发一个Webhook事件。  
```bash
python3 {baseDir}/scripts/ifttt.py trigger my_event --value1 "Hello" --value2 "World"
```

### `trigger-json`  
使用JSON数据触发事件。  
```bash
python3 {baseDir}/scripts/ifttt.py trigger-json my_event '{"value1":"data1","value2":"data2","value3":"data3"}'
```

### `status`  
检查Webhook的连接状态。  
```bash
python3 {baseDir}/scripts/ifttt.py status
```

### `user`  
获取用户信息（通过Connect API）。  
```bash
python3 {baseDir}/scripts/ifttt.py user
```

### `applets`  
列出所有已连接的Applets。  
```bash
python3 {baseDir}/scripts/ifttt.py applets --limit 20
```

### `applet-enable`  
启用一个Applet。  
```bash
python3 {baseDir}/scripts/ifttt.py applet-enable abc123
```

### `applet-disable`  
禁用一个Applet。  
```bash
python3 {baseDir}/scripts/ifttt.py applet-disable abc123
```

### `services`  
列出所有已连接的服务。  
```bash
python3 {baseDir}/scripts/ifttt.py services
```

## 输出格式

所有命令默认以JSON格式输出。若需要可读性更强的输出格式，可添加`--human`参数。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/ifttt.py trigger --limit 5

# Human-readable
python3 {baseDir}/scripts/ifttt.py trigger --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/ifttt.py` | 主要的命令行工具（CLI），用于执行所有IFTTT相关操作 |

## 数据政策

本工具**从不本地存储数据**。所有请求都会直接发送到IFTTT API，结果会显示在标准输出（stdout）中。您的数据将保存在IFTTT的服务器上。

## 致谢  
本工具由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi)和[agxntsix.ai](https://www.agxntsix.ai)共同开发。  
相关视频教程可在[YouTube](https://youtube.com/@aiwithabidi)观看，代码实现可在[GitHub](https://github.com/aiwithabidi)查看。  
本工具属于**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。  

📅 **需要帮助为您的业务配置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)