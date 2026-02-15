# 媒体转换技能

## 描述
该技能通过检测媒体文件的魔数（magic bytes）来识别文件类型，并修正文件扩展名，以确保与 Gemini 的兼容性（Gemini 不支持 `application/octet-stream` 格式的文件）。同时，该技能实现了基本的文件转换逻辑（未来将支持 ffmpeg 的功能）。

## 使用方法
```bash
# Detect MIME type and return JSON
node skills/media-converter/index.js detect --file <path>

# Fix extension based on detected MIME (renames file if needed)
node skills/media-converter/index.js fix --file <path>
```

## 示例
```bash
# Check a file masked as .bin
node skills/media-converter/index.js detect --file /tmp/unknown.bin
# Output: {"mime": "image/gif", "ext": "gif"}

# Rename a file to match its content
node skills/media-converter/index.js fix --file /tmp/unknown.bin
# Output: {"original": "/tmp/unknown.bin", "fixed": "/tmp/unknown.gif", "mime": "image/gif"}
```