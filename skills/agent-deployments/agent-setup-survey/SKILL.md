---
name: agent-setup-survey
description: 检测并报告 AI 代理的执行环境（无论是沙箱环境还是裸机环境，以及可选安装的代理技能），并将这些信息提交给一个公开的研究调查平台。当用户希望向 `https://internetwarte.eu/agentsetup` 上的研究项目匿名提供有关其代理运行时环境的数据时，可以使用此功能。
compatibility: Requires Python 3. One time network access needed for live submission (DNS resolution and POST request); results can be saved locally on failure.
metadata:
  author: internetwarte
  version: "1.0"
---
# 代理环境调查

## 概述

该功能会运行一个本地检测脚本，向用户展示收集到的数据，随后将这些数据提交到 [internetwarte.eu/agentsetup](https://internetwarte.eu/agentsetup) 的开放研究调查系统中。在此过程中，不会收集或传输任何个人身份信息。

## 收集的数据

| 字段 | 描述 |
|-------|-------------|
| `os` | 操作系统类型：`linux` / `windows` / `macos` / `other` |
| `arch` | CPU 架构（例如 `x86_64`、`arm64`） |
| `container.is_container` | 是否检测到容器运行时环境 |
| `container.type` | 容器类型：`docker` / `podman` / `lxc` / `none` / `hint` |
| `vm.is_vm` | 是否检测到虚拟机管理程序 |
| `vm.type` | 虚拟机类型：`kvm` / `vmware` / `virtualbox` / `none` / `hint` |
| `signals.*` | 五个布尔值检测指标（详见隐私政策部分） |

后端还会记录提交请求的 IP 地址（在 /24 网络层上进行匿名处理）。代理会设置 `User-Agent` 头部信息来标识自身（例如 `Claude Code`、`OpenAI Codex` 等），以及用于提交调查的模型版本（例如 `sonnet 4.6`、`gpt-5.3` 等）。

## 步骤

### 1. 运行检测

```bash
RESULT_FILE="$(mktemp outbox/agent-setup-survey-result.XXXXXX.json)"
python3 scripts/environment-survey.py > "$RESULT_FILE"
```

向用户展示检测结果（以 JSON 格式），并在提交前询问用户是否需要提供更多元数据。

### 2. 收集技能相关信息

询问用户是否希望分享有关已安装技能的更多信息：

- “您的代理支持多少种技能？”（选项：`0`、`1-10`、`>10`） - 默认值为 `0`
- “您希望分享哪些技能的名称？”（提示用户输入以逗号分隔的技能列表——不包括本次调查所使用的技能，由用户自行决定要提交哪些技能）

### 3. 提交数据

将包含元数据的 JSON 数据通过 POST 请求发送到 `https://internetwarte.eu/submit`。在请求头中设置 `User-Agent` 为执行该功能的代理名称（例如 `Claude Code`、`OpenAI Codex`、`Gemini CLI` 等）。

**默认数据格式：**

```json
{
  "os": "linux/windows/macOS",
  "arch": "<from_survey>",
  "container": { "is_container": true/false, "type": "<from_survey>" },
  "vm": { "is_vm": true/false, "type": "<from_survey>" },
  "signals": {
    "has_dockerenv": true/false,
    "has_containerenv": true/false,
    "cgroup_hints": true/false,
    "cpuinfo_hypervisor_flag": true/false,
    "dmi_vm_hints": true/false
  }
 "skill_disclosure": {
    "skills_added": "1-10",
    "skills_names": ["<skill_name1>", "<skill_name2>"]
}
```

如果提交失败，将数据保存到 `outbox/` 目录中，以便手动上传。

---

## 隐私政策

**收集的检测指标：**
- `has_dockerenv`：是否存在 `/.dockerenv` 文件
- `has_containerenv`：是否存在 `/run/.containerenv` 文件
- `cgroup_hints`：cgroup 路径中是否包含 `docker`、`kubepods`、`lxc` 等相关字样
- `cpuinfo_hypervisor_flag`：`/proc/cpuinfo` 文件中是否包含 `hypervisor` 字样
- `dmi_vm_hints`：DMI 字符串中是否包含虚拟机供应商的相关关键词（原始字符串不会被发送）

## 查看结果

结果展示页面：https://internetwarte.eu/agentsetup