---
name: google-keep
description: 通过命令行界面（CLI）读取、创建、编辑、搜索以及管理 Google Keep 中的笔记和列表。
metadata:
  openclaw:
    requires:
      bins: ["python3", "uv"]
    install:
      - id: venv
        kind: shell
        command: "cd \"$SKILL_DIR\" && uv venv .venv && .venv/bin/pip install gkeepapi gpsoauth"
        label: "Create venv and install gkeepapi + gpsoauth"
---
# Google Keep CLI 技能

使用非官方的 gkeepapi 从命令行管理 Google Keep 的笔记和列表。

## 设置

安装完成后，该 CLI 会位于 `skill` 目录中。您可以设置一个便捷的别名或封装脚本来使用它：

```bash
SKILL_DIR="<path-to-this-skill>"  # e.g. skills/google-keep
alias gkeep="$SKILL_DIR/.venv/bin/python3 $SKILL_DIR/gkeep.py"
```

或者创建一个全局封装脚本：

```bash
cat > ~/.local/bin/gkeep << 'EOF'
#!/bin/bash
SKILL_DIR="$(dirname "$(readlink -f "$0")")/../.openclaw/workspace/skills/google-keep"
exec "$SKILL_DIR/.venv/bin/python3" "$SKILL_DIR/gkeep.py" "$@"
EOF
chmod +x ~/.local/bin/gkeep
```

## 认证

### 首次设置（OAuth 令牌交换）：

1. 在浏览器中访问 https://accounts.google.com/EmbeddedSetup
2. 用您的 Google 账户登录
3. 在同意页面上点击“我同意”（页面可能会长时间加载——请忽略）
4. 打开开发者工具（F12）→ “应用程序”选项卡→ “Cookies”→ “accounts.google.com”
5. 复制 `oauth_token` cookie 的值
6. 运行以下命令：

```bash
gkeep auth <email> <oauth_token>
```

### 如果已经获得了 master 令牌：

```bash
gkeep auth-master <email> <master_token>
```

凭据存储在 `<skill-dir>/.config/` 文件中（权限设置为 600）。Master 令牌具有完整的账户访问权限——请将其视为密码。该令牌**不会过期**（与标准的 OAuth 刷新令牌不同）。

## 命令

### 列出笔记

```bash
gkeep list                    # Active notes
gkeep list --archived         # Include archived
gkeep list --pinned           # Pinned only
gkeep list --label "Shopping" # Filter by label
gkeep list --json             # JSON output
gkeep list -v                 # Show IDs
```

### 搜索

```bash
gkeep search "grocery"
gkeep search "todo" --json
```

### 获取特定笔记

```bash
gkeep get <note-id>
gkeep get "Shopping List"     # By title (case-insensitive)
gkeep get <id> --json
```

### 创建笔记

```bash
gkeep create --title "Ideas" --text "Some thoughts"
gkeep create --title "Groceries" --list --items "Milk" "Eggs" "Bread"
gkeep create --title "Important" --pin --color Red --label "Work"
```

### 编辑笔记

```bash
gkeep edit <id-or-title> --title "New Title"
gkeep edit <id-or-title> --text "Updated text"
gkeep edit <id-or-title> --pin true
gkeep edit <id-or-title> --archive true
gkeep edit <id-or-title> --color Blue
```

### 列出操作记录

```bash
gkeep check "Groceries" "milk"           # Check off an item
gkeep check "Groceries" "milk" --uncheck # Uncheck
gkeep check "Groceries" "m" --all        # Check all matching
gkeep add-item "Groceries" "Butter" "Cheese"  # Add items
```

### 删除（放入回收站）

```bash
gkeep delete <id-or-title>
```

### 添加标签

```bash
gkeep labels              # List all labels
gkeep labels --json
```

### 导出/备份

```bash
gkeep dump                # All notes as JSON
gkeep dump > backup.json
```

## 颜色

支持的颜色：白色、红色、橙色、黄色、绿色、青色、蓝色、深蓝色、紫色、粉色、棕色、灰色

## 工作原理

- 该工具使用 [gkeepapi](https://github.com/kiwiz/gkeepapi)（拥有 1,600 多个星标，持续维护中）——这是一个非官方的 Google Keep 客户端库
- 通过 [gpsoauth](https://github.com/simon-weber/gpsoauth) 进行认证，利用 Google Play Services 的 OAuth 流程获取 master 令牌
- 状态信息会缓存到本地文件 `.config/state.json` 中，以便在初次同步后快速启动
- Master 令牌不会过期，因此无需重新认证
- **注意：此为非官方 API**——Google 可能随时更改其兼容性（但 gkeepapi 多年来一直保持稳定）

## 安全提示

- Master 令牌会授予对关联 Google 账户的**完全访问权限**
- 凭据以 600 权限存储在 `.config/` 文件中
- **切勿将 `.config/` 文件提交到版本控制系统中**
- `delete` 命令会将笔记放入回收站（可恢复）——不会永久删除笔记