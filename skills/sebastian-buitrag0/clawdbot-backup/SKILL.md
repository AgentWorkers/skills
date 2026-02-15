---
name: clawdbot-backup
description: 备份和恢复 ClawdBot 的配置、技能、命令及设置。实现跨设备的数据同步，通过 Git 进行版本控制，自动化备份流程，并能够将配置迁移到新机器上。
homepage: https://github.com/clawdbot/backup-skill
metadata: {"clawdbot":{"emoji":"💾","requires":{"bins":["git","tar","rsync"],"env":[]}}}
---

# ClawdBot 备份技能

您可以直接通过 Clawdbot 在不同设备之间备份、恢复和同步 ClawdBot 的配置。

## 概述

此技能可帮助您：
- 备份所有 ClawdBot 数据和设置
- 从备份中恢复数据
- 在多台机器之间同步配置
- 对配置进行版本控制
- 自动化备份流程
- 将配置迁移到新设备

## ClawdBot 目录结构

### 关键位置

```
~/.claude/                    # Main ClawdBot directory
├── settings.json             # Global settings
├── settings.local.json       # Local overrides (machine-specific)
├── projects.json             # Project configurations
├── skills/                   # Your custom skills
│   ├── skill-name/
│   │   ├── SKILL.md
│   │   └── supporting-files/
│   └── another-skill/
├── commands/                 # Custom slash commands (legacy)
│   └── command-name.md
├── contexts/                 # Saved contexts
├── templates/                # Response templates
└── mcp/                      # MCP server configurations
    └── servers.json

~/projects/                   # Your projects (optional backup)
├── project-1/
│   └── .claude/              # Project-specific config
│       ├── settings.json
│       └── skills/
└── project-2/
```

### 需要备份的内容

```
ESSENTIAL (Always backup):
✓ ~/.claude/skills/           # Custom skills
✓ ~/.claude/commands/         # Custom commands
✓ ~/.claude/settings.json     # Global settings
✓ ~/.claude/mcp/              # MCP configurations

RECOMMENDED (Usually backup):
✓ ~/.claude/contexts/         # Saved contexts
✓ ~/.claude/templates/        # Templates
✓ Project .claude/ folders    # Project configs

OPTIONAL (Case by case):
○ ~/.claude/settings.local.json  # Machine-specific
○ Cache directories              # Can be rebuilt
○ Log files                      # Usually not needed
```

## 快速备份命令

### 完整备份

```bash
# Create timestamped backup
BACKUP_DIR="$HOME/clawdbot-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="clawdbot_backup_$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

tar -czvf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" \
  -C "$HOME" \
  .claude/skills \
  .claude/commands \
  .claude/settings.json \
  .claude/mcp \
  .claude/contexts \
  .claude/templates \
  2>/dev/null

echo "Backup created: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
```

### 仅备份所需内容的命令

```bash
# Backup just skills
tar -czvf ~/clawdbot_skills_$(date +%Y%m%d).tar.gz \
  -C "$HOME" .claude/skills .claude/commands
```

### 从备份中恢复

```bash
# Restore full backup
BACKUP_FILE="$HOME/clawdbot-backups/clawdbot_backup_20260129.tar.gz"

# Preview contents first
tar -tzvf "$BACKUP_FILE"

# Restore (will overwrite existing)
tar -xzvf "$BACKUP_FILE" -C "$HOME"

echo "Restore complete!"
```

## 备份脚本

### 全功能备份脚本

