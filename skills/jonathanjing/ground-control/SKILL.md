---
name: ground-control
description: OpenClaw升级后的验证系统：该系统定义了一个用于验证结果的模型/定时任务/通道基准文件，并构建了一个包含五个阶段的自动化验证流程（配置完整性验证、API密钥有效性验证、定时任务配置有效性验证、会话连接稳定性测试以及通道连接稳定性测试）。在检测到配置或定时任务配置出现偏差时，系统能够自动进行修复。
version: "0.3.5"
metadata:
  author: JonathanJing
  tags: [ops, verification, upgrade, config, cron, health]
  license: MIT
  credentials: none
---
# 地面控制（Ground Control）

这是一个用于 OpenClaw 的升级后验证工具，可确保系统在每次升级后仍保持正常运行状态。

## 🛠️ 安装

### 1. 推荐使用 OpenClaw 的命令行界面
只需向 OpenClaw 发送指令：“*Install the ground-control skill.*”，代理会自动完成安装和配置。

### 2. 手动安装（通过 CLI）
如果您更喜欢使用终端，请运行以下命令：
```bash
clawhub install ground-control
```

## 权限与权限要求

该工具需要 OpenClaw 具备以下功能：
- **`gateway config.get`** — 读取当前配置（所有阶段）
- **`gateway config.patch`** — 自动修复配置差异（仅限第 1 阶段）
- **`cron list` / `cron update`** — 验证并自动修复 cron 作业（第 3 阶段）
- **`sessions_spawn`** — 启动测试会话（第 2、4、5 阶段）
- **`message send`** — 发送消息以测试通道是否正常运行，并生成汇总报告（第 5 阶段）

**自动修复机制：** 第 1 和第 3 阶段会自动修复配置或 cron 作业，使其与预设的 `GROUND_TRUTH` 值一致。使用 `--dry-run` 选项可禁用自动修复功能，仅进行报告生成。

**安全与数据保护：** 该工具遵循“零秘密日志记录”（Zero-Secret Logging）协议：
- **即时数据删除**：获取运行时配置后，敏感数据（如认证信息、插件相关数据）会立即从内存中清除。
- **敏感数据替换**：敏感字段中的不一致之处会以 `[REDACTED_SENSITIVE_MISMATCH]` 的形式显示。
- **功能验证**：API 密钥通过功能调用进行验证，而非直接比较。
- **无数据持久化**：任何敏感信息都不会被写入内存或消息通道中。

## 使用场景：
- 在执行 `openclaw update` 或 `npm install -g openclaw@latest` 之后
- 当怀疑配置发生异常（如模型变更、cron 作业故障、通道中断等）时
- 通过 `/verify` 命令定期进行系统健康检查

## 设置步骤：
1. 将 `templates/MODEL_GROUND_TRUTH.md` 复制到工作区的根目录。
2. 替换文件中的配置值（模型信息、cron 作业内容、通道设置等）为实际值。
3. 将 `GROUND_TRUTH` 的同步规则添加到 `AGENTS.md` 文件中（详见 README 文件）。
4. 运行 `/verify` 命令进行测试。

## 相关文件：
- `templates/MODEL_GROUND_TRUTH.md` — 基准配置模板（复制到工作区根目录）
- `scripts/post-upgrade-verify.md` — 用于执行五阶段验证的代理脚本
- `scripts/UPGRADE_SOP.md` — 升级标准操作流程