---
name: wpstime-punchclock
description: **自动化在 WPS Time/NetTime (wpstime.com) 上记录考勤时间的功能**  
该功能可用于执行以下操作：  
- 设置考勤系统（setup punchclock/configure punchclock）  
- 记录上班/下班时间（clock in/clock out）  
- 开始/结束休息时间（start break/end break）  
- 开始/结束午餐时间（start lunch/end lunch）  
- 查看考勤状态（check status）  

系统会运行一个 Playwright 脚本，自动捕获屏幕截图，并发送简短的确认信息作为回复。
---

# WPS Time / NetTime 出勤打卡系统

运行随附的 Playwright 脚本，使用 macOS Keychain 的凭证登录 WPS Time NetTime 系统，执行所需的打卡操作（或状态检查），截取屏幕截图，并报告结果。

## 输入 → 操作
将用户意图映射到脚本的 `--action` 参数：

### 设置 / 凭证
- 设置打卡系统 / 配置打卡流程 → 运行设置流程

### 打卡操作
- 登录 → `clock-in`
- 下班 → `clock-out`
- 开始休息 → `start-break`
- 结束休息 → `end-break`（在脚本中实现为 `Clock In (end-break)`
- 开始午餐 → `start-lunch`
- 结束午餐 → `end-lunch`（在脚本中实现为 `Clock In (end-lunch)`
- 查看状态 → `status`

## 首次设置（每台机器 / 每个用户）

### 选项 A（推荐）：本地终端设置（密码不会记录在聊天日志中）
运行交互式设置脚本，将凭证存储在 **macOS Keychain** 中：

```bash
cd {baseDir}/scripts
node ./setup.mjs
```

这些凭证将存储在 Keychain 服务中：
- `wpstime-punchclock.company`（secret = 公司/通用 ID）
- `wpstime-punchclock`（account = 用户名, secret = 密码）

### 选项 B：聊天助手设置（包含密码；风险较高）
仅在用户明确请求通过聊天进行设置，并且同意密码会显示在聊天记录/日志中时使用。

**操作流程：**
1) 明确警告：
   - 密码将通过聊天发送，可能会被聊天平台和网关日志记录。
   - 建议选择选项 A。
2) 如果用户仍确认使用此方式，分三次收集以下信息：
   - companyId
   - 用户名
   - 密码
3) 使用 `security add-generic-password -U` 命令将凭证存储在运行网关的同一台机器上的 Keychain 中：

```bash
security add-generic-password -U -s "wpstime-punchclock.company" -a "company" -w "<companyId>"
security add-generic-password -U -s "wpstime-punchclock" -a "<username>" -w "<password>"
```

4) 严禁将密码显示给用户。存储凭证后，运行 `status` 命令验证登录是否成功。

## 工作流程
1) 运行打卡脚本（默认为无界面模式）：

```bash
node {baseDir}/scripts/punchclock.mjs --action <action>
```

**可选参数：**
- `--headless 0` 用于调试
- `--outDir <路径>` 用于指定截图输出路径

2) 解析脚本的输出 JSON 数据：
- 成功时：读取 `performed`、`screenshotPath` 以及（可选的）`snippet` 中的关键信息。
- 失败时：报告错误，并不视为打卡成功。

3) 向请求通道回复：
- 一条确认消息（说明执行的操作）
- 如果有有效状态/时间信息，则一并提供
- 附加截图文件（路径为 `screenshotPath`）

4) 如果用户请求打卡，但系统可能已经处于相应的状态，建议先运行 `status` 命令进行确认，以避免重复打卡的错误。

## 凭证（macOS Keychain）
不要将凭证存储在文件或提示框中，应使用 Keychain 进行管理。

**推荐使用的 Keychain 服务：**
- 服务 `wpstime-punchclock.company` → secret = 公司/通用 ID
- 服务 `wpstime-punchclock` → account = 用户名, secret = 密码

**向后兼容（旧版 OpenClaw 设置）：**
- `openclaw.wpstime.company`
- `openclaw.wpstime`

如果这些服务不存在，打卡脚本会抛出错误。此时，引导用户重新运行脚本：

```bash
cd {baseDir}/scripts
node ./setup.mjs
```

然后重新尝试所需的操作。

## 参考资料
如需查看更详细的操作手册，请参阅：
- `references/PUNCHCLOCK_RUNBOOK.md`