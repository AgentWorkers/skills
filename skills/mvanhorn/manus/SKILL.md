---
name: manus
description: 通过Manus API创建和管理AI代理任务。Manus是一个自主的AI代理，它可以浏览网页、使用各种工具，并完成完整的工作成果。
homepage: https://manus.im
user-invocable: true
disable-model-invocation: true
metadata:
  clawdbot:
    emoji: "🤖"
    primaryEnv: MANUS_API_KEY
    requires:
      bins: [curl, jq]
      env: [MANUS_API_KEY]
---

# Manus AI Agent

用于为自主AI代理Manus创建任务，并检索已完成的工作成果。

## 认证

请将`MANUS_API_KEY`环境变量设置为从[manus.im](https://manus.im)获取的API密钥。

---

## 命令

所有命令均通过`scripts/manus.sh`脚本执行。

### 创建任务

```bash
{baseDir}/scripts/manus.sh create "Your task description here"
{baseDir}/scripts/manus.sh create "Deep research on topic" manus-1.6-max
```

可用配置文件：`manus-1.6`（默认）、`manus-1.6-lite`（快速）、`manus-1.6-max`（详细）。

### 检查任务状态

```bash
{baseDir}/scripts/manus.sh status <task_id>
```

返回状态：`pending`（待处理）、`running`（运行中）、`completed`（已完成）或`failed`（失败）。

### 等待任务完成

```bash
{baseDir}/scripts/manus.sh wait <task_id>
{baseDir}/scripts/manus.sh wait <task_id> 300  # custom timeout in seconds
```

持续轮询任务状态，直到任务完成或超时（默认超时时间为600秒）。

### 获取任务详情

```bash
{baseDir}/scripts/manus.sh get <task_id>
```

返回包含任务状态和输出结果的完整JSON数据。

### 列出输出文件

```bash
{baseDir}/scripts/manus.sh files <task_id>
```

显示每个输出文件的名称及下载链接。

### 下载输出文件

```bash
{baseDir}/scripts/manus.sh download <task_id>
{baseDir}/scripts/manus.sh download <task_id> ./output-folder
```

将所有输出文件下载到指定目录（默认为当前目录）。

### 列出所有任务

```bash
{baseDir}/scripts/manus.sh list
```

---

## 典型工作流程

1. **创建任务**：`manus.sh create "yourprompt"`
2. **等待任务完成**：`manus.sh wait <task_id>`
3. **下载结果**：`manus.sh download <task_id>`

---

## 高级API功能

有关文件附件、Webhook、连接器、多轮对话和交互模式等功能，请参阅Manus的完整API文档：

- API参考：https://open.manus.ai/docs
- 主要文档：https://manus.im/docs

---

## 安全性与权限

**该工具的功能：**
- 将任务提示发送到`api.manus.ai`接口。
- 轮询任务完成情况，并从Manus的CDN服务器下载输出文件。
- API密钥仅通过`API_KEY`头部发送至`api.manus.ai`。

**该工具不支持的功能：**
- 不支持上传本地文件（文件上传属于高级API功能，未包含在默认脚本中）。
- 不支持注册Webhook或连接外部账户。
- 不会将API密钥发送到除`api.manus.ai`之外的任何端点。
- 不会修改本地系统配置。
- 该工具不能被代理自动执行（`disable-model-invocation: true`设置为true时有效）。
- 必须手动触发每个任务。

**包含的脚本：`scripts/manus.sh`（Bash脚本，使用`curl`和`jq`工具）**

首次使用前，请务必查看`scripts/manus.sh`脚本以确认其功能是否符合预期。