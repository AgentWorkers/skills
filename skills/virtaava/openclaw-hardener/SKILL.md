---
name: openclaw-hardener
description: "加固 OpenClaw（工作区及 ~/.openclaw 目录）：执行 OpenClaw 安全审计，识别命令注入（prompt-injection）和数据泄露（exfil）风险，扫描系统中是否存在敏感信息，并应用相应的安全修复措施（如修改文件权限或清理可执行文件的执行权限）。此外，还提供了可选的配置补丁（config.patch）计划，以进一步降低系统被攻击的风险。"
---

# OpenClaw Hardener

此工具提供了一种**用户可选**的强化功能，可以：

- 运行 OpenClaw 内置的安全审计工具（`openclaw security audit --deep` / `--fix`）。
- 检查工作区的安全状况（例如：是否存在未授权的可执行文件、多余的 `.env` 文件、不安全的序列化模式等）。
- 仅在用户明确请求的情况下，应用安全的修复措施。
- 生成（并可选地应用）一个 **Gateway `config.patch` 计划**，以加强运行时的安全策略。

## 运行该工具

脚本路径：
`skills_live/openclaw-hardener/scripts/hardener.py`

**使用示例：**

```bash
# Read-only checks (recommended default)
python3 skills_live/openclaw-hardener/scripts/hardener.py check --all

# Only run OpenClaw built-in audit (deep)
python3 skills_live/openclaw-hardener/scripts/hardener.py check --openclaw

# Only run workspace checks
python3 skills_live/openclaw-hardener/scripts/hardener.py check --workspace

# Apply safe fixes (chmod/exec-bit cleanup + optionally openclaw audit --fix)
python3 skills_live/openclaw-hardener/scripts/hardener.py fix --all

# Generate a config.patch plan (prints JSON5 patch)
python3 skills_live/openclaw-hardener/scripts/hardener.py plan-config

# Apply the plan (requires a running gateway; uses `openclaw gateway call`)
python3 skills_live/openclaw-hardener/scripts/hardener.py apply-config
```

## 设计规则（请遵守）：

- **默认设置为仅检查**。除非用户执行 `fix` 或 `apply-config` 命令，否则不会修改任何文件或配置。
- **输出结果中不得包含敏感信息**。如果脚本检测到敏感路径，必须对相关数据进行脱敏处理。
- **必须明确显示补丁内容**。在应用补丁之前，必须向用户展示具体的补丁内容。

## 检查/修复的内容：

### OpenClaw 内置的安全审计
- 运行 `openclaw security audit --deep`（在 `fix` 模式下还会执行修复操作）。

### 工作区安全检查（检查范围：工作区及 `~/.openclaw` 目录）
- 检查 `~/.openclaw` 目录下的权限设置是否合理。
- 确认非可执行文件类型中是否存在未授权的可执行文件。
- 检查是否存在多余的 `.env` 文件（警告）或被跟踪的 `.env` 文件（视为错误）。
- 通过启发式方法检测脚本中的不安全序列化模式或其他风险。

### 配置强化（可选计划）
生成一个保守的 `config.patch` 模板，主要关注以下方面：
- 加强对传入数据的访问控制（仅在使用 `pairing/allowlist` 策略时进行）。
- 确保敏感日志数据被正确脱敏。

（具体需要修改的配置项取决于您的实际设置；该补丁计划仅供参考，建议在使用前仔细审查。）