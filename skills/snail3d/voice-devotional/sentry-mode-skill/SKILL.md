---
name: sentry-mode
description: 带有AI分析功能的网络摄像头监控系统。提供两种模式：  
(1) 一次性分析模式：针对特定场景提出问题（例如：“房间里有人吗？”）；  
(2) BOLO（Be On Lookout）监控模式：持续监控并具备运动检测功能，可自定义需要关注的人员或物体列表（例如：“有没有戴黑帽子的人？”或“那个金发小女孩在哪里？”）。  
系统会触发运动检测警报，并在3分钟后自动停止警报。
---

# Sentry模式  
基于网络摄像头的监控系统，配备人工智能分析功能。提出问题，即可获得可视化答案。  

## 快速入门  

### 激活Sentry模式  
```bash
sentry-mode activate --query "Is anyone in the room?"
```  

**输出：**  
```
📹 Sentry Mode Activated
🎥 Recording video (3 seconds)...
🔍 Extracting frames (ffmpeg)...
🤖 Analyzing with vision AI...

📊 REPORT:
Query: Is anyone in the room?
Status: ✅ Yes
Details: One person visible at desk, facing monitor
Confidence: High
Timestamp: 2026-01-27 11:15:00 MST
```  

### 支持的查询类型  

**人员检测：**  
- “房间里有人吗？”  
- “能看到多少人？”  
- “我的人在画面里吗？”  

**物体检测：**  
- “我的桌子上有什么？”  
- “有打开的窗户或门吗？”  
- “房间的状态如何？”  

**运动检测：**  
- “检测到任何移动吗？”  
- “自上次检查以来有什么变化吗？”  
- “画面中有任何活动吗？”  

**文本识别：**  
- “读取所有可见的文本”  
- “屏幕上显示的是什么？”  
- “有可辨认的文字吗？”  

**总体状态：**  
- “拍摄一张截图并描述现场情况”  
- “你看到了什么？”  
- “分析当前的画面”  

## 工作原理  

### 第一步：捕获视频  
- 通过ffmpeg或系统工具访问网络摄像头  
- 录制3-5秒的视频  
- 保存到临时文件  

### 第二步：提取关键帧  
- 使用ffmpeg从视频中提取3-5帧关键帧  
- 将帧转换为图像  
- 选择最相关的帧  

### 第三步：使用视觉AI进行分析  
- 将帧发送到Claude视觉模型  
- 在查询中包含你的需求  
- 获取详细分析结果  

### 第四步：报告分析结果  
- 总结分析结果  
- 显示置信度  
- 提供时间戳  
- 如有需要，建议相应的操作  

## 示例  

### 示例1：检查房间是否有人  
```bash
sentry-mode activate --query "Is anyone in the room?"
```  
**响应：**  
```
✅ YES - One person visible
- Person at desk, facing left
- Seated position
- No visible movement
- Confidence: High
```  

### 示例2：监控桌面  
```bash
sentry-mode activate --query "What's on my desk and is it organized?"
```  
**响应：**  
```
📊 DESK STATUS:
Items visible:
- Laptop (open, screen active)
- Coffee cup (left side)
- Papers (scattered)
- Keyboard and mouse (centered)
- Phone (right side)

Organization: Fair
Notes: Some papers could be filed
Confidence: High
```  

### 示例3：检测运动  
```bash
sentry-mode activate --query "Any movement or activity?"
```  
**响应：**  
```
🎬 MOTION ANALYSIS:
Primary frames: 5 extracted
Movement detected: Yes
Type: Person typing/working
Duration: Continuous across frames
Intensity: Light (sitting activity)
Confidence: High
```  

## 配置设置  

### 默认设置  
- **录制时长：** 3秒  
- **提取帧数：** 5帧  
- **格式：** JPEG图像  
- **分析工具：** Claude视觉AI（最新版本）  
- **置信度阈值：** 中等以上  

### 可调整的选项  
```bash
sentry-mode activate \
  --query "Is anyone in the room?" \
  --duration 5 \  # seconds
  --frames 8 \    # number to extract
  --confidence high  # high/medium/low
```  

## 技术细节  

### 依赖库/工具  
- ffmpeg（用于视频捕获和帧提取）  
- Claude视觉API（用于分析）  
- Node.js或类似技术（用于任务协调）  

### 支持的摄像头类型  
- 内置网络摄像头（默认）  
- USB摄像头  
- 可本地访问的IP摄像头  

### 输出格式  
- **文本报告**（默认）  
- **JSON格式**（使用`--format json`选项）  
- **详细分析报告**（使用`--verbose`选项）  

### 隐私与数据存储  
- 视频在提取后立即删除  
- 分析完成后，相关帧也会被删除  
- 默认情况下不进行持久化存储  
- 分析结果仅保存在对话记录中  

## 使用场景  

**工作空间监控：**  
- 确认自己是否在办公桌前  
- 检查桌面整理情况  
- 监控是否有干扰  

**安全检查：**  
- 确认房间是否无人  
- 检查门窗状态  
- 检测未经授权的进入  

**活动记录：**  
- 跟踪工作流程  
- 监控房间内的活动  
- 用于考勤记录  

**视觉辅助任务：**  
- 从屏幕上读取文字  
- 确认物体的位置  
- 检查视觉环境  

**远程管理：**  
- 监控远程工作空间  
- 检查设备状态  
- 验证安装或设置是否正确  

## 限制因素  

- **光照条件：** 在良好光照环境下效果最佳  
- **视角范围：** 受限于网络摄像头的安装位置  
- **隐私问题：** 会捕捉到视野内的所有内容（请谨慎使用）  
- **细节识别：** 无法识别具体人员  
- **深度信息：** 仅提供2D分析结果  

## 安全与隐私注意事项  

⚠️ **重要提示：**  
- 该功能会录制您工作空间的视频  
- 在共享空间使用时，请确保遵守隐私规定  
- 需要获得画面中人员的同意  
- 数据通过Claude API进行处理（遵循Anthropic的隐私政策）  
- 默认情况下不进行本地数据存储  

## 常见问题及解决方法  

### 摄像头无法启动  
- 检查系统权限（macOS可能需要摄像头访问权限）  
- 确认没有其他应用程序正在使用该摄像头  
- 可尝试明确指定摄像头：`--camera 0`  

### 帧质量较低  
- 改善照明条件  
- 将设备移近摄像头  
- 增加提取的帧数  
- 清洁摄像头镜头  

### 分析结果过于模糊  
- 请更具体地描述查询内容  
- 尝试多次提问  
- 使用`--verbose`选项获取更详细的分析结果  
- 明确指出需要分析的重点  

## 相关脚本  
- **sentry-mode.js**：主要协调脚本（负责视频捕获、帧提取、分析及结果报告）  
- **webcam-capture.js**：用于视频捕获的ffmpeg封装脚本  
- **frame-extractor.js**：用于提取关键帧的脚本  
- **vision-analyzer.js**：负责将帧发送至Claude模型并解析分析结果的脚本  

## 参考文档  
- **SETUP.md**：摄像头权限及设备配置指南  
- **EXAMPLES.md**：实际使用场景示例  
- **BOLO.md**：持续监控模式（包含监控列表功能）