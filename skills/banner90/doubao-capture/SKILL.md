---
 name: doubao-capture
 description: Capture Doubao translation results with auto-scroll and auto-end detection.
 tools:
   - capture_translation
---
# Doubao 字幕捕获

## 使用方法

```bash
python scripts/capture_doubao_scroll_v2.py --hwnd <window_handle> --output-dir <dir> --stop-auto --json-output
```

## 参数

- `window_handle`（必填）：来自 `doubao-launch` 的 HWND（窗口句柄）
- `output_dir`（可选）：输出目录，默认值：`works/translations`
- `stop_auto`（可选）：是否自动检测任务结束，默认值：`true`
- `no_new_threshold`（可选）：连续空读取次数的阈值，默认值：`5`

## 返回值

```json
{
  "success": true,
  "text_file_path": "H:/works/translations/doubao_20240307_143022.txt",
  "line_count": 156,
  "char_count": 3847,
  "stopped_by": "auto_detect"
}
```

## 工具

## capture_translation

用于从 Doubao 中捕获已翻译的字幕。

## 工作流程集成

该功能是 YouTube 翻译工作流程的一部分：
1. **youtube-audio-download**：从 YouTube 下载音频文件
2. **doubao-launch**：启动 Doubao 翻译窗口
3. **audio-play**：播放下载的音频文件
4. **doubao-capture**：捕获翻译后的字幕

## 执行方式

所有功能均通过 WSL（Windows Subsystem for Linux）在 Windows 系统上使用 Python 进行跨平台调用：

```
wsl -> python.exe scripts/capture_doubao_scroll_v2.py ...
```

## 错误处理

所有功能返回包含 `success` 字段的 JSON 数据：
- `success: true`：操作完成
- `success: false`：请查看 `error_code` 和 `error_message` 以获取错误信息

## 注意事项

- Windows 图形界面自动化需要桌面可见（禁止使用 RDP 连接）
- 输出文件存储在 Windows 系统的 `works/` 目录中
- WSL 通过 `/mnt/h/...` 路径访问 Windows 文件系统中的文件