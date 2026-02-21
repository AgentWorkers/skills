---
name: agent-factory
description: >
  **代理创建与代理间切换（v1.0.5 - 支持 Chromium + 全部功能）**  
  **使用方法：**  
  - `/create_agent <名称>`：创建新代理并将其添加到配置文件中。  
  - `/switch <代理ID>`：切换当前使用的代理。
---
# 代理工厂（Agent Factory）

用于管理代理：创建代理以及代理之间的切换。

## 1. `/create_agent` 命令

用于创建新的代理：

```
/create_agent Muhasebeci
/create_agent Coderman
/create_agent Analist
```

### 参数

- **名称**：代理的显示名称
- **表情符号**：默认值：🤖
- **任务**：默认值：“帮助用户”

### 脚本使用方法

```bash
/home/ubuntu/.openclaw/workspace/skills/agent-factory/scripts/create_agent.sh \
  --id "ajan-id" \
  --name "İsim" \
  --emoji "⚙️" \
  --task "Görev tanımı"
```

### 创建的文件

脚本会自动生成以下文件：

- `IDENTITY.md` – 身份信息
- `SOUL.md` – 任务和行为规则
- `USER.md` – 用户信息
- `AGENTS.md` – 工作规则
- `TOOLS.md` – 工具
- `MEMORY.md` – 长期存储数据
- `HEARTBEAT.md` – （用于心跳检测，若关闭则为空文件）
- `cron/README.md` – Cron 脚本模板
- `cron/ornek.py` – 示例 Cron 脚本

## ⚡ 所有代理都具备的默认技能

每个新创建的代理都具备以下技能：

### 1. 网页搜索（使用 Brave API）

- 所有代理都可以进行网页搜索
- API 密钥：在 Gateway 配置中定义
- 使用方法：`web_search` 工具

### 2. 浏览器（Chromium）

每个代理都可以控制浏览器：

#### 截取屏幕截图：

```bash
# Browser snapshot
browser action=snapshot profile=openclaw targetUrl=https://orneksite.com
```

#### 浏览网页：

```bash
# Sayfa içeriğini çek
browser action=open profile=openclaw targetUrl=https://orneksite.com
browser action=snapshot profile=openclaw
```

#### 交互（点击、填写表单）：

```bash
browser action=act profile=openclaw request='{"kind": "click", "ref": "button-id"}'
browser action=act profile=openclaw request='{"kind": "type", "ref": "input-id", "text": "değer"}'
```

**注意：**
- `profile=openclaw` 用于独立浏览器；
- `profile=chrome` 用于操作现有的 Chrome 窗口。

### 3. 网页内容获取

- 用于获取简单的 HTML 内容（例如 API 响应）
- 使用方法：`web_fetch` 工具

### 4. Google Sheets（gog）

- 读写 Google Sheets 数据
- 使用方法：`gog` CLI

### 5. Cron 任务

- 每个代理都可以创建自己的 Cron 任务
- 相关文件会自动存储在 `cron/` 目录中

## 2. `/switch` 命令

用于切换代理：

```
/switch angarya
/switch main
```

### 其他切换方法

**通过 Telegram：**

- `angarya: <消息>` – 直接向代理发送消息
- `/pm angarya <消息>` – 同样功能

**作为子代理（Sub-agent）：**

- “让 Angarya 做……” – 可以通过此命令调用代理

## 3. 向代理发送任务

你可以通过我向其他代理发送任务：

```
Angarya'ya sor ne yapıyor
Angarya'ya şunu yaptır: çalışan servisleri kontrol et
```

## 4. 默认模型

新创建的代理会使用 OpenClaw 主代理的默认模型：

这些模型是 OpenClaw 自带的默认设置。安装此技能的用户将使用其自己的 OpenClaw 中的模型配置。

## 示例用法

| 命令                          | 说明                                      |
| --------------------------- | ----------------------------------------- |
| `/create_agent Muhasebeci`       | 创建一个名为“Muhasebeci”的新代理             |
| `/switch angarya`                | 切换到 Angarya 代理                         |
| `angarya: merhaba`               | 向 Angarya 发送消息                   |
| “Angarya, 你在做什么？”         | 查询 Angarya 的状态                   |
| “Angarya, 执行 ls -la”           | 向 Angarya 发送任务                   |

## 注意事项

- 创建的代理会自动添加到配置文件中
- 需要重启 Gateway：`/restart`