---
name: webuntis
description: 仅限读取 Untis/WebUntis 学生时间表的权限。当您需要从 WebUntis 系统中获取或汇总学生的当前课程安排（今日/本周/指定日期范围）、即将进行的课程、上课教室、授课教师或代课教师信息时，可以使用此权限。
---

# WebUntis（Untis）课程表

使用随附的脚本通过 JSON-RPC 进行登录并获取课程表信息。

## 安全/凭证

- **切勿** 要求用户在聊天中输入密码。
- 如果学校允许，建议使用**专用的只读学生账户**。
- 凭证必须通过环境变量提供（或由操作员安全地注入）。

**单个账户：**
  - `WEBUNTIS_BASE_URL`（例如：`https://xyz.webuntis.com`）
  - `WEBUNTIS_SCHOOL`（学校名称/WebUntis 使用的标识符）
  - `WEBUNTIS_USER`
  - `WEBUNTIS_PASS`
  - 可选：`WEBUNTIS_ELEMENT_TYPE`（默认值为 `5`，表示学生）
  - 可选：`WEBUNTIS_ELEMENT_ID`（在自动检测失败时使用）

**多个账户（并行使用）：**
  - 设置 `WEBUNTIS_PROFILE=<名称>` 或使用 `--profile <名称>` 参数
  - 为每个账户设置相应的环境变量，例如对于名为 `cdg` 的账户：
    - `WEBUNTIS_CDG_BASE_URL`
    - `WEBUNTIS_CDG_SCHOOL`
    - `WEBUNTIS_CDG_USER`
    - `WEBUNTIS_CDG_PASS`
    - 可选：`WEBUNTIS_CDG_ELEMENT_TYPE`、`WEBUNTIS_CDG_ELEMENT_ID`

## 快速命令（执行）

**查看今日课程：**
```bash
cd skills/webuntis/scripts
./webuntis.py today

# or pick a profile
./webuntis.py --profile cdg today
```

**查看指定时间范围内的课程：**
```bash
cd skills/webuntis/scripts
./webuntis.py range 2026-02-10 2026-02-14
```

## 故障排除**

如果出现“无法确定元素 ID”的错误：
1) 执行脚本一次并记录错误信息。
2) 添加 `WEBUNTIS_ELEMENT_ID=<数字>` 参数后重新尝试。

如果认证失败：
- 确认 `WEBUNTIS_BASE_URL` 是否正确对应您的学校。
- 确认 `WEBUNTIS_SCHOOL` 是否与 WebUntis 使用的学校标识符一致。

## 输出结果

脚本会为每节课/活动输出一行信息：
`YYYY-MM-DD HH:MM-HH:MM · <科目> · 教室 <房间> · 教师 <教师姓名>`