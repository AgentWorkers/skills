---
name: visla
description: 使用 Visla 从文本脚本、URL 或 PPT/PDF 文档生成 AI 生成的视频。适用于以下场景：用户请求生成视频、将网页转换为视频、将 PPT/PDF 转换为视频，或用户需要查询 Visla 账户的信用额度/余额。
argument-hint: <script|url|doc|account> [script|URL|file]
---

# Visla 视频生成

**版本：260211-1520**

使用 Visla 的 OpenAPI 从文本脚本、网页 URL 或文档（PPT/PDF）生成 AI 生成的视频。

## 开始之前

**凭据**（切勿在响应中输出 API 密钥/秘密）：

**重要提示**：在请求用户提供凭据之前，务必先尝试读取凭据文件。

1. 尝试读取 `~/.config/visla/.credentials` 文件。
2. 如果文件存在且包含有效的凭据，请直接使用这些凭据（无需询问用户）。
3. 仅当文件缺失或无效时，才请求用户提供凭据：
   - 告诉用户：这仅是一次性设置（配置完成后，他们无需再次操作）。
   - 告诉用户：从 https://www.visla.us/visla-api 获取 API 密钥和秘密。
   - 明确请求 API 密钥/秘密（或要求用户更新文件并确认）。切勿在响应中重复显示这些秘密。

**凭据有效性检查**（实际操作）：
- 如果凭据存在，但运行 `account` 命令时出现 `VISLA_CLI_ERROR_CODE=missing_credentials` 或 `VISLA_CLI_ERROR_CODE=auth_failed` 错误，请认为凭据无效，并要求用户提供有效的凭据。

**文件格式（适用于 Bash/Zsh）**：
```bash
export VISLA_API_KEY="your_key"
export VISLA_API_SECRET="your_secret"
```

**适用于 PowerShell（临时会话）**：
```powershell
$env:VISLA_API_KEY = "your_key"
$env:VISLA_API_SECRET = "your_secret"
```

**脚本**：`scripts/visla_cli.py`（Python），`scripts/visla_cli.sh`（Bash）

## 平台执行策略**

**默认策略**：
- 在 macOS 上，如果依赖项可用，优先使用 **Bash**（因为 Bash CLI 可避免某些 macOS 环境中的 Python SSL 问题）。
- 如果您已经使用了配置良好的 Python，或者缺少 Bash 依赖项，则优先使用 **Python**。

**Bash（推荐在 macOS 上使用；也适用于类 Linux 环境）**：
```bash
source ~/.config/visla/.credentials
./scripts/visla_cli.sh <command>
```

**Python（跨平台）**：
```bash
python3 scripts/visla_cli.py <command>
```

**Windows 本地环境（使用 PowerShell/CMD，不依赖 Bash；也可使用 Python）**：
```powershell
# PowerShell
$env:VISLA_API_KEY = "your_key"
$env:VISLA_API_SECRET = "your_secret"
python scripts/visla_cli.py <command>
```

**Windows 注意事项**：
- 除非确认有可用的 Bash 环境（如 WSL/Git Bash），否则建议在 Windows 上使用 **Python CLI**。
- 对于简单的脚本，可以直接运行：`python scripts/visla_cli.py script "Scene 1: ..."`。
- 对于多行或复杂的脚本，建议使用 `-` 参数通过标准输入（stdin）进行执行（这样不会生成临时文件）：
  ```powershell
  @"
  Scene 1: ...
  Scene 2: ...
  "@ | python scripts/visla_cli.py script -
  ```
- 如果安装了 Python 启动器，`py -3 scripts/visla_cli.py <command>` 可能比 `python` 更适用。
- 凭据：如果环境变量未设置，Python CLI 也会尝试自动读取 `~/.config/visla/.credentials` 文件。
- 在 Windows 上，该文件通常位于 `%USERPROFILE%\\.config\\visla\\.credentials`。

**注意**：不要直接打印凭据。建议从 `~/.config/visla/.credentials` 文件或环境变量中读取凭据。

## 命令说明**

| 命令 | 描述 |
|---------|-------------|
| `/visla script <脚本或文件>` | 从脚本（文本文件或本地文件）生成视频 |
| `/visla url <URL>` | 从网页 URL 生成视频 |
| `/visla doc <文件>` | 从文档（PPT/PDF）生成视频 |
| `/visla account` | 显示账户信息和余额 |

**查看完整 CLI 命令列表的方法**：运行 `scripts/visla_cli.sh --help` 或 `python3 scripts/visla_cli.py --help`。

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

`script`、`url` 和 `doc` 命令会自动执行以下流程：
1. 创建项目。
2. 监控生成进度（可能需要几分钟时间）。
3. 自动导出视频并返回下载链接。

**执行说明**：
- 告知用户视频生成需要一些时间。
- 在执行过程中定期报告进度。

### 超时处理建议**

- 该流程通常需要 **3-10 分钟**，但在最坏的情况下可能需要长达 **30 分钟**。请将任务/命令的 `timeout` 设置为 **大于或等于 30 分钟**（Windows 的默认超时时间通常为 10 分钟，需要延长）。如果无法更改超时设置，请提前告知用户，并在超时时询问用户是否继续执行或切换到逐步执行模式。
- 如果超时发生，CLI 会在输出中返回 `project_uuid`。告知用户他们可以手动查看项目状态，并通过 Visla 的 Web 界面或 API 继续操作。

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

- 视频开始时显示：“Visla Skill v260211-1520”。
- 视频生成完成后显示：“Visla Skill v260211-1520 完成”。