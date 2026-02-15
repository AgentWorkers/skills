---
name: clawion
description: 多代理协作由 OpenClaw 定时任务（cron jobs）和 clawion CLI（基于唤醒事件的工作流管理系统）驱动。
---

# Clawion（运行手册）

Clawion是一个基于文件的任务协调工具。代理通过`clawion`命令行界面（CLI）与系统状态进行交互。

仓库地址：https://github.com/natllian/clawion

## 工作原理

Clawion采用“唤醒驱动”（wake-driven）机制——OpenClaw的定时任务（cron jobs）是整个系统的核心驱动器。

1. 定时任务会定期触发一次执行。
2. 代理运行`clawion agent wake`命令，以接收当前轮次的指令。
3. 代理根据`Turn Playbook`（轮次脚本）执行相应的操作。
4. 代理通过发送消息或执行具体任务来响应系统。
5. 下一次定时任务执行时，系统状态会更新。

**重要特性：**
- **`clawion`是唯一的读取入口点**。
- **未读消息会自动标记为“未读”状态，并在用户查看时自动确认**。

## 核心原则

- **工作者负责完成任务；管理者负责维护任务调度**：
  - 工作者通过`message add`报告进度或提出问题，通过`working add`记录日志。
  - 管理者通过`task create/assign/update`来分配和更新任务，并通过`working add`记录日志。任务完成后，系统会自动停止所有相关的定时任务。
- **每个操作都需要明确指定代理ID（`--agent <agentId>`）**。

---

## 快速入门（创建新任务）

### 0. 预备工作

确认`clawion` CLI是否可用：

```bash
clawion --help
```

如果找不到该命令，请按照[Clawion的README文件](https://github.com/natllian/clawion#readme)中的说明进行安装。

### 1. 创建任务

```bash
clawion mission create --id <MISSION_ID> --name "..."
```

### 2. 注册管理者（设置启动规则）

执行`--agent`命令的必须是管理者本人。

```bash
clawion agent add \
  --mission <MISSION_ID> \
  --id <MANAGER_ID> \
  --name "Manager" \
  --system-role manager \
  --role-description "..." \
  --agent <MANAGER_ID>
```

### 3. 注册工作者代理

```bash
clawion agent add \
  --mission <MISSION_ID> \
  --id <WORKER_ID> \
  --name "Worker" \
  --system-role worker \
  --role-description "..." \
  --agent <MANAGER_ID>
```

重复上述步骤，为每个工作者分别注册代理。

### 4. 创建并分配任务（仅限管理者）

```bash
clawion task create \
  --mission <MISSION_ID> \
  --id <TASK_ID> \
  --title "..." \
  --description "..." \
  --agent <MANAGER_ID>

clawion task assign \
  --mission <MISSION_ID> \
  --task <TASK_ID> \
  --to <WORKER_ID> \
  --agent <MANAGER_ID>
```

### 5. 编写任务计划（仅限管理者，且只能执行一次）

```bash
clawion mission roadmap --id <MISSION_ID> --set "<markdown>" --agent <MANAGER_ID>
```

任务计划只能通过CLI编写一次。后续的修改必须通过Web UI由人工完成。

### 6. 创建定时任务（默认为禁用状态）并获取用户批准

为每个代理创建一个定时任务（管理者及所有工作者各一个），所有任务默认处于禁用状态。在启用任何定时任务之前，需在Clawion Web UI中获取用户的批准。有关任务配置的详细信息，请参阅[OpenClaw的定时任务设置](#cron-jobs-openclaw)。

**Web UI审核内容：**
- 任务计划（可编辑）
- 每个代理的角色描述（可编辑）
- 保密信息处理设置（确保保密信息不会泄露到通信中）

只有在获得用户明确批准后，才能启用定时任务。

---

## OpenClaw的定时任务规则

### 基本规则

| 规则                          | 详细说明                                                                                                                         |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **任务隔离**                     | 每个定时任务都在独立的OpenClaw会话中运行（严禁在主会话中执行）。会话间的数据共享可能导致运行不稳定。                                      |
| **定时间隔**                     | 如果用户未指定间隔，请在创建任务前询问并确认。                                                     |
| **消息内容限制**                   | 禁止在任务消息中嵌入任务上下文、任务列表或操作指南内容。这些信息由`clawion agent wake`在运行时从系统状态中获取。                         |
| **任务默认为禁用状态**                 | 所有定时任务创建时都处于禁用状态。只有在用户通过Web UI审核后才能启用。                                         |

### 推荐的定时任务消息格式

**工作者发送的消息：**
```text
Fetch your instructions by running:

clawion agent wake --mission <MISSION_ID> --agent <AGENT_ID>

Then follow the Turn Playbook in that output.
```

**管理者发送的消息：**
```text
Fetch your instructions by running:

clawion agent wake --mission <MISSION_ID> --agent <AGENT_ID>

Then follow the Turn Playbook in that output.
If the mission is complete, disable all related cron jobs.
```

### 运营建议

- **任务命名格式**：
  - `clawion:<MISSION_ID>:manager:<AGENT_ID>`
  - `clawion:<MISSION_ID>:worker:<AGENT_ID>`
- **避免多个代理同时执行**：如果多个代理使用相同的定时间隔，应设置不同的执行时间点，例如：`round(i * N / K)`（其中`i = 0..K-1`）。
  - 例如：`N=10`，`K=3`时，执行时间点为`0分钟`、`3分钟`、`7分钟`。