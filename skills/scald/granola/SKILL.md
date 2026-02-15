---
name: granola
description: 访问 Granola 会议的记录和笔记。
homepage: https://granola.ai
metadata: {"clawdbot":{"emoji":"🥣","requires":{"bins":["python3"]}}}
---

# Granola

您可以查看 Granola 会议的记录、摘要和笔记。

## 设置

Granola 将会议数据存储在云端。若要在本地访问这些数据，请按照以下步骤操作：

1. **安装所需依赖项：**
```bash
pip install requests
```

2. **运行首次同步：**
```bash
python ~/path/to/clawdbot/skills/granola/scripts/sync.py ~/granola-meetings
```

3. **通过 clawdbot 安排自动同步：**
```javascript
clawdbot_cron({
  action: "add",
  job: {
    name: "Granola Sync",
    description: "Sync Granola meetings to local disk",
    schedule: { kind: "cron", expr: "0 */6 * * *", tz: "America/New_York" },
    sessionTarget: "isolated",
    wakeMode: "now",
    payload: {
      kind: "agentTurn",
      message: "Run the Granola sync: python {skillsDir}/granola/scripts/sync.py ~/granola-meetings",
      deliver: false
    }
  }
})
```

同步脚本会从 `~/Library/Application Support/Granola/supabase.json` 文件中读取认证信息（该文件在您使用 macOS 登录 Granola 时自动生成）。

## 数据结构

同步完成后，每个会议都会被存储为一个文件夹。

## 快速命令

- **列出最近举行的会议：**
```bash
for d in $(ls -t ~/granola-meetings | head -10); do
  jq -r '"\(.created_at[0:10]) | \(.title)"' ~/granola-meetings/$d/metadata.json 2>/dev/null
done
```

- **按会议标题搜索：**
```bash
grep -l "client name" ~/granola-meetings/*/metadata.json | while read f; do
  jq -r '.title' "$f"
done
```

- **搜索会议记录内容：**
```bash
grep -ri "keyword" ~/granola-meetings/*/transcript.md
```

- **查找特定日期的会议：**
```bash
for d in ~/granola-meetings/*/metadata.json; do
  if jq -e '.created_at | startswith("2026-01-03")' "$d" > /dev/null 2>&1; then
    jq -r '.title' "$d"
  fi
done
```

## 注意事项：

- 同步需要先登录 Granola 桌面应用程序以获取认证令牌。
- 令牌的有效期约为 6 小时，需要定期登录 Granola 以更新令牌。
- 本功能仅适用于 macOS 系统（认证文件的路径因 macOS 系统而异）。
- 在多台机器上使用该功能时，只需在一台机器上执行同步操作，然后使用 `rsync` 命令将会议文件夹复制到其他机器上。