```bash
#!/bin/bash
# clawdbot-backup.sh - Comprehensive ClawdBot backup tool

set -e

# Configuration
BACKUP_ROOT="${CLAWDBOT_BACKUP_DIR:-$HOME/clawdbot-backups}"
CLAUDE_DIR="$HOME/.claude"
MAX_BACKUPS=10  # Keep last N backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if ClawdBot directory exists
check_claude_dir() {
    if [ ! -d "$CLAUDE_DIR" ]; then
        log_error "ClawdBot directory not found: $CLAUDE_DIR"
        exit 1
    fi
}

# Create backup
create_backup() {
    local backup_type="${1:-full}"
    local backup_name="clawdbot_${backup_type}_${TIMESTAMP}"
    local backup_path="$BACKUP_ROOT/$backup_name.tar.gz"
    
    mkdir -p "$BACKUP_ROOT"
    
    log_info "Creating $backup_type backup..."
    
    case $backup_type in
        full)
            tar -czvf "$backup_path" \
                -C "$HOME" \
                .claude/skills \
                .claude/commands \
                .claude/settings.json \
                .claude/settings.local.json \
                .claude/projects.json \
                .claude/mcp \
                .claude/contexts \
                .claude/templates \
                2>/dev/null || true
            ;;
        skills)
            tar -czvf "$backup_path" \
                -C "$HOME" \
                .claude/skills \
                .claude/commands \
                2>/dev/null || true
            ;;
        settings)
            tar -czvf "$backup_path" \
                -C "$HOME" \
                .claude/settings.json \
                .claude/settings.local.json \
                .claude/mcp \
                2>/dev/null || true
            ;;
        *)
            log_error "Unknown backup type: $backup_type"
            exit 1
            ;;
    esac
    
    if [ -f "$backup_path" ]; then
        local size=$(du -h "$backup_path" | cut -f1)
        log_info "Backup created: $backup_path ($size)"
    else
        log_error "Backup failed!"
        exit 1
    fi
}

# List backups
list_backups() {
    log_info "Available backups in $BACKUP_ROOT:"
    echo ""
    
    if [ -d "$BACKUP_ROOT" ]; then
        ls -lh "$BACKUP_ROOT"/*.tar.gz 2>/dev/null | \
            awk '{print $9, $5, $6, $7, $8}' || \
            echo "No backups found."
    else
        echo "Backup directory doesn't exist."
    fi
}

# Restore backup
restore_backup() {
    local backup_file="$1"
    
    if [ -z "$backup_file" ]; then
        log_error "Please specify backup file"
        list_backups
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        # Try relative path in backup dir
        backup_file="$BACKUP_ROOT/$backup_file"
    fi
    
    if [ ! -f "$backup_file" ]; then
        log_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    log_warn "This will overwrite existing configuration!"
    read -p "Continue? (y/N) " confirm
    
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        log_info "Restore cancelled."
        exit 0
    fi
    
    log_info "Restoring from: $backup_file"
    tar -xzvf "$backup_file" -C "$HOME"
    log_info "Restore complete!"
}

# Clean old backups
cleanup_backups() {
    log_info "Cleaning old backups (keeping last $MAX_BACKUPS)..."
    
    cd "$BACKUP_ROOT" 2>/dev/null || return
    
    local count=$(ls -1 *.tar.gz 2>/dev/null | wc -l)
    
    if [ "$count" -gt "$MAX_BACKUPS" ]; then
        local to_delete=$((count - MAX_BACKUPS))
        ls -1t *.tar.gz | tail -n "$to_delete" | xargs rm -v
        log_info "Removed $to_delete old backup(s)"
    else
        log_info "No cleanup needed ($count backups)"
    fi
}

# Show backup stats
show_stats() {
    log_info "ClawdBot Backup Statistics"
    echo ""
    
    echo "=== Directory Sizes ==="
    du -sh "$CLAUDE_DIR"/skills 2>/dev/null || echo "Skills: N/A"
    du -sh "$CLAUDE_DIR"/commands 2>/dev/null || echo "Commands: N/A"
    du -sh "$CLAUDE_DIR"/mcp 2>/dev/null || echo "MCP: N/A"
    du -sh "$CLAUDE_DIR" 2>/dev/null || echo "Total: N/A"
    
    echo ""
    echo "=== Skills Count ==="
    find "$CLAUDE_DIR/skills" -name "SKILL.md" 2>/dev/null | wc -l | xargs echo "Skills:"
    find "$CLAUDE_DIR/commands" -name "*.md" 2>/dev/null | wc -l | xargs echo "Commands:"
    
    echo ""
    echo "=== Backup Directory ==="
    if [ -d "$BACKUP_ROOT" ]; then
        du -sh "$BACKUP_ROOT"
        ls -1 "$BACKUP_ROOT"/*.tar.gz 2>/dev/null | wc -l | xargs echo "Backup files:"
    else
        echo "No backups yet"
    fi
}

# Usage
usage() {
    cat << EOF
ClawdBot Backup Tool

Usage: $(basename $0) <command> [options]

Commands:
    backup [type]   Create backup (types: full, skills, settings)
    restore <file>  Restore from backup file
    list            List available backups
    cleanup         Remove old backups (keep last $MAX_BACKUPS)
    stats           Show backup statistics
    help            Show this help

Examples:
    $(basename $0) backup              # Full backup
    $(basename $0) backup skills       # Skills only
    $(basename $0) restore latest.tar.gz
    $(basename $0) list
    $(basename $0) cleanup

Environment:
    CLAWDBOT_BACKUP_DIR    Backup directory (default: ~/clawdbot-backups)

EOF
}

# Main
main() {
    check_claude_dir
    
    case "${1:-help}" in
        backup)
            create_backup "${2:-full}"
            ;;
        restore)
            restore_backup "$2"
            ;;
        list)
            list_backups
            ;;
        cleanup)
            cleanup_backups
            ;;
        stats)
            show_stats
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            log_error "Unknown command: $1"
            usage
            exit 1
            ;;
    esac
}

main "$@"
```

