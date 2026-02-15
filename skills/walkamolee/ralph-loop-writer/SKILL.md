---

# Ralph 命令生成器

该工具用于生成用于自动化 Claude Code、Gemini CLI 或 Grok CLI 的循环命令。它会根据用户的需求提问，并输出可在 PowerShell、Windows CMD 或 Bash/Linux 上运行的命令。

## 允许使用的工具：
- AskUserQuestion
- Write
- Read

---

## Ralph 命令生成器的工作流程：

1. **选择 AI 工具**：
   - 使用 `AskUserQuestion` 提问用户想要使用哪种 AI CLI 工具：
     - 选项：
       - "Claude Code"（推荐）
       - "Gemini CLI"
       - "Grok CLI"

2. **选择模型**：
   - 根据用户选择的 AI 工具，再次使用 `AskUserQuestion` 提问用户想要使用哪个模型：
     - 对于 Claude Code：
       - 选项：
         - "Default"（推荐） - 使用默认模型（当前为 Sonnet 4.5）
         - "Haiku" - 最快且成本最低
         - "Sonnet" - 性能与成本平衡
         - "Opus" - 功能最强大，但成本较高
     - 对于 Gemini CLI：
       - 选项：
         - "Default"（推荐） - 使用默认模型
         - "gemini-3-flash" - 最新的 Gemini 3，速度最快且成本最低
         - "gemini-3-pro" - 最新的 Gemini 3，适合复杂任务
         - "gemini-2.5-flash" - 稳定的生产模型，速度较快
         - "gemini-2.5-pro" - 稳定的生产模型，功能更强大
     - 对于 Grok CLI：
       - 选项：
         - "Default"（推荐） - 使用 grok-code-fast-1，专为快速代码生成和自动化循环设计
         - "grok-4-latest" - 最新的 Grok 4，适合复杂推理
         - "grok-beta" - 即将推出的功能预览版

3. **选择操作系统**：
   - 使用 `AskUserQuestion` 提问用户使用哪种 shell 环境：
     - 选项：
       - "PowerShell"（推荐）
       - "Windows CMD"
       - "Bash/Linux"

4. **选择复杂度级别**：
   - 使用 `AskUserQuestion` 提问用户需要多高的控制程度：
     - 选项：
       - "Simple"（推荐） - 基本循环，选项最少
       - "Intermediate" - 结合两种控制机制
       - "Advanced" - 全面控制，具有多种保护机制

5. **选择循环类型（根据复杂度级别）**：
   - **如果选择 Simple**：
     - 使用 `AskUserQuestion` 提问用户需要哪种类型的循环：
       - 选项：
         - "Fixed count"（推荐） - 精确运行 N 次
         - "Infinite with delay" - 永远运行并带有暂停
         - "Stop file trigger" - 运行直到 STOP.txt 文件出现

   - **如果选择 Intermediate**：
     - 使用 `AskUserQuestion` 提问用户需要哪些组合功能：
       - 多选选项：
         - "Fixed iterations" - 运行最多 N 次
         - "Time limit" - 运行最多 X 分钟
         - "Stop file" - 当 STOP.txt 文件出现时停止
         - "Delay between runs" - 每次运行之间暂停 X 秒
         - "Show counter" - 显示运行次数
         - "File monitoring" - 根据文件大小/行数停止

   - **如果选择 Advanced**：
     - 使用 `AskUserQuestion` 提问用户需要哪些功能：
       - 多选选项：
         - "Max iterations" - 限制运行次数
         - "Time limit" - 最大运行时间
         - "Stop file" - 手动停止
         - "Delay between runs" - 每次运行之间暂停 X 秒
         - "Timestamp logging" - 显示每次运行的时间
         - "Counter display" - 显示运行次数

6. **收集参数**：
   - 根据用户选择的选项，收集所需的参数值：

7. **生成命令**：
   - 根据以下信息构建相应的命令：
     - AI 工具（Claude 或 Gemini）
     - 模型
     - Shell 环境（PowerShell、CMD、Bash）
     - 复杂度级别
     - 选定的功能
     - 参数值

