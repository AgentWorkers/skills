---
name: Write
description: 规划、起草、编写内容，并对其进行版本控制和质量审核。
metadata: {"clawdbot":{"emoji":"✍️","os":["linux","darwin"]}}
---

## 设置

首次使用时，请创建工作区：
```bash
./scripts/init-workspace.sh ~/writing
```

## 工作流程

```
Request → Plan → Draft → Audit → Refine → Deliver
```

**规则：**
- 将所有写作任务委托给子代理——主要负责人专注于其他工作；
- **严禁** 直接编辑文件——请使用 `./scripts/edit.sh`（该脚本会自动维护文件版本控制）；
- 在提交任何较长的内容之前，必须先运行质量审核（详见 `audit.md`）；
- 只有在用户确认内容最终确定后，才进行文件清理。

## 配置

配置信息存储在 `config.json` 中：
- `depth`: "quick" | "standard" | "thorough" —— 控制研究深度和修订次数；
- `auto_audit`: true/false —— 草稿完成后是否自动运行质量审核。

## 脚本（强制执行）

| 脚本 | 功能 |
|--------|---------|
| `init-workspace.sh` | 创建项目结构 |
| `new-piece.sh` | 以指定 ID 开始新的写作任务 |
| `edit.sh` | 进行编辑操作，并自动备份文件版本 |
| `audit.sh` | 运行质量审核并生成报告 |
| `list.sh` | 显示所有写作任务及其版本信息 |
| `restore.sh` | 恢复文件的先前版本 |
| `cleanup.sh` | 在用户确认后删除旧版本 |

参考文档：`brief.md`（用于规划）、`execution.md`（用于起草）、`verification.md`（用于质量检查）、`state.md`（用于跟踪进度）、`research.md`（用于资料调研）、`versioning.md`（用于版本管理规则）、`audit.md`（用于审核标准）、`criteria.md`（用于设置偏好）。相关脚本位于 `scripts/` 目录下：`scripts/init-workspace.sh`、`scripts/new-piece.sh`、`scripts/edit.sh`、`scripts/audit.sh`、`scripts/list.sh`、`scripts/restore.sh`、`scripts/cleanup.sh`。

---

### 偏好设置
<!-- 用户的写作偏好设置 -->

### 禁止的操作
<!-- 用户不允许执行的操作 -->

---
*空白部分表示需要根据实际情况填写。*