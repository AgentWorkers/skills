---
name: tidbyt-status
description: 这是一个HTTP API服务器，用于暴露OpenClaw代理的状态信息，以便与Tidbyt LED显示屏进行集成。该服务器可用于创建与Tidbyt设备的集成方案、构建状态仪表板，或在64x32像素的显示屏上显示代理的活动情况。它返回的JSON数据包含代理的状态、表情符号、活动级别以及任务数量等信息。
---
# Tidbyt状态显示 - Scout组件

本文档介绍了如何将Scout的状态信息完整地显示在Tidbyt的64x32 LED显示屏上。

## 组件

1. **状态API服务器** (`scripts/status_server.py`) - 以JSON格式提供Scout的状态信息。
2. **Tidbyt应用程序** (`scout_status.star`) - 用于在Tidbyt显示屏上渲染状态信息的Starlark应用程序。

## 快速入门

### 1. 启动状态API服务器

```bash
cd ~/.openclaw/workspace/skills/tidbyt-status
python3 scripts/status_server.py
```

API地址：`http://localhost:8765/status`

### 2. 安装Pixlet（Tidbyt开发工具）

**macOS:**
```bash
brew install tidbyt/tidbyt/pixlet
```

**Linux:**
从[GitHub仓库](https://github.com/tidbyt/pixlet/releases/latest)下载。

### 3. 在本地测试

在`scout_status.star`文件（第10行）中更新IP地址：
```python
DEFAULT_API_URL = "http://YOUR-LOCAL-IP:8765/status"
```

执行渲染并启动服务器：
```bash
pixlet serve scout_status.star
```

访问`http://localhost:8080`进行预览。

### 4. 将应用程序推送到Tidbyt设备

首先登录并获取设备ID：
```bash
pixlet login
pixlet devices
```

在Tidbyt设备上运行应用程序：
```bash
pixlet render scout_status.star
```

将应用程序推送到Tidbyt设备：
```bash
pixlet push --installation-id Scout <YOUR-DEVICE-ID> scout_status.webp
```

## 显示功能

- **代理名称 + 表情符号**（🦅）位于顶部，带有动画效果的脸部表情。
- **状态对应的面部表情**：
  - **聊天**（绿色）：正在闲聊，眼睛会动。
  - **工作**（黄色）：正在忙碌，脸部为黄色，眼睛呈紫色且专注。
  - **思考**（蓝色）：正在思考/处理任务，眼睛会眨动。
  - **睡眠**（灰色）：处于空闲/睡眠状态，眼睛闭合。
- **任务数量**：当前正在运行的子代理任务数量。
- **最近活动**：滚动显示的文本，展示最近的活动内容。

## API响应格式

状态服务器返回的JSON格式如下：
```json
{
  "agent": "Scout",
  "emoji": "🦅",
  "status": "chatting|working|thinking|sleeping",
  "timestamp": "2026-02-06T14:30:00",
  "active_tasks": 0,
  "last_activity": "2026-02-06T14:25:00",
  "recent_activity": "Chatting with user..."
}
```

**状态类型**：
- `chatting`：主会话处于活跃状态，没有后台任务。
- `working`：子代理会话正在运行（处理任务）。
- `thinking`：有活动，但具体内容不明确。
- `sleeping`：超过1小时没有活动。

## 配置

### 自定义API端口

```bash
PORT=9000 python3 scripts/status_server.py
```

### 在Tidbyt应用程序中配置API地址

在将应用程序推送到Tidbyt设备时，通过移动应用程序进行配置：
1. 点击Scout的安装项。
2. 进入设置 → API地址。
3. 输入完整的API地址。

## 将API服务器作为服务运行

### systemd（Linux）

创建`/etc/systemd/system/scout-status.service`文件：
```ini
[Unit]
Description=Scout Status API for Tidbyt
After=network.target

[Service]
Type=simple
User=<username>
WorkingDirectory=/home/<username>/.openclaw/workspace/skills/tidbyt-status
ExecStart=/usr/bin/python3 scripts/status_server.py
Restart=always
Environment="PORT=8765"

[Install]
WantedBy=multi-user.target
```

启用并启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable scout-status
sudo systemctl start scout-status
```

### 手动后台运行

```bash
nohup python3 scripts/status_server.py > /tmp/scout-status.log 2>&1 &
```

## 网络配置

为了让Tidbyt设备能够访问API：
1. **查找本地IP地址：**
   ```bash
   hostname -I | awk '{print $1}'
   ```

2. **（如需要）更新防火墙设置：**
   ```bash
   sudo ufw allow 8765/tcp
   ```

3. **从其他设备进行测试：**
   ```bash
   curl http://YOUR-IP:8765/status
   ```

## 状态检测逻辑

服务器会监控`~/.openclaw/agents/main/sessions/*.jsonl`文件：
- **活跃状态**：在过去5分钟内有任何会话被修改。
- **空闲状态**：没有最近的活动记录。
- **活跃任务**：子代理会话的数量（不包括主会话）。
- **最近活动**：显示自上次活动以来的时间。

## 自定义设置

### 更改表情符号

编辑`scripts/status_server.py`文件的第16行：
```python
"emoji": "🦅",  # Change to any emoji
```

### 调整活动检测阈值

编辑`scripts/status_server.py`文件的第34行（默认值为300秒）：
```python
if age_seconds < 300:  # Change threshold here
```

### 修改显示颜色

编辑`scout_status.star`文件的第39-40行：
```python
status_color = "#00FF00" if status == "active" else "#888888"
```

## 故障排除

**API返回错误：**
- 检查OpenClaw是否正在运行。
- 确认`~/.openclaw/agents/main/sessions/`文件夹是否存在。

**Tidbyt显示“API错误”：**
- 确认从Tidbyt设备的网络中可以访问API地址。
- 检查防火墙设置。
- 使用`curl http://YOUR-IP:8765/status`进行测试。

**显示内容未更新：**
- Tidbyt应用程序大约每30秒刷新一次（请参考代码中的`ttl_seconds`设置）。
- 检查状态API服务器是否仍在运行。

## 相关文件

- `SKILL.md`：本文档。
- `scripts/status_server.py`：HTTP API服务器脚本。
- `scout_status.star`：Tidbyt应用程序代码。
- `tidbyt-status.skill`：打包后的应用程序文件。