****重要提示 - 命令语法：**
   - **对于 Claude Code（PowerShell/Bash）**：
     使用 `claude-code`（而不是 `claude -p`），因为 `-p` 标志需要参数，不能通过管道传递。
     - 默认命令：
       - `Get-Content PROMPT.md -Raw | claude-code --dangerously-skip-permissions`
     - 使用 haiku 模型时：`Get-Content PROMPT.md -Raw | claude-code --model haiku --dangerously-skip-permissions`
     - 使用 sonnet 模型时：`Get-Content PROMPT.md -Raw | claude-code --model sonnet --dangerously-skip-permissions`
     - 使用 opus 模型时：`Get-Content PROMPT.md -Raw | claude-code --model opus --dangerously-skip-permissions`

   - **对于 Gemini CLI（PowerShell）**：
     Gemini CLI 支持标准输入（stdin）管道。
     - 默认命令：
       - `Get-Content PROMPT.md -Raw | gemini --yolo`
     - 使用 gemini-3-flash 模型时：`Get-Content PROMPT.md -Raw | gemini --model gemini-3-flash --yolo`
     - 使用 gemini-3-pro 模型时：`Get-Content PROMPT.md -Raw | gemini --model gemini-3-pro --yolo`
     - 使用 gemini-2.5-flash 模型时：`Get-Content PROMPT.md -Raw | gemini --model gemini-2.5-flash --yolo`
     - 使用 gemini-2.5-pro 模型时：`Get-Content PROMPT.md -Raw | gemini --model gemini-2.5-pro --yolo`

   - **对于 Grok CLI（PowerShell）**：
     默认命令：`Get-Content PROMPT.md -Raw | grok-auto`（使用 GROK_MODEL 环境变量中的默认模型）
     - 使用 grok-code-fast-1 模型时：`Get-Content PROMPT.md -Raw | grok-auto -m grok-code-fast-1`
     - 使用 grok-4-latest 模型时：`Get-Content PROMPT.md -Raw | grok-auto -m grok-4-latest`
     - 使用 grok-beta 模型时：`Get-Content PROMPT.md -Raw | grok-auto -m grok-beta`

****命令模板中的占位符替换规则：**
   - 对于 **Claude Code**：将 `[AI_COMMAND_WITH_PROMPT]` 替换为包含提示参数的完整命令：
     - 默认命令：`claude -p (Get-Content PROMPT.md -Raw) --dangerously-skip-permissions`
     - 使用模型时：`claude -p (Get-Content PROMPT.md -Raw) --model haiku --dangerously-skip-permissions`

   - 对于 **Gemini CLI**：将 `[AI_COMMAND_WITH_PROMPT]` 替换为通过管道传递的命令：
     - 默认命令：`Get-Content PROMPT.md -Raw | gemini --yolo`
     - 使用模型时：`Get-Content PROMPT.md -Raw | gemini --model gemini-3-flash --yolo`

   - 对于 **Grok CLI**：将 `[AI_COMMAND_WITH_PROMPT]` 替换为通过管道传递的命令：
     - 默认命令：`Get-Content PROMPT.md -Raw | grok-auto`
     - 使用模型时：`Get-Content PROMPT.md -Raw | grok-auto -m grok-4-latest`

