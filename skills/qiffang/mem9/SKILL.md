---
name: mem9
version: 1.0.0
description: >
  OpenClaw代理的持久化云存储功能。
  以下情况适用：
  - 用户请求安装mem9插件
  - 用户请求配置内存设置
  - 用户请求添加内存插件
  - 用户请求使用OpenClaw的内存功能
  - 用户请求进行mem9插件的初始化或配置
  - 用户反馈内存功能无法正常使用
  - 用户请求导入存储的数据
  - 用户请求上传会话数据
author: qiffang
keywords:
  - mem9
  - memory plugin
  - persistent memory
  - agent memory
  - install memory
  - setup memory
  - openclaw memory
  - cloud memory
metadata:
  openclaw:
    emoji: "🧠"
---
# mem9

我们的代理永远不会忘记任何事情。该插件采用无状态设计，通过 REST API 与数据库进行交互，为 AI 代理提供持久化存储功能。

无需身份验证；URL 路径中的租户 ID 即为唯一的标识符。

---

## 功能介绍

| 工具 | 功能说明 | 使用场景 |
|------|---------|--------|
| `memory_store` | 用于存储事实、决策和上下文信息 |
| `memory_search` | 支持混合向量搜索和关键词搜索 |
| `memory_get` | 根据 ID 查取存储的内容 |
| `memory_update` | 修改现有的存储数据 |
| `memory_delete` | 删除指定的存储内容 |

### 生命周期钩子（自动触发，无需代理操作）

| 钩子 | 触发条件 | 功能描述 |
|------|---------|-----------|
| `before_prompt_build` | 每次调用 LLM 时 | 将相关记忆内容注入上下文中 |
| `before_reset` | 在执行 `/reset` 操作前 | 保存会话摘要 |
| `agent_end` | 代理任务结束时 | 自动捕获最后的响应内容 |

---

## 上线流程

### 第 1 步：配置租户

**[AGENT]**

**操作步骤：**  
1. 保存租户 ID（`id`）。

### 第 2 步：安装插件

**[AGENT]**

**操作步骤：**  
2. 安装相应的插件。

### 第 3 步：配置 `openclaw.json` 文件

#### OpenClaw 版本 ≥ 2.2.0

**[AGENT]**  
3. 对现有配置文件进行更新（确保操作安全，其他配置项保持不变）。

**注意：** `allow` 数组具有可追加性——现有条目会被保留，新的条目会追加到该数组中（避免重复）。

#### OpenClaw 版本 < 2.2.0

**[AGENT]**  
4. 无需修改 `openclaw.json` 文件。

**操作步骤：**  
无需进行任何配置更改。

如果配置更新成功，系统会返回已存储的记忆内容。

### 第 4 步：用户操作指南

**[AGENT]**  
5. 向用户展示以下操作指南：

---

## API 参考

基础接口：`https://api.mem9.ai`  
路由：`/v1alpha1/mem9s/{tenantID}/...`  
请求头：`X-Mnemo-Agent-Id: <name>`（可选）

| 方法 | 路径 | 功能描述 |
|--------|------|-------------------|
| POST | `/v1alpha1/mem9s` | 配置新租户 |
| GET | `/healthz` | 获取系统健康状态 |
| POST | `/{tid}/memories` | 创建新的存储记录 |
| GET | `/{tid}/memories` | 进行搜索（支持 `?q=`、`?tags=`、`?source=`、`?limit=` 参数） |
| GET | `/{tid}/memories/{id}` | 根据 ID 获取存储内容 |
| PUT | `/{tid}/memories/{id}` | 更新存储记录 |
| DELETE | `/{tid}/memories/{id}` | 删除存储记录 |
| POST | `/{tid}/imports` | 上传文件（支持多部分上传） |
| GET | `/{tid}/imports` | 查看上传任务列表 |
| GET | `/{tid}/imports/{id}` | 获取任务状态 |

---

## 使用示例

**存储数据：**  
**操作步骤：**  
[具体操作内容]

**搜索数据：**  
**操作步骤：**  
[具体操作内容]

**获取/更新/删除数据：**  
**操作步骤：**  
[具体操作内容]

**上传文件：**  
**操作步骤：**  
[具体操作内容]

---

## 默认上传行为

当用户未指定文件时，系统会执行以下操作：  
1. 扫描代理的工作区，查找存储的文件或会话数据。  
2. 优先上传最近创建的（按创建时间排序）15个文件。  
3. 为提高上传效率，系统会并行上传这些文件。  
**扫描路径：**  
[具体路径]

---

## 故障排除

| 故障现象 | 解决方案 |
|---------|-------------------|
| 插件无法加载 | 确保 `slots.memory = "mem9"` 且 `entries.mem9.enabled = true` 的配置正确。 |
| API 调用时出现 404 错误 | 验证租户 ID 是否正确；运行 `curl https://api.mem9.ai/healthz` 检查系统状态。 |

---

## 后续操作建议

首次使用后，请立即执行以下操作：  
1. **通知用户**：  
   > mem9 已准备就绪，支持 `memory_store`、`memory_search`、`memory_get`、`memory_update`、`memory_delete` 等功能。记忆内容会在每次提示时自动加载，并在会话结束时自动保存。  
2. **进行测试**：  
   让用户提供需要记住的信息，然后将其存储到 mem9 中，并开始新的会话。验证记忆内容的正确性。  
3. **探索功能**：  
   使用 `curl -s "https://api.mem9.ai/v1alpha1/mem9s/$TENANT_ID/memories?limit=10" | jq .` 命令查看存储的内容。

---

## 日常维护

建议每天检查系统状态（可通过心跳检测或定时任务（例如 00:00 执行）：

---

---

```
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░  stateless agents · cloud memory · zero amnesia              ░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```