### 保存和使用备份文件

```bash
# Save script
cat > ~/.local/bin/clawdbot-backup << 'SCRIPT'
# Paste script content here
SCRIPT

chmod +x ~/.local/bin/clawdbot-backup

# Usage
clawdbot-backup backup          # Full backup
clawdbot-backup backup skills   # Skills only
clawdbot-backup list            # List backups
clawdbot-backup restore <file>  # Restore
```

## Git 版本控制

### 初始化 Git 仓库

```bash
cd ~/.claude

# Initialize git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Machine-specific settings
settings.local.json

# Cache and temp files
cache/
*.tmp
*.log

# Large files
*.tar.gz
*.zip

# Sensitive data (if any)
*.pem
*.key
credentials/
EOF

# Initial commit
git add .
git commit -m "Initial ClawdBot configuration backup"
```

### 将备份推送到远程仓库

```bash
# Add remote (GitHub, GitLab, etc)
git remote add origin git@github.com:username/clawdbot-config.git

# Push
git push -u origin main
```

### 日常工作流程

```bash
# After making changes to skills/settings
cd ~/.claude
git add .
git commit -m "Updated skill: trading-bot"
git push
```

### 自动提交脚本

```bash
#!/bin/bash
# auto-commit-claude.sh - Auto commit changes

cd ~/.claude || exit 1

# Check for changes
if git diff --quiet && git diff --staged --quiet; then
    echo "No changes to commit"
    exit 0
fi

# Get changed files for commit message
CHANGED=$(git status --short | head -5 | awk '{print $2}' | tr '\n' ', ')

git add .
git commit -m "Auto-backup: $CHANGED ($(date +%Y-%m-%d))"
git push 2>/dev/null || echo "Push failed (offline?)"
```

## 在设备之间同步配置

### 方法 1：使用 Git 进行同步

```bash
# On new device
git clone git@github.com:username/clawdbot-config.git ~/.claude

# Pull latest changes
cd ~/.claude && git pull

# Push local changes
cd ~/.claude && git add . && git commit -m "Update" && git push
```

### 方法 2：使用 Rsync 进行同步

```bash
# Sync to remote server
rsync -avz --delete \
    ~/.claude/ \
    user@server:~/clawdbot-backup/

# Sync from remote server
rsync -avz --delete \
    user@server:~/clawdbot-backup/ \
    ~/.claude/
```

### 方法 3：使用云存储进行同步

