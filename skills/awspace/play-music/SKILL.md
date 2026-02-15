# 🎵 播放音乐技能  
**具备暂停/继续/停止功能的音乐播放器**  
通过单一入口点进行控制，后台服务器实现全面管理  

## 快速开始  
1. 将音乐文件放入 `music` 文件夹（默认位置），或设置 `MUSIC_DIR` 环境变量。  
2. （推荐）安装 `pygame`：`pip install pygame`  
3. 使用方法：`./play-music play`  

## 单一入口点  
该技能的**唯一入口点**是 `./play-music`。  

### 命令接口  
```
./play-music help          - Show this help
./play-music list          - List available songs
./play-music play          - Play default song
./play-music pause         - Pause currently playing music
./play-music resume        - Resume paused music
./play-music stop          - Stop currently playing music
./play-music status        - Show playback status
./play-music <filename>    - Play specific song (e.g., song.mp3)
./play-music server-start  - Start music server manually
./play-music server-stop   - Stop music server
```  

## 示例  
```bash
# Play the default song
./play-music play

# Play a specific song
./play-music song.mp3

# Control playback
./play-music pause
./play-music resume
./play-music stop

# See what's available
./play-music list
```  

## 功能特点  
✅ **单一入口点**：无需纠结使用哪个脚本。  
✅ **全面的播放控制**：播放、暂停、继续、停止。  
✅ **高效资源利用**：需要时服务器自动启动，音乐停止时自动关闭。  
✅ **清晰的架构**：客户端与服务器分离。  
✅ **基于 pygame**：提供高质量的音频播放体验。  
✅ **跨平台兼容**：支持 macOS、Windows 和 Linux。  

## 设置  
### 1. 安装 Pygame（推荐）  
若需实现完整的暂停/继续/停止功能，请执行以下操作：  
```bash
pip install pygame
```  

### 2. 添加音乐文件  
将音乐文件放入以下位置：  
- 默认位置：`./music`（相对于脚本所在目录）  
- 自定义位置：设置 `MUSIC_DIR` 环境变量。  

### 3. 配置  
```bash
# Set custom music directory
export MUSIC_DIR="/path/to/your/music"

# Set default song name
export DEFAULT_SONG="my-song.mp3"
```  

## 工作原理  
该技能采用清晰的客户端-服务器架构：  
1. `play-music`：作为单一入口点，整合了所有客户端功能。  
2. `music-server.py`：负责后台音乐播放的服务器程序。  
3. `Pygame mixer`：确保音频播放的高质量及全面的控制功能。  

**高效资源利用**：服务器在音乐播放时自动启动，在音乐停止时自动关闭，从而节省系统资源，同时保持客户端-服务器架构的便捷性。  

## 故障排除  
- **尝试暂停/继续/停止时无法播放音乐？**  
  先执行 `./play-music play` 命令开始播放音乐。  
- **找不到音乐目录？**  
  创建相应的目录：`mkdir music`，或设置 `MUSIC_DIR` 环境变量。  
- **未安装 pygame？**  
  安装 `pygame`：`pip install pygame`。  
- **服务器无法启动？**  
  检查端口 12346 是否可用，或关闭其他正在运行的服务器程序：  
```bash
pkill -f "music-server.py"
./play-music server-start
```  

## 文件结构  
```
play-music/
├── play-music           # Single entry point (Python script)
├── music-server.py      # Background server
├── SKILL.md            # This documentation
├── README.md           # User documentation
├── _meta.json          # Skill metadata
└── .gitignore          # Git ignore file
```  
文件结构简洁明了，无冗余文件。  

## 与 OpenClaw 的集成  
将该技能注册到 OpenClaw 后，即可使用它来执行音乐播放任务。该技能提供了所需的工具和功能，支持音乐的暂停、继续和停止操作。