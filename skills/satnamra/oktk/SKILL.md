---
name: oktk
version: 2.4.0
description: **LLM Token Optimizer** – 将AI API的使用成本降低60%至90%。在将命令行输出（git、docker、kubectl等）发送给GPT-4/Claude之前对其进行压缩。该工具支持AI自动学习功能。开发者：Buba Draugelis 🇱🇹
author: Buba Draugelis
license: MIT
homepage: https://github.com/satnamra/openclaw-workspace/tree/main/skills/oktk
tags:
  - optimization
  - tokens
  - cost-savings
  - cli
  - filtering
  - llm
requires:
  bins:
    - node
openclaw:
  emoji: 🔪
  category: optimization
---

# oktk – 为大型语言模型（LLMs）设计的 CLI 输出压缩工具

## 问题

当你通过 AI 助手运行命令时，所有的输出内容都会被传递给大型语言模型（LLM）：

**每个输出生成的“令牌”都需要付费。过于详细的输出会浪费你的上下文窗口（即模型可使用的信息量）。**

## 解决方案

oktk 位于你的命令和大型语言模型之间，能够智能地压缩输出内容：

## 适用场景

当你通过 OpenClaw 运行支持的命令时，oktk 会自动执行压缩操作：

| 命令 | oktk 的作用 | 节省的令牌数量 |
|---------|----------------|:-------:|
| `git status` | 仅显示：分支名、进度（领先/落后）、文件数量 | **90%** |
| `git log` | 每条提交记录仅显示：哈希值、提交信息、作者 | **85%** |
| `git diff` | 显示摘要：修改的文件数量（+Y/-Z 行）、文件列表 | **80%** |
| `npm test` | 仅显示：测试结果（✅ 通过或 ❌ 失败）及通过的数量 | **98%** |
| `ls -la` | 按文件类型分组、显示文件大小、省略详细信息 | **83%** |
| `curl` | 显示状态码、关键头部信息以及截断后的响应内容 | **97%** |
| `grep` | 显示匹配次数及前 N 条匹配结果 | **80%** |
| `docker ps` | 显示容器列表（名称、镜像、状态） | **85%** |
| `docker logs` | 显示最后 N 行日志及错误数量 | **90%** |
| `kubectl get pods` | 显示 Pod 的状态及数量 | **85%** |
| `kubectl logs` | 显示最后 N 行日志及错误/警告数量 | **90%** |
| **任何命令** | oktk 会自动学习命令的输出模式（可选） | **约 70%** |

## 具体示例

### 使用 oktk 之前（800 个令牌被发送给大型语言模型）：
```
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   src/components/Button.jsx
        modified:   src/components/Header.jsx
        modified:   src/utils/format.js
        modified:   src/utils/validate.js
        modified:   package.json
        modified:   package-lock.json

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/components/Footer.jsx
        src/components/Sidebar.jsx
        tests/Button.test.js

no changes added to commit (use "git add" and/or "git commit -a")
```

### 使用 oktk 之后（80 个令牌被发送给大型语言模型）：
```
📍 main
↑ Ahead 3 commits
✏️  Modified: 6
❓ Untracked: 3
```

**相同的信息，但发送的令牌数量减少了 90%。**

## 技术原理

1. 在命令执行完成后拦截其输出。
2. 识别命令的类型（如 `git`、`npm`、`ls` 等）。
3. 为该命令应用相应的过滤规则。
4. 仅提取必要的信息。
5. 将处理后的结果缓存起来（相同命令会立即得到压缩后的结果，无需重新处理）。

### 安全性

oktk **绝不会干扰你的工作流程**：

**最坏的情况**：你仍然会收到完整的输出内容。
**最好的情况**：可以节省 90% 的令牌使用量。

## 使用方法

### 全局安装（推荐）

安装完成后，`oktk` 可以在整个系统中全局使用：

```bash
# Pipe any command through oktk
git status | oktk git status
docker ps | oktk docker ps
kubectl get pods | oktk kubectl get pods

# See your total savings
oktk --stats

# Bypass filter (get raw)
oktk --raw git status
```

### 使用 shell 别名（自动过滤）

将别名文件添加到 shell 配置中以实现自动过滤：

```bash
# Add to ~/.zshrc or ~/.bashrc
source ~/.openclaw/workspace/skills/oktk/scripts/oktk-aliases.sh
```

然后可以使用简短的别名来执行命令：

```bash
gst        # git status (filtered)
glog       # git log (filtered)
dps        # docker ps (filtered)
kpods      # kubectl get pods (filtered)

# Universal wrapper - filter ANY command
ok git status
ok docker ps -a
ok kubectl describe pod my-pod
```

### 与 OpenClaw 的集成

在使用 OpenClaw 的 `exec` 工具时，可以将输出结果通过 `oktk` 进行压缩处理：

**注意**：OpenClaw 目前还没有内置的输出压缩功能。
推荐的操作步骤是：
1. 将别名文件添加到 shell 配置中。
2. 对任何命令使用 `ok <命令>` 的形式进行调用。
3. 或者手动将命令输出通过管道传递给 `oktk`：`<命令> | oktk <命令>`。

## 实际节省效果示例

经过一周的正常使用后，可以显著节省令牌使用量：

```
📊 Token Savings
━━━━━━━━━━━━━━━━
Commands filtered: 1,247
Tokens saved:      456,789 (78%)

💰 At $0.01/1K tokens = $4.57 saved
```

## 安装方式

oktk 已经内置在 OpenClaw 的工作环境中；也可以单独安装：

```bash
clawhub install oktk
```

---

**本工具由我们在立陶宛（🇱🇹）精心开发。**