```bash
# Backup to cloud folder (Dropbox, Google Drive, etc)
CLOUD_DIR="$HOME/Dropbox/ClawdBot"

# Sync skills
rsync -avz ~/.claude/skills/ "$CLOUD_DIR/skills/"
rsync -avz ~/.claude/commands/ "$CLOUD_DIR/commands/"

# Copy settings
cp ~/.claude/settings.json "$CLOUD_DIR/"
```

### 同步脚本

```bash
#!/bin/bash
# sync-clawdbot.sh - Sync ClawdBot config between devices

SYNC_DIR="${CLAWDBOT_SYNC_DIR:-$HOME/Dropbox/ClawdBot}"
CLAUDE_DIR="$HOME/.claude"

sync_to_cloud() {
    echo "Syncing to cloud..."
    mkdir -p "$SYNC_DIR"
    
    rsync -avz --delete "$CLAUDE_DIR/skills/" "$SYNC_DIR/skills/"
    rsync -avz --delete "$CLAUDE_DIR/commands/" "$SYNC_DIR/commands/"
    rsync -avz "$CLAUDE_DIR/mcp/" "$SYNC_DIR/mcp/" 2>/dev/null
    cp "$CLAUDE_DIR/settings.json" "$SYNC_DIR/" 2>/dev/null
    
    echo "Sync complete!"
}

sync_from_cloud() {
    echo "Syncing from cloud..."
    
    rsync -avz "$SYNC_DIR/skills/" "$CLAUDE_DIR/skills/"
    rsync -avz "$SYNC_DIR/commands/" "$CLAUDE_DIR/commands/"
    rsync -avz "$SYNC_DIR/mcp/" "$CLAUDE_DIR/mcp/" 2>/dev/null
    
    # Don't overwrite local settings by default
    if [ ! -f "$CLAUDE_DIR/settings.json" ]; then
        cp "$SYNC_DIR/settings.json" "$CLAUDE_DIR/" 2>/dev/null
    fi
    
    echo "Sync complete!"
}

case "$1" in
    push) sync_to_cloud ;;
    pull) sync_from_cloud ;;
    *)
        echo "Usage: $0 {push|pull}"
        echo "  push - Upload local config to cloud"
        echo "  pull - Download cloud config to local"
        ;;
esac
```

## 自动化备份

### 使用 Cron Job（Linux/Mac）

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /home/user/.local/bin/clawdbot-backup backup full

# Add weekly cleanup on Sundays
0 3 * * 0 /home/user/.local/bin/clawdbot-backup cleanup

# Add git auto-commit every 6 hours
0 */6 * * * cd ~/.claude && git add . && git commit -m "Auto-backup $(date +\%Y-\%m-\%d)" && git push 2>/dev/null
```

### 使用 systemd 定时器（Linux）

```bash
# Create service: ~/.config/systemd/user/clawdbot-backup.service
cat > ~/.config/systemd/user/clawdbot-backup.service << 'EOF'
[Unit]
Description=ClawdBot Backup

[Service]
Type=oneshot
ExecStart=/home/user/.local/bin/clawdbot-backup backup full
EOF

# Create timer: ~/.config/systemd/user/clawdbot-backup.timer
cat > ~/.config/systemd/user/clawdbot-backup.timer << 'EOF'
[Unit]
Description=Daily ClawdBot Backup

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable
systemctl --user enable clawdbot-backup.timer
systemctl --user start clawdbot-backup.timer
```

### 使用 Launchd（macOS）

```bash
# Create plist: ~/Library/LaunchAgents/com.clawdbot.backup.plist
cat > ~/Library/LaunchAgents/com.clawdbot.backup.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.clawdbot.backup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/username/.local/bin/clawdbot-backup</string>
        <string>backup</string>
        <string>full</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
EOF

# Load
launchctl load ~/Library/LaunchAgents/com.clawdbot.backup.plist
```

## 迁移指南

### 将配置迁移到新设备

```bash
# === On OLD machine ===

# 1. Create full backup
clawdbot-backup backup full

