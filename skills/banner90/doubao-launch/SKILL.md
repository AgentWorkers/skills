---
 name: doubao-launch
 description: Launch Doubao desktop application and configure real-time translation window.
 tools:
   - launch_doubao
---
# Doubao 启动

## 使用方法

```bash
python scripts/doubao_auto_workflow.py [--dual|--single] --json-output
```

## 参数

- `mode`（可选）：`dual` 或 `single`，默认值为 `dual`

## 返回值

```json
{
  "success": true,
  "window_handle": 123456,
  "window_title": "Doubao - Real-time Subtitles",
  "mode": "dual"
}
```

## 工具

## launch_doubao

用于启动 Doubao 应用程序


## 工作流程集成

此技能是 YouTube 翻译工作流程的一部分：
1. **youtube-audio-download**：从 YouTube 下载音频文件
2. **doubao-launch**：启动 Doubao 翻译窗口
3. **audio-play**：播放下载的音频文件
4. **doubao-capture**：捕获翻译后的字幕

## 执行方式

所有技能均通过 WSL（Windows Subsystem for Linux）在 Windows 上使用 Python 进行跨平台调用：
```
wsl -> python.exe scripts/doubao_auto_workflow.py ...
```

## 错误处理

所有技能都会返回一个 JSON 对象，其中包含 `success` 字段：
- `success: true`：操作已完成
- `success: false`：请查看 `error_code` 和 `error_message` 以获取错误信息

## 注意事项

- Windows 图形界面自动化需要桌面可见（不允许使用 RDP 断开连接）
- 输出文件存储在 Windows 的 `works/` 目录中
- WSL 通过 `/mnt/h/...` 访问 Windows 文件系统