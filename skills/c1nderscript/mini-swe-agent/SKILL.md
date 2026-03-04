# mini-swe-agent

使用 `mini-swe-agent` CLI 自动执行复杂的软件工程任务。

## 说明
当用户请求修复漏洞、实现新功能或解决需要全面探索和编辑代码库的 GitHub 问题时，可以使用此技能。该工具充当“分包商”，负责处理这些复杂任务。

## 使用方法
当收到需要完成复杂编码任务的请求时，先编写一个简洁明了的问题描述，然后使用 bash 工具运行 `mini` CLI。

```bash
mini --yolo "Fix the authentication logic in /src/auth.py to ensure tokens expire after 3600 seconds"
Rules
Autonomy: Always use the --yolo flag so the agent runs autonomously without waiting for user input.

Formatting: Escape double quotes inside the problem statement if necessary.

Verification: Monitor the output. Once mini finishes, verify the changes if requested by the user.

Scope Limitation: Do NOT use this for simple one-line text replacements or minor typo fixes. Use standard file editing tools for those to save time and compute.


---

### 2. How to Build/Install It

Instead of creating it manually, you can run this single command in your terminal. It will create the necessary OpenClaw skills directory (if it doesn't already exist) and write the `SKILL.md` file directly into it.

```bash
mkdir -p ~/.openclaw/skills/mini-swe-agent && cat << 'EOF' > ~/.openclaw/skills/mini-swe-agent/SKILL.md
# mini-swe-agent

使用 `mini-swe-agent` CLI 自动执行复杂的软件工程任务。

## 说明
当用户请求修复漏洞、实现新功能或解决需要全面探索和编辑代码库的 GitHub 问题时，可以使用此技能。该工具充当“分包商”，负责处理这些复杂任务。

## 使用方法
当收到需要完成复杂编码任务的请求时，先编写一个简洁明了的问题描述，然后使用 bash 工具运行 `mini` CLI。

` ` `bash
mini --yolo "修复 `/src/auth.py` 中的认证逻辑，确保令牌在 3600 秒后过期"
` ` `

## 规则
* **自动执行：** 必须始终使用 `--yolo` 标志，以便代理能够自动运行而无需等待用户输入。
* **格式要求：** 如有必要，请对问题描述中的双引号进行转义处理。
* **验证结果：** 监控 `mini` 的执行结果。任务完成后，根据用户要求验证所做的更改。
* **使用范围限制：** 请勿将此工具用于简单的单行文本替换或轻微的拼写错误修复。这些任务应使用标准的文件编辑工具来完成，以节省时间和计算资源。
EOF