# 2. Copy backup file to new machine
scp ~/clawdbot-backups/clawdbot_full_*.tar.gz newmachine:~/

# Or use git
cd ~/.claude
git add . && git commit -m "Pre-migration backup"
git push


# === On NEW machine ===

# Method A: From backup file
tar -xzvf ~/clawdbot_full_*.tar.gz -C ~

# Method B: From git
git clone git@github.com:username/clawdbot-config.git ~/.claude

# 3. Verify
ls -la ~/.claude/skills/
```

### 导出单个技能

```bash
# Export one skill for sharing
SKILL_NAME="my-awesome-skill"
tar -czvf "${SKILL_NAME}.tar.gz" -C ~/.claude/skills "$SKILL_NAME"

# Import skill
tar -xzvf "${SKILL_NAME}.tar.gz" -C ~/.claude/skills/
```

### 导出所有技能以供共享

```bash
# Create shareable skills bundle (no personal settings)
tar -czvf clawdbot-skills-share.tar.gz \
    -C ~/.claude \
    skills \
    --exclude='*.local*' \
    --exclude='*personal*'
```

## 备份验证

### 验证备份文件的完整性

```bash
# Test backup without extracting
tar -tzvf backup.tar.gz > /dev/null && echo "Backup OK" || echo "Backup CORRUPT"

# List contents
tar -tzvf backup.tar.gz

# Verify specific file exists
tar -tzvf backup.tar.gz | grep "skills/my-skill/SKILL.md"
```

### 将备份文件与当前配置进行比较

```bash
# Extract to temp dir
TEMP_DIR=$(mktemp -d)
tar -xzf backup.tar.gz -C "$TEMP_DIR"

# Compare
diff -rq ~/.claude/skills "$TEMP_DIR/.claude/skills"

# Cleanup
rm -rf "$TEMP_DIR"
```

## 故障排除

### 常见问题

```bash
# Issue: Permission denied
chmod -R u+rw ~/.claude

# Issue: Backup too large
# Exclude cache and logs
tar --exclude='cache' --exclude='*.log' -czvf backup.tar.gz ~/.claude

# Issue: Restore overwrote settings
# Keep settings.local.json for machine-specific config
# It won't be overwritten if using proper backup

# Issue: Git conflicts after sync
cd ~/.claude
git stash
git pull
git stash pop
# Resolve conflicts manually if needed
```

### 在数据损坏时进行恢复

```bash
# If ~/.claude is corrupted

# 1. Move corrupted dir
mv ~/.claude ~/.claude.corrupted

# 2. Restore from backup
clawdbot-backup restore latest.tar.gz

# 3. Or restore from git
git clone git@github.com:username/clawdbot-config.git ~/.claude

# 4. Compare and recover anything missing
diff -rq ~/.claude ~/.claude.corrupted/
```

## 快速参考

### 常用命令

```bash
# Backup
tar -czvf ~/clawdbot-backup.tar.gz -C ~ .claude/skills .claude/commands .claude/settings.json

# Restore
tar -xzvf ~/clawdbot-backup.tar.gz -C ~

# List backup contents
tar -tzvf ~/clawdbot-backup.tar.gz

# Git backup
cd ~/.claude && git add . && git commit -m "Backup" && git push

# Git restore
cd ~/.claude && git pull
```

### 备份检查清单

```
Before major changes:
□ Create backup
□ Verify backup integrity
□ Note what you're changing

Regular maintenance:
□ Weekly full backup
□ Daily git commits (if using)
□ Monthly cleanup of old backups
□ Test restore procedure quarterly
```

## 资源

### 相关技能

```
- skill-creator - Create new skills
- mcp-builder - Configure MCP servers
- dotfiles - General dotfile management
```

### 文档资料

```
- ClawdBot Docs: docs.clawdbot.com
- Skills Guide: docs.clawdbot.com/skills
- MCP Setup: docs.clawdbot.com/mcp
```

---

**提示：** 在真正需要使用备份功能之前，请务必先测试其恢复过程。无法恢复的备份是没有意义的！