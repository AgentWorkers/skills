---
name: clawspotify
description: "控制 Spotify 播放功能：播放、暂停、继续播放、跳过当前曲目、返回上一首曲目、重新开始播放、搜索歌曲、将歌曲加入播放列表、调整音量、随机播放、重复播放以及查看当前正在播放的歌曲的状态。"
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      bins: ["bash", "python3"]
---
# ClawSpotify 🎵  
直接通过 OpenClaw 代理或终端控制您的 Spotify 播放功能。支持 **免费和高级** Spotify 账户。  

---

## 📦 安装  

### 通过 ClawHub（推荐）  
```bash  
clawhub install clawspotify  
```  

### 从 GitHub 手动安装  
```bash  
# 克隆主技能代码  
git clone https://github.com/ejatapibeda/ClawSpotify.git ~/.openclaw/workspace/skills/ClawSpotify  

# 创建虚拟环境  
python3 -m venv ~/.venv-clawspotify  

# 安装 SpotAPI（支持会话的修改版本）  
git clone https://github.com/ejatapibeda/SpotAPI.git ~/.openclaw/workspace/skills/SpotAPI  
~/.venv-clawspotify/bin/pip install -e ~/.openclaw/workspace/skills/SpotAPI  

# 创建包装脚本  
cat > ~/.local/bin/clawspotify << 'EOF'  
#!/bin/bash  
VENV="/home/$(whoami)/.venv-clawspotify"  
SCRIPT_DIR="/home/$(whoami)/.openclaw/workspace/skills/ClawSpotify"  
exec "$VENV/bin/python" "$SCRIPT_DIR/scripts/spotify.py" "$@"  
EOF  
chmod +x ~/.local/bin/clawspotify  

# 确保 ~/.local/bin 在 PATH 中  
export PATH="$HOME/.local/bin:$PATH"  
```  

### 依赖项  
- Python 3.10+  
- SpotAPI（来自 ejatapibeda 的自定义版本）  
- 活跃的 Spotify 账户（免费或高级）  
- 至少在一个设备（PC/手机/网页）上打开 Spotify 应用程序，以便播放命令生效。  

---

## 🔐 首次设置（身份验证）  
`clawspotify` 使用浏览器中的两个会话 cookie（`sp_dc` 和 `sp_key`）进行身份验证。每个账户只需执行此操作 **一次**。  

### 分步操作  

