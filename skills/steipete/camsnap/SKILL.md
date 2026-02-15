---
name: camsnap
description: 从 RTSP/ONVIF 相机中捕获帧或视频片段。
homepage: https://camsnap.ai
metadata: {"clawdbot":{"emoji":"📸","requires":{"bins":["camsnap"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/camsnap","bins":["camsnap"],"label":"Install camsnap (brew)"}]}}
---

# camsnap

使用 `camsnap` 从已配置的摄像头中抓取快照、视频片段或运动事件。

**设置**  
- 配置文件：`~/.config/camsnap/config.yaml`  
- 添加摄像头：`camsnap add --name kitchen --host 192.168.0.10 --user user --pass pass`  

**常用命令**  
- 发现摄像头：`camsnap discover --info`  
- 获取快照：`camsnap snap kitchen --out shot.jpg`  
- 录制视频片段：`camsnap clip kitchen --dur 5s --out clip.mp4`  
- 监控运动事件：`camsnap watch kitchen --threshold 0.2 --action '...'`  
- 检查摄像头状态：`camsnap doctor --probe`  

**注意事项**  
- 需要在系统路径（PATH）中安装 `ffmpeg`。  
- 建议先进行简短的测试拍摄，再录制较长的视频片段。