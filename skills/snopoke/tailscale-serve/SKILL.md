# Tailscale Serve 技能

使用 `tailscale serve` 管理多个路径，避免冲突。

## 关键命令

### 检查当前正在提供的内容
```bash
tailscale serve status
```

### 在特定路径上提供目录或文件
```bash
# Directory
tailscale serve --bg --set-path /slides /path/to/directory

# Single file
tailscale serve --bg --set-path /presentation /path/to/file.html

# Port (for running services)
tailscale serve --bg --set-path /api http://localhost:8080
```

### 从根目录的某个端口提供内容（会覆盖所有其他内容）
```bash
tailscale serve --bg 8888
```

### 删除某个特定路径
```bash
tailscale serve --https=443 /slides off
```

### 重置所有服务配置
```bash
tailscale serve reset
```

## 重要说明

- **路径冲突：** 在 `/` 路径上提供内容会覆盖所有其他路径。
- **后台模式：** 使用 `--bg` 选项使服务在后台运行。
- **多个路径：** 可以使用不同的路径同时提供多个资源。
- **先查看状态：** 在添加新路径之前，请务必先使用 `tailscale serve status` 命令查看当前服务状态。

## 常见用法

### 同时提供演示文稿和控制界面
```bash
# If control UI is at /, serve presentation at a subpath
tailscale serve --bg --set-path /slides ~/clawd/personal-agents-presentation.html

# Access at: https://[hostname].ts.net/slides
```

### 提供多个目录
```bash
tailscale serve --bg --set-path /docs ~/documents
tailscale serve --bg --set-path /slides ~/presentations
tailscale serve --bg --set-path /files ~/files
```

### 提供本地开发服务器
```bash
tailscale serve --bg --set-path /app http://localhost:3000
```

## 工作流程

1. 查看当前服务状态：`tailscale serve status`
2. 选择一个未使用的路径（例如 `/slides`、`/docs`、`/api`）。
3. 使用 `--set-path /your-path /source` 命令提供相应资源。
4. 再次使用 `tailscale serve status` 命令验证服务状态。
5. 分享完整的 URL：`https://[hostname].ts.net/your-path`

## 故障排除

**“无法访问我提供的内容”**
- 查看 `tailscale serve status` 命令的输出，确认内容是否在预期的路径上。
- 是否有其他服务覆盖了根目录 `/`？

**“想用某个端口替换所有服务”**
```bash
tailscale serve reset
tailscale serve --bg 8888
```

**“想向现有配置中添加新服务”**
```bash
# Don't use reset! Just add with --set-path
tailscale serve --bg --set-path /newpath /source
```