1. 在浏览器中打开 **[https://open.spotify.com](https://open.spotify.com)** 并 **登录**。  
2. 按 **F12** 打开开发者工具。  
3. 转到 **应用程序** 标签 → **Cookies** → `https://open.spotify.com`。  
4. 找到并复制 `sp_dc` 的值。  
5. 找到并复制 `sp_key` 的值。  
6. 运行：  
```bash  
clawspotify setup --sp-dc "AQC..." --sp-key "07c9..."  
```  

会话信息会保存在 `~/.config/spotapi/session.json` 文件中，并自动重用。  

#### 多账户支持  
```bash  
clawspotify setup --sp-dc "..." --sp-key "..." --id "work"  
clawspotify status --id "work"  
```  

> **注意：** Cookie 会定期过期。如果命令因 401 错误失败，请使用新的 Cookie 重新运行 `clawspotify setup`。  

---

## 🎮 命令  

### 当前播放状态  
```bash  
clawspotify status            # 默认账户  
clawspotify status --id work  # 特定账户  
```  

### 搜索音乐（不播放）  
```bash  
clawspotify search "Bohemian Rhapsody"        # 搜索曲目，显示前 5 个结果  
clawspotify search-playlist "Workout"         # 搜索播放列表，显示前 5 个结果  
```  

### 搜索并播放  
```bash  
clawspotify play "Bohemian Rhapsody"          # 播放第一个搜索结果  
clawspotify play "Bohemian Rhapsody" --index 2  # 选择第 2 个结果（索引从 0 开始）  
clawspotify play-playlist "Lofi Girl"         # 播放第一个播放列表结果  
```  

### 播放控制  
```bash  
clawspotify pause              # 暂停  
clawspotify resume            # 继续播放  
clawspotify skip                # 跳到下一首曲目  
clawspotify prev                # 跳到上一首曲目  
clawspotify restart             # 从头开始播放  
```  

### 队列  
```bash  
clawspotify queue "Stairway to Heaven"      # 添加歌曲到队列  
clawspotify queue "spotify:track:3z8h0TU..."    # 通过 URI 添加歌曲  
```  

### 音量  
```bash  
clawspotify volume 50             # 设置音量为 50%  
clawspotify volume 0              # 静音  
clawspotify volume 100            # 最大音量  
```  

### 随机播放/重复播放  
```bash  
clawspotify shuffle on            # 开启随机播放  
clawspotify shuffle off            # 关闭随机播放  
clawspotify repeat on            # 开启重复播放  
clawspotify repeat off            # 关闭重复播放  
```  

---

## 💡 使用提示  

- 为了使播放命令生效，至少需要在某个设备上打开 Spotify 应用程序。该技能会将播放任务转移到一个虚拟设备上，但需要一个活跃的会话。  
- **首次运行可能较慢**（10-30 秒），因为需要建立 WebSocket 连接并完成设备注册。后续命令会更快。  
- **会话标识符**：默认为 `"default"`。使用 `--id` 标志来管理多个 Spotify 账户。  
- **搜索功能**：使用艺术家名称 + 曲目名称可以获得最佳搜索结果。  
- **输出**：命令会显示状态信息（例如：“正在搜索...”，“正在播放：URI”）。  

---

## ⚠️ 故障排除  

### “未找到活跃的 Spotify 设备”  
- 在任何设备（PC、手机或网页）上打开 Spotify 并开始播放歌曲。  
- 确保使用的账户与浏览器中的 Cookie 对应。  

### “spotapi 未安装”或导入错误  
- 检查虚拟环境：`ls ~/.venv-clawspotify/bin/python`  
- 重新安装 SpotAPI：`~/.venv-clawspotify/bin/pip install -e ~/.openclaw/workspace/skills/SpotAPI`  

### 401 未授权/会话过期  
- Cookie（`sp_dc`、`sp_key`）已过期。使用浏览器中的新 Cookie 重新运行 `clawspotify setup`。  

### 命令超时或卡住  
- 该技能使用 WebSocket 进行实时状态更新。如果 Spotify 的 API 响应缓慢，命令可能会延迟。可以增加超时时间或使用后台执行。  
- 如果 OpenClaw 代理变得无响应，重启代理以重新加载技能。  

### 找不到包装脚本（`命令未找到：clawspotify`）  
- 确保 `~/.local/bin` 在 `PATH` 中：`echo $PATH`  
- 或直接运行：`~/.venv-clawspotify/bin/python ~/.openclaw/workspace/skills/ClawSpotify/scripts/spotify.py <command>`  

---

## 📂 文件位置  

| 组件          | 路径                                      |  
|------------------|-----------------------------------------|  
| 技能文件夹        | `~/.openclaw/workspace/skills/ClawSpotify`           |  
| 包装脚本        | `~/.local/bin/clawspotify`                    |  
| 虚拟环境        | `~/.venv-clawspotify`                    |  
| SpotAPI（可编辑）      | `~/.openclaw/workspace/skills/SpotAPI`              |  
| 会话凭证        | `~/.config/spotapi/session.json`                |  
| 主脚本        | `~/skills/ClawSpotify/scripts/spotify.py`            |  

---

## 🔧 代理实现说明  

通过 OpenClaw 代理使用此技能时：  
1. **播放命令**（如 `play`、`pause`、`skip` 等）是异步的。命令会在 Spotify 接受请求后返回结果，实际播放可能需要几秒钟。  
2. **长时间运行的操作**（如 `play`、`search`、`status`）建议使用后台执行或设置较长的超时时间（15-30 秒），以避免过早终止。  
3. **状态查询** 可能会因 WebSocket 延迟而超时。播放命令通常更可靠。  
4. **始终检查** Spotify 应用程序/设备的实际播放状态。CLI 只报告 Spotify 的响应情况。  
5. 如果技能变得无响应，重启 OpenClaw 代理以清除 WebSocket 连接。  

---

## 🌐 平台说明  

- **Linux/macOS**：原生支持 bash。  
- **Windows**：需要 WSL、Git Bash 或 Cygwin 来运行 `clawspotify` 脚本。或者，直接运行 Python：  
  ```bash  
  python ~/.openclaw/workspace/skills/ClawSpotify/scripts/spotify.py play "song name"  
  ```  

---

**版本：** 1.0.1（技能） | SpotAPI：1.2.7（自定义版本）  
**官方网站：** https://github.com/ejatapibeda/ClawSpotify  
**作者：** Deli（OpenClaw 代理）+ ejatapibeda（原始作者）