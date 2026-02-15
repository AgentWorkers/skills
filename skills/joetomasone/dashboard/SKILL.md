# 仪表板技能

为您的Clawdbot代理构建并运行一个类似看板（Kanban）的任务管理仪表板。

## 概述

此技能创建了一个本地Web仪表板，可让您：
- 在看板中管理任务（待办 → 进行中 → 已完成 → 归档）
- 实时监控代理状态（在线/思考中/准备就绪）
- 为代理添加备注以便其在心跳检查时查看
- 查看操作日志和快速访问交付物（deliverables）

## 快速开始

运行设置脚本以安装并启动仪表板：

```bash
bash /path/to/skills/dashboard/setup.sh
```

或者让您的代理运行它：
> 设置并启动我的Clawdbot仪表板

## 手动设置

### 1. 安装依赖项

```bash
# Ubuntu/Debian
apt-get install -y python3-flask python3-flask-cors

# Or with pip
pip3 install flask flask-cors
```

### 2. 创建仪表板目录

```bash
mkdir -p ~/clawd-dashboard/{templates,static/css,static/js,data}
```

### 3. 复制文件

将这些文件从技能的`src/`目录复制到以下路径：
- `app.py` → `~/clawd-dashboard/`
- `templates/index.html` → `~/clawd-dashboard/templates/`
- `static/css/style.css` → `~/clawd-dashboard/static/css/`
- `static/js/dashboard.js` → `~/clawd-dashboard/static/js/`

### 4. 启动仪表板

```bash
cd ~/clawd-dashboard
python3 app.py
```

仪表板的访问地址为 **http://localhost:5050**

## 配置

### 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `CLAWD_WORKSPACE` | `/root/clawd` | 代理工作空间的路径 |
| `DASHBOARD_PORT` | `5050` | 仪表板运行的端口 |

### 自定义

编辑`app.py`以进行自定义：
- **交付物（Deliverables）**：修改`get_deliverables()`函数以添加您自己的文件夹快捷方式
- **代理ID（Agent ID）**：如果您的代理名称不是“clawd”，请更改`get_agent_status()`函数中的会话键模式

## 功能

### 看板（Kanban Board）
- 可在列之间拖放任务
- 列采用颜色编码（红色=待办，黄色=进行中，绿色=已完成，灰色=已归档）
- 点击即可编辑任何任务
- 任务信息会保存在`data/tasks.json`文件中

### 代理状态（Agent Status）
- 每10秒查询一次`clawdbot status --json`命令
- 显示代理的在线/离线状态、思考中/准备就绪的状态
- 显示模型名称和令牌使用情况

### 备注部分（Notes Section）
- 为代理添加说明
- 代理可以在心跳检查时读取这些备注
- 备注信息保存在`data/notes.json`文件中

### 操作日志（Action Log）
- 记录任务的创建/移动/删除操作
- 所有操作都会带有时间戳
- 最近100条记录保存在`data/action_log.json`文件中

## 作为服务运行

为了在退出登录后仍保持仪表板运行：

```bash
# Using systemd (recommended)
cat > /etc/systemd/system/clawd-dashboard.service << 'EOF'
[Unit]
Description=Clawd Dashboard
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/clawd-dashboard
ExecStart=/usr/bin/python3 app.py
Restart=always
Environment=CLAWD_WORKSPACE=/root/clawd

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable clawd-dashboard
systemctl start clawd-dashboard
```

## 安全注意事项

- 仪表板默认**没有身份验证**功能
- 仅应在受信任的网络环境中运行（如localhost、Tailscale、VPN）
- 请勿在没有添加身份验证机制的情况下将其暴露到公共互联网

## 故障排除

### “状态显示为离线”
- 确认`clawdbot status --json`命令在命令行中可以正常执行
- 验证代理ID的模式是否与您的设置匹配

### “任务无法保存”
- 确认`data/`目录存在且可写入
- 查看终端或`/tmp/dashboard.log`文件中的错误信息

### “端口已被占用”
- 更改端口：运行`python3 app.py`，然后编辑`app.run()`函数中的端口设置
- 或者终止现有进程：`pkill -f "python3 app.py"`

## 文件参考

```
clawd-dashboard/
├── app.py                 # Flask backend (API + routes)
├── data/
│   ├── tasks.json         # Kanban tasks
│   ├── notes.json         # Notes for agent
│   └── action_log.json    # Activity history
├── static/
│   ├── css/
│   │   └── style.css      # Dark theme styles
│   └── js/
│       └── dashboard.js   # Frontend logic
└── templates/
    └── index.html         # Main page template
```

## 致谢

本技能的灵感来源于Nate Herk的Clawdbot视频中的“Klaus Dashboard”。