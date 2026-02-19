---
name: visla
description: 使用 Visla 从文本脚本、URL 或 PPT/PDF 文档生成 AI 生成的视频。适用于以下场景：用户请求生成视频、将网页转换为视频、将 PPT/PDF 文件转换为视频，或用户需要查询 Visla 账户的信用额度/余额。
argument-hint: <script|url|doc|account> [script|URL|file]
metadata:
  clawdbot:
    emoji: ""
    requires:
      env: ["VISLA_API_KEY", "VISLA_API_SECRET"]
    primaryEnv: "VISLA_API_KEY"
    files: ["scripts/*"]
---
# Visla 视频生成

**版本：260218-1410**

使用 Visla 的 OpenAPI，可以从文本脚本、网页 URL 或文档（PPT/PDF）生成 AI 生成的视频。

## 开始使用前

**凭据**（切勿在响应中输出 API 密钥/秘密）：

**重要提示**：仅在没有用户明确同意的情况下，才读取本地的凭据文件。

1. 在读取 `~/.config/visla/.credentials` 之前，请先获得用户的许可。
2. 如果获得许可且文件存在且凭据有效，请使用 `--credentials-file ~/.config/visla/.credentials` 与 **Python** CLI 进行操作。**Bash** CLI 不支持 `--credentials-file` 选项，因此请使用环境变量。
3. 如果用户拒绝提供凭据、文件缺失或凭据无效，请再次请求用户提供凭据。

仅处理用户明确提供的本地文件（脚本/文档），并提醒用户不要上传敏感数据。
- 告知用户：这仅是一次性设置（配置完成后，无需再次操作）。
- 告知用户：请从 https://www.visla.us/visla-api 获取 API 密钥和秘密。
- 明确请求用户的 API 密钥/秘密（或要求用户更新文件并确认）。不要在响应中重复显示这些信息。

**凭据有效性检查**：
- 如果凭据存在，但运行 `account` 时出现 `VISLA_CLI_ERROR_CODE=missing_credentials` 或 `VISLACLI_ERROR_CODE=auth_failed` 的错误，请认为凭据无效，并要求用户提供有效的凭据。

**文件格式（Bash/Zsh）**：
```bash
export VISLA_API_KEY="your_key"
export VISLA_API_SECRET="your_secret"
```

**PowerShell（临时会话）**：
```powershell
$env:VISLA_API_KEY = "your_key"
$env:VISLA_API_SECRET = "your_secret"
```

**脚本**：`scripts/visla_cli.py`（Python），`scripts/visla_cli.sh`（Bash）

## 平台执行方式**

**默认策略**：
- 在 macOS 上，如果依赖项可用，优先使用 **Bash**（因为 Bash CLI 可以避免某些 macOS 环境中的 Python SSL 问题）。
- 如果您已经配置好了 Python，或者缺少 Bash 依赖项，优先使用 **Python**。

**Bash（推荐在 macOS 上使用；也适用于类 Linux 环境）**：
```bash
# With user consent, you may source ~/.config/visla/.credentials
export VISLA_API_KEY="your_key"
export VISLA_API_SECRET="your_secret"
./scripts/visla_cli.sh <command>
```

**Python（跨平台）**：
```bash
python3 scripts/visla_cli.py --key "your_key" --secret "your_secret" <command>
# Or, with user consent:
python3 scripts/visla_cli.py --credentials-file ~/.config/visla/.credentials <command>
```

**Windows 原生环境（PowerShell/CMD，不支持 Bash；使用 Python）**：
```powershell
# PowerShell
$env:VISLA_API_KEY = "your_key"
$env:VISLA_API_SECRET = "your_secret"
python scripts/visla_cli.py <command>
```

**Windows 注意事项**：
- 除非确认有可用的 Bash 环境（如 WSL/Git Bash），否则建议在 Windows 上使用 **Python CLI**。
- 对于简单的脚本，可以直接运行：`python scripts/visla_cli.py script "Scene 1: ..."`
- 对于多行或复杂的脚本，建议使用 `-` 选项通过 stdin 运行（不生成临时文件）：
  ```powershell
  @"
  Scene 1: ...
  Scene 2: ...
  "@ | python scripts/visla_cli.py script -
  ```
- 如果安装了 Python 启动器，`py -3 scripts/visla_cli.py <command>` 可能比 `python` 更适用。
- 凭据：
  - Python CLI 仅在提供了 `--credentials-file` 选项时才会读取凭据文件。
  - 在 Windows 上，默认路径通常是：`%USERPROFILE%\\.config\\visla\\.credentials`。

**注意**：不要打印凭据信息。建议使用环境变量或 `--credentials-file`，并在用户明确同意的情况下进行操作。

## 命令**

| 命令 | 描述 |
|---------|-------------|
| `/visla script <脚本或文件>` | 从脚本（文本或本地文件）生成视频 |
| `/visla url <URL>` | 从网页 URL 生成视频 |
| `/visla doc <文件>` | 从文档（PPT/PDF）生成视频 |
| `/visla account` | 显示账户信息和余额 |

有关 CLI 的完整用法，请运行 `scripts/visla_cli.sh --help` 或 `python3 scripts/visla_cli.py --help`。

## 脚本格式**

```
**Scene 1** (0-10 sec):
**Visual:** A futuristic calendar flipping to 2025 with digital patterns.
**Narrator:** "AI is evolving rapidly! Here are 3 game-changing AI trends."

**Scene 2** (10-25 sec):
**Visual:** Text: "Trend #1: Generative AI Everywhere." Show tools like ChatGPT.
**Narrator:** "Generative AI is dominating industries—creating content and images."
```

## 工作流程**

`script`、`url` 和 `doc` 命令会自动执行整个流程：
1. 创建项目
2. 监控生成进度（可能需要几分钟时间）
3. 自动导出视频并返回下载链接

**执行说明**：
- 告知用户视频生成需要一些时间
- 在执行过程中定期报告进度

### 超时处理

- 该流程通常需要 **3-10 分钟**，但在最坏的情况下可能需要长达 **30 分钟**。请将任务/命令的 `timeout` 设置为 **>= 30 分钟**（Windows 的默认超时时间通常为 10 分钟，需要延长）。如果无法更改超时时间，请提前告知用户，并在超时时询问用户是否继续执行或切换到逐步执行模式。
- 如果超时发生，CLI 会在输出中返回 `project_uuid`。告知用户他们可以手动查看项目状态，并稍后通过 Visla 的 Web 界面或 API 继续操作。

## 示例**

```
/visla script @myscript.txt
/visla script "Scene 1: ..."
/visla url https://blog.example.com/article
/visla doc presentation.pptx
/visla account
```

## 支持的文档格式**

- **PowerPoint**：`.pptx`、`.ppt`
- **PDF**：`.pdf`

## 输出格式**

- **开始**：在技能开始时显示 “Visla Skill v260218-1410”
- **结束**：在技能完成后显示 “Visla Skill v260218-1410 完成”