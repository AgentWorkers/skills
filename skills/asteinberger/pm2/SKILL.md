---
name: pm2
description: 使用 PM2 进程管理器来管理 Node.js 应用程序。它可用于在生产环境中部署、监控以及自动重启 Node.js 应用程序。内容包括：启动应用程序、查看日志、设置应用程序在系统启动时自动运行，以及管理多个进程。
---

# PM2 进程管理器

这是一个专为 Node.js 开发的生产环境进程管理器，内置了负载均衡功能。

## 安装

```bash
npm install -g pm2
```

## 快速入门

```bash
# Start an app
pm2 start app.js
pm2 start npm --name "my-app" -- start
pm2 start "npm run start" --name my-app

# With specific port/env
pm2 start npm --name "my-app" -- start -- --port 3000
PORT=3000 pm2 start npm --name "my-app" -- start
```

## 常用命令

```bash
# List processes
pm2 list
pm2 ls

# Logs
pm2 logs              # All logs
pm2 logs my-app       # Specific app
pm2 logs --lines 100  # Last 100 lines

# Control
pm2 restart my-app
pm2 stop my-app
pm2 delete my-app
pm2 reload my-app     # Zero-downtime reload

# Info
pm2 show my-app
pm2 monit             # Real-time monitor
```

## 启动时自动启动

```bash
# Save current process list
pm2 save

# Generate startup script (run the output command with sudo)
pm2 startup

# Example output - run this:
# sudo env PATH=$PATH:/opt/homebrew/bin pm2 startup launchd -u username --hp /Users/username
```

## Next.js / 生产环境构建

```bash
# Build first
npm run build

# Start production server
pm2 start npm --name "my-app" -- start

# Or with ecosystem file
pm2 start ecosystem.config.js
```

## 生态系统配置文件（ecosystem.config.js）

```javascript
module.exports = {
  apps: [{
    name: 'my-app',
    script: 'npm',
    args: 'start',
    cwd: '/path/to/app',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    }
  }]
}
```

## 有用的参数

| 参数 | 说明 |
|------|-------------|
| `--name` | 进程名称 |
| `--watch` | 文件更改时自动重启 |
| `-i max` | 集群模式（使用所有 CPU） |
| `--max-memory-restart 200M` | 内存限制达到时自动重启 |
| `--cron "0 * * * *"` | 定时重启 |

## 清理

```bash
pm2 delete all        # Remove all processes
pm2 kill              # Kill PM2 daemon
pm2 unstartup         # Remove startup script
```