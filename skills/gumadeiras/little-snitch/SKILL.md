---
name: little-snitch
description: 在 macOS 上控制 Little Snitch 防火墙。可以查看日志、管理防火墙配置文件（profiles）和规则组（rule groups），以及监控网络流量。适用于用户需要检查防火墙的运行状态、启用/禁用特定配置文件或黑名单，或排查网络连接问题的场景。
---

# Little Snitch CLI

用于在 macOS 上控制 Little Snitch 网络监控/防火墙工具。

## 设置

在 **Little Snitch → 首选项 → 安全 → 允许通过终端访问** 中启用 CLI 访问功能。

启用后，您可以在终端中使用 `littlesnitch` 命令。

⚠️ **安全警告：** `littlesnitch` 命令功能非常强大，可能会被恶意软件滥用。启用访问权限后，必须采取预防措施，确保不受信任的进程无法获取 root 权限。

参考链接：https://help.obdev.at/littlesnitch5/adv-commandline

## 命令

| 命令 | 是否需要 root 权限 | 描述 |
|---------|-------|-------------|
| `--version` | 否 | 显示版本信息 |
| `restrictions` | 否 | 显示许可证状态 |
| `log` | 否 | 读取日志信息 |
| `profile` | 是 | 激活/停用配置文件 |
| `rulegroup` | 是 | 启用/禁用规则组及黑名单 |
| `log-traffic` | 是 | 打印流量日志数据 |
| `list-preferences` | 是 | 列出所有配置选项 |
| `read-preference` | 是 | 读取配置选项的值 |
| `write-preference` | 是 | 写入配置选项的值 |
| `export-model` | 是 | 导出数据模型（备份） |
| `restore-model` | 是 | 从备份中恢复数据模型 |
| `capture-traffic` | 是 | 捕获进程流量数据 |

## 示例

### 查看最近日志（无需 root 权限）
```bash
littlesnitch log --last 10m --json
```

### 实时流式显示日志（无需 root 权限）
```bash
littlesnitch log --stream
```

### 检查许可证状态（无需 root 权限）
```bash
littlesnitch restrictions
```

### 激活配置文件（需要 root 权限）
```bash
sudo littlesnitch profile --activate "Silent Mode"
```

### 禁用所有配置文件（需要 root 权限）
```bash
sudo littlesnitch profile --deactivate-all
```

### 启用/禁用规则组（需要 root 权限）
```bash
sudo littlesnitch rulegroup --enable "My Rules"
sudo littlesnitch rulegroup --disable "Blocklist"
```

### 查看流量历史记录（需要 root 权限）
```bash
sudo littlesnitch log-traffic --begin-date "2026-01-25 00:00:00"
```

### 实时显示流量数据（需要 root 权限）
```bash
sudo littlesnitch log-traffic --stream
```

### 备份配置（需要 root 权限）
```bash
sudo littlesnitch export-model > backup.json
```

## 日志选项

| 选项 | 描述 |
|--------|-------------|
| `--last <时间>[分钟\|小时\|天]` | 显示过去 N 分钟/小时/天的日志记录 |
| `--stream` | 实时流式显示日志信息 |
| `--json` | 以 JSON 格式输出日志 |
| `--predicate <字符串>` | 根据指定条件过滤日志记录 |

## 注意事项

- 仅支持 macOS 系统 |
- 许多命令需要使用 `sudo`（root 权限）执行 |
- 配置文件：预定义的规则集（例如“静默模式”、“警报模式”）
- 规则组：自定义的规则集合和黑名单