****重要提示：**
   - **Claude Code** 需要将提示作为命令行参数传递，不能通过管道传递。请使用 `claude -p (Get-Content PROMPT.md -Raw) --dangerously-skip-permissions`。
   - **对于 Gemini 和 Grok CLI**，可以使用标准输入（stdin）管道。
   - **模型选择是可选的**：始终询问用户想要使用哪个模型，但选择“Default”选项时会省略 `--model` 标志。
   - **对于 Claude Code（PowerShell）**：
     - 默认格式：`claude -p (Get-Content PROMPT.md -Raw) --dangerously-skip-permissions`
     - 使用模型时：`claude -p (Get-Content PROMPT.md -Raw) --model <model> --dangerously-skip-permissions`
     - 可用的模型：`haiku`、`sonnet`、`opus`
   - **对于 Gemini CLI**：
     - 默认格式：`Get-Content PROMPT.md -Raw | gemini --yolo`
     - 使用模型时：`Get-Content PROMPT.md -Raw | gemini --model <model> --yolo`
     - 可用的模型：`gemini-3-flash`、`gemini-3-pro`、`gemini-2.5-flash`、`gemini-2.5-pro`
     - 注意：`-p` 标志在 Gemini 中已被弃用。
   - **对于 Grok CLI**：
     - 使用 `grok-auto` PowerShell 函数可以直接调用 xAI API（非常适合自动化）。
     - 默认格式：`Get-Content PROMPT.md -Raw | grok-auto`（不使用 `-m` 标志，会使用 GROK_MODEL 环境变量）
     - 使用模型时：`Get-Content PROMPT.md -Raw | grok-auto -m <model>`
     - 可用的模型：`grok-code-fast-1`、`grok-4-latest`、`grok-beta`、`grok-4`
     - 注意：`grok-auto` 是一个 PowerShell 函数，可以直接调用 xAI API（不需要 CLI）。
     - 建议使用默认的 `grok-code-fast-1` 模型进行自动化循环（响应最快）。
   - 当用户不确定时，建议选择“Recommended”选项。
   - 尽量将命令放在一行上，以便于复制和粘贴。
   - **始终包含时间跟踪**：使用 `Get-Date`（PowerShell）或 `date +%s`（Bash）显示每次运行的时间。
   - **始终创建带时间戳的文件**：文件格式为 `ralphcommand-YYYY-MM-DD-HHMMSS.md`。
   - **不要包含成本跟踪**：没有 `Get-LastCallCost` 函数，不进行成本计算，仅进行时间跟踪。
   - 如果需要使用 Claude 的成本跟踪，请让用户查看 [https://console.anthropic.com](https://console.anthropic.com) 以获取实际 API 使用情况。
   - 在为 PowerShell 生成最终命令时：
     - 对于 Claude：将 `[AI_COMMAND_WITH_PROMPT]` 替换为包含提示参数的完整 Claude 命令。
     - 对于 Gemini/Grok：模板中已经包含了管道操作，只需将 `[AI_COMMAND]` 替换为命令即可。

---

### 示例命令（部分）：
- **PowerShell - 简单循环（无延迟）**：
  ```powershell
  ralphcommand-2026-01-14-233045.md
  cat PROMPT.md | claude-code --dangerously-skip-permissions
  ```

- **PowerShell - 简单循环（带延迟）**：
  ```powershell
  ralphcommand-2026-01-14-233045.md
  cat PROMPT.md | claude-code --dangerously-skip-permissions -delay 5 seconds
  ```

- **PowerShell - 无限循环（带延迟）**：
  ```powershell
  ralphcommand-2026-01-14-233045.md
  cat PROMPT.md | claude-code --dangerously-skip-permissions -delay 5 seconds
  ```

- **PowerShell - 高级循环（全控制）**：
  ```powershell
  ralphcommand-2026-01-14-233045.md
  cat PROMPT.md | claude-code --dangerously-skip-permissions -max iterations 10 -timeout 30 minutes
  ```

- **CMD - 简单循环（无延迟）**：
  ```cmd
  ralphcommand-2026-01-14-233045.md
  cat PROMPT.md | claude-code --dangerously-skip-permissions
  ```

- **CMD - 简单循环（带延迟）**：
  ```cmd
  ralphcommand-2026-01-14-233045.md
  cat PROMPT.md | claude-code --dangerously-skip-permissions -delay 5 seconds
  ```

- **CMD - 无限循环（带延迟）**：
  ```cmd
  ralphcommand-2026-01-14-233045.md
  cat PROMPT.md | claude-code --dangerously-skip-permissions -delay 5 seconds
  ```

请注意：CMD 的功能有限。建议使用 PowerShell 进行时间跟踪。

---

## 其他注意事项：
- **对于 Claude Code**：提示必须作为命令行参数传递，不能通过 stdin 管道传递。请使用 `claude -p (Get-Content PROMPT.md -Raw) --dangerously-skip-permissions`。
- **对于 Gemini 和 Grok CLI**，可以使用标准输入（stdin）管道。
- **模型选择是可选的**：始终询问用户想要使用哪个模型，但选择“Default”选项时会省略 `--model` 标志。
- **对于 Claude Code（PowerShell）**：
  - 默认格式：`claude -p (Get-Content PROMPT.md -Raw) --dangerously-skip-permissions`
  - 使用模型时：`claude -p (Get-Content PROMPT.md -Raw) --model <model> --dangerously-skip-permissions`
  - 可用的模型：`haiku`、`sonnet`、`opus`
- **对于 Gemini CLI**：
  - 默认格式：`Get-Content PROMPT.md -Raw | gemini --yolo`
  - 使用模型时：`Get-Content PROMPT.md -Raw | gemini --model <model> --yolo`
  - 可用的模型：`gemini-3-flash`、`gemini-3-pro`、`gemini-2.5-flash`、`gemini-2.5-pro`
  - 注意：`-p` 标志在 Gemini 中已被弃用。
- **对于 Grok CLI**：
  - 使用 `grok-auto` PowerShell 函数可以直接调用 xAI API（非常适合自动化）。
  - 默认格式：`Get-Content PROMPT.md -Raw | grok-auto`（不使用 `-m` 标志，会使用 GROK_MODEL 环境变量）
  - 使用模型时：`Get-Content PROMPT.md -Raw | grok-auto -m <model>`
  - 可用的模型：`grok-code-fast-1`、`grok-4-latest`、`grok-beta`、`grok-4`
  - 注意：`grok-auto` 是一个 PowerShell 函数，可以直接调用 xAI API（不需要 CLI）。
- **建议使用默认的 `grok-code-fast-1` 模型进行自动化循环（响应最快）。
- 尽量将命令放在一行上，以便于复制和粘贴。
- **始终包含时间跟踪**：使用 `Get-Date`（PowerShell）或 `date +%s`（Bash）显示每次运行的时间。
- **始终创建带时间戳的文件**：文件格式为 `ralphcommand-YYYY-MM-DD-HHMMSS.md`。
- **不要包含成本跟踪**：没有 `Get-LastCallCost` 函数，不进行成本计算，仅进行时间跟踪。
- 如果需要使用 Claude 的成本跟踪，请让用户查看 [https://console.anthropic.com](https://console.anthropic.com) 以获取实际 API 使用情况。
- 在为 PowerShell 生成最终命令时：
  - 对于 Claude：将 `[AI_COMMAND_WITH_PROMPT]` 替换为包含提示参数的完整 Claude 命令。
- 对于 Gemini/Grok：模板中已经包含了管道操作，只需将 `[AI_COMMAND]` 替换为命令即可。