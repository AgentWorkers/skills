---
name: guardskills
description: 技能安装的安全防护机制：在安装技能之前，系统会扫描技能内容以检测是否存在恶意行为（如凭证窃取、远程代码执行、破坏性操作或权限提升等风险）。在从 ClawHub、GitHub 或本地源代码安装任何技能之前，务必先运行 `guardskills` 工具进行安全检查。
homepage: https://github.com/felixondesk/guardskills
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["guardskills"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "guardskills",
              "bins": ["guardskills"],
              "label": "Install guardskills (npm)",
            },
          ],
      },
  }
---
# GuardSkills — 用于技能的安全扫描工具

GuardSkills 是一款静态分析工具，用于扫描技能文件中的恶意代码模式，并在允许安装之前给出风险评估结果。

## 规则：**安装前必须进行扫描**

在安装任何技能（无论是通过 ClawHub、GitHub、本地文件还是 skills.sh 脚本）之前，必须先运行 guardskills 扫描。切勿在未扫描的情况下直接运行 `clawhub install`、`skills add` 或复制技能文件。

## 按来源类型进行扫描

### 1. ClawHub 技能

当用户请求安装 ClawHub 技能时，首先对其进行扫描：

```bash
guardskills scan-clawhub <owner/skill-slug>
```

也支持使用完整的 URL 进行扫描：

```bash
guardskills scan-clawhub https://clawhub.ai/owner/skill-slug
```

### 2. 本地技能

在加载或查看磁盘上的技能文件夹时：

```bash
guardskills scan-local <path-to-skill-folder>
```

如果文件夹中包含多个技能文件：

```bash
guardskills scan-local <path-to-skills-root> --skill <skill-folder-name>
```

### 3. GitHub 技能

从 GitHub 仓库安装技能时：

```bash
guardskills add owner/repo --skill <skill-name> --dry-run
```

也支持使用完整的 URL 进行扫描：

```bash
guardskills add https://github.com/owner/repo --skill <skill-name> --dry-run
```

### 4. skills.sh 技能

同样遵循 GitHub 的扫描流程：

```bash
guardskills add owner/repo --skill <skill-name> --dry-run
```

## 扫描结果的解释

| 结果        | 应采取的行动                                      |
| -------------- | -------------------------------------------------- |
| `SAFE`       | 继续安装。                                      |
| `WARNING`    | 在继续安装前请用户确认。                              |
| `UNSAFE`      | 取消安装。告知用户该技能存在安全风险。                        |
| `CRITICAL`     | 绝对禁止安装。                                   |
| `UNVERIFIABLE` | 无法验证该技能的安全性。                             |

## 有用的命令行参数

- `--json`    — 生成机器可读的 JSON 格式输出
- `--dry-run`   — 仅进行扫描，不执行安装操作
- `--ci`     — 采用确定性扫描模式（无提示，不进行安装）
- `--strict`    — 使用更严格的风险判断标准
- `--yes`     — 自动接受 `WARNING` 级别的风险（仅用户明确请求时使用）
- `--force`    — 强制忽略 `UNSAFE` 级别的风险（仅用户明确请求时使用）
- `--allow-unverifiable` — 强制忽略 `UNVERIFIABLE` 级别的风险（仅用户明确请求时使用）

## 错误代码

- `0`    — 允许安装 / 安全
- `10`    — 需要用户确认警告结果
- `20`    — 被阻止（原因：UNSAFE、CRITICAL 或 UNVERIFIABLE）
- `30`    — 运行时/内部错误

## 推荐的工作流程

1. 用户请求安装技能。
2. 确定技能的来源（ClawHub、GitHub、本地文件或 skills.sh 脚本）。
3. 运行相应的 `guardskills` 扫描命令。
4. 查看扫描结果。
5. 如果结果为 `SAFE`，则继续执行 `clawhub install` 或相应的安装操作。
6. 如果结果为 `WARNING`，则告知用户并请求确认。
7. 如果结果为 `UNSAFE`、`CRITICAL` 或 `UNVERIFIABLE`，则阻止安装并说明原因。
8. 严禁跳过扫描步骤。

## 注意事项

- GuardSkills 是额外的安全保障机制，不能替代人工审核。
- 结果为 `SAFE` 表示未检测到已知的高风险代码模式，但并不能完全保证安全。
- 该扫描工具会检测以下风险：凭证泄露、远程代码执行、破坏性文件系统操作、权限提升、混淆后的恶意代码以及可疑的网络活动。