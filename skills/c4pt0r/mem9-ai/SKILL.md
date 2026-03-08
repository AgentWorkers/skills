---
name: mem9
version: 1.0.0
description: >
  OpenClaw代理的持久化云存储功能。
  适用场景：
  - 当用户请求执行以下操作时：
    - “安装mem9”
    - “配置内存”
    - “添加内存插件”
    - “管理OpenClaw的内存资源”
    - “进行mem9的初始化设置”
    - “报告内存使用异常”
    - “导入存储的数据”
    - “上传会话数据”
  相关术语说明：
  - mem9：一种用于管理OpenClaw代理内存资源的插件或工具。
  - memory plugin：用于扩展OpenClaw内存管理功能的插件。
  - OpenClaw memory：指OpenClaw系统本身提供的内存管理接口或功能。
  - memory not working：表示内存相关功能出现故障或无法正常使用。
  - import memories：从外部源导入存储的数据或配置信息。
  - upload sessions：将当前会话数据上传到云端存储。
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

我们的代理永远不会忘记任何事情。该插件采用无状态设计，通过 REST API 与数据库进行交互，为 AI 代理提供持久化的存储空间。

无需身份验证；URL 路径中的租户 ID 即为唯一的标识符。

---

## 功能介绍

| 工具 | 功能 | 适用场景 |
|------|------|---------|
| `memory_store` | 保存事实、决策和上下文信息 |
| `memory_search` | 支持混合向量搜索和关键词搜索 |
| `memory_get` | 根据 ID 获取数据 |
| `memory_update` | 修改现有数据 |
| `memory_delete` | 删除数据 |

### 生命周期钩子（自动触发，无需代理操作）

| 钩子 | 触发条件 | 功能描述 |
|------|---------|-------------|
| `before_prompt_build` | 每次调用大型语言模型（LLM）时 | 将相关记忆信息注入上下文中 |
| `before_reset` | 在执行 `reset` 操作之前 | 保存会话摘要 |
| `agent_end` | 代理任务结束时 | 记录最后的响应内容 |

---

## 上手指南

### 第一步：配置租户

`[AGENT]`

---  
（配置租户信息的代码块）  

**响应：**  
（保存租户 ID 的代码块）  

### 第二步：安装插件

`[AGENT]`

---  
（安装插件的代码块）  

### 第三步：配置 openclaw.json

#### OpenClaw ≥ 2.2.0

`[AGENT]`  
（安全地修改现有配置文件，保留其他配置项）  

---  
**注意：** `allow` 数组是可追加的——现有条目会被保留，新条目会追加到列表中（避免重复）。  

如果系统中没有 `openclaw.json` 文件，则需要创建该文件：  

---  
（创建 openclaw.json 文件的代码块）  

#### OpenClaw < 2.2.0

`[AGENT]`  
（此版本不需要 `allow` 数组）  

---  
如果系统成功返回了存储的信息，说明配置完成。  

### 第四步：后续操作

`[AGENT]`  
向用户显示以下信息：  

---  
（向用户展示操作指引的代码块）  

---

## API 参考

基础地址：`https://api.mem9.ai`  
路由：`/v1alpha1/mem9s/{tenantID}/...`  
请求头：`X-Mnemo-Agent-Id: <name>`（可选）  

| 方法 | 路径 | 功能描述 |
|--------|------|-------------|
| POST | `/v1alpha1/mem9s` | 配置新租户 |
| GET | `/healthz` | 检查系统状态 |
| POST | `/{tid}/memories` | 创建新的记忆记录 |
| GET | `/{tid}/memories` | 搜索记忆记录（支持 `?q=`, `?tags=`, `?source=`, `?limit=`） |
| GET | `/{tid}/memories/{id}` | 根据 ID 获取记忆记录 |
| PUT | `/{tid}/memories/{id}` | 更新记忆记录 |
| DELETE | `/{tid}/memories/{id}` | 删除记忆记录 |
| POST | `/{tid}/imports` | 上传文件（支持多部分数据） |
| GET | `/{tid}/imports` | 查看上传任务列表 |
| GET | `/{tid}/imports/{id}` | 查看任务状态 |

---

## 使用示例

**存储数据：**  
---  
（存储数据的代码块）  

**搜索数据：**  
---  
（搜索数据的代码块）  

**获取/更新/删除数据：**  
---  
（获取/更新/删除数据的代码块）  

**上传文件：**  
---  
（上传文件的代码块）  

---

## 默认上传行为

当用户未指定文件时，系统会执行以下操作：  
1. 扫描代理的工作区，查找记忆或会话相关文件。  
2. 上传最近创建的 **15 个** 文件（按创建时间排序）。  
3. 为了提高上传速度，系统会并行上传这些文件。  
   **扫描路径：**  
---  
（指定文件扫描路径的代码块）  

---

## 故障排除

| 故障现象 | 解决方案 |
|---------|-----|
| 插件无法加载 | 确保 `slots.memory = "mem9"` 且 `entries.mem9.enabled = true` 的配置正确。 |
| API 调用时出现 404 错误 | 验证租户 ID；运行 `curl https://api.mem9.ai/healthz` 检查系统状态。 |

---

## 下一步操作

初次使用后，请立即执行以下操作：  
1. **通知用户**：  
   > mem9 已准备好使用。支持 `memory_store`, `memory_search`, `memory_get`, `memory_update`, `memory_delete` 功能。记忆信息会在每次提示时自动加载，在会话结束时自动保存。  
2. **进行测试**：  
   让用户提供需要记住的内容，然后保存该信息，并开始新的会话。验证系统是否能够正确回忆该内容。  
3. **探索功能**：  
   使用 `curl -s "https://api.mem9.ai/v1alpha1/mem9s/$TENANT_ID/memories?limit=10" | jq .` 来查看存储的记忆记录。  

---

## 更新说明

建议每天检查系统配置（可以通过心跳检测或定时任务在 00:00 自动执行更新操作）：  

---  
（更新配置的代码块）  

---  
```
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░  stateless agents · cloud memory · zero amnesia              ░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```