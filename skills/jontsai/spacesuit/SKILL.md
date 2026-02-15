# openclaw-spacesuit

**OpenClaw工作空间的框架支架**

## 元数据

| 字段 | 值 |
|-------|-------|
| **名称** | `spacesuit` |
| **版本** | `0.3.0` |
| **作者** | jontsai |
| **许可证** | MIT |
| **类别** | 框架 |
| **标签** | 工作空间、支架、规范、内存管理、Git工作流程 |

## 说明

Spacesuit是一个为OpenClaw工作空间设计的框架层，它包含以下功能：

- **会话启动协议** — 以安全为首要考虑的文件加载顺序
- **内存管理系统** — 每日日志记录以及经过管理的长期内存存储（遵循提交规范）
- **Git工作流程** — 强制性的提交前检查、工作树规范、并行代理协调
- **安全规则** — 行动前的检查清单、防止破坏性操作的机制、紧急停止协议
- **优先级系统** — 任务和事件的P0–P5等级分类
- **跨平台信息传递** — 在Slack/Discord/Telegram之间结构化地传递信息
- **心跳检测框架** — 定期主动检查并跟踪系统状态
- **决策记录** — 对架构决策进行强制性的审计跟踪
- **元学习框架** — 以专家为中心的研究方法（考虑了“邓宁-克鲁格效应”）
- **安全基线** — 保密传输政策、防止代码注入的防护措施、数据分类

## 安装

```bash
# First-time install (creates workspace files with markers)
make init

# Upgrade existing workspace (replaces only SPACESUIT sections)
make upgrade
```

## 工作原理

OpenClaw会从工作空间根目录读取硬编码的文件名（如`AGENTS.md`、`SOUL.md`等）。由于无法更改这种加载方式，Spacesuit采用了**基于章节的合并机制**：

1. 框架内容被包裹在`<!-- SPACESUIT:BEGIN -->`和`<!-- SPACESUIT:END -->`标记之间
2. 升级时，只有这些标记之间的内容会被替换
3. 标记之外的所有内容（即您的自定义设置）都将被保留

## 管理的文件

| 文件 | 基础内容 | 用户自定义内容 |
|------|-------------|--------------|
| `AGENTS.md` | 会话协议、内存管理、Git配置、安全规则 | 频道映射、工具配置、个人规则 |
| `SOUL.md` | 核心框架配置 | 个人风格、特定于用户的沟通方式 |
| `TOOLS.md` | 工具组织指南 | 实际工具配置、凭证信息、API详细信息 |
| `HEARTBEAT.md` | 检查框架及状态跟踪 | 需要执行的特定检查 |
| `IDENTITY.md` | （仅模板） | 用户名称、头像、个人风格 |
| `USER.md` | （仅模板） | 用户相关信息 |
| `MEMORY.md` | 长期内存存储结构 | 项目笔记、个人上下文信息 |
| `SECURITY.md` | 完整的安全基线设置 | 针对不同联系人的警报通道 |
| `Makefile` | （仅模板） | 系统管理相关配置 |

## 升级流程

```bash
# See what would change
./scripts/diff.sh

# Apply upgrade
./scripts/upgrade.sh

# Check version
cat skills/spacesuit/VERSION
```