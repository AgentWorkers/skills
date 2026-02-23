---
name: apple-notes-updater
description: 使用 `osascript` 按笔记名称更新 Apple Notes 的内容。此功能支持非交互式的笔记内容更新，同时保留格式并支持 HTML 格式。
---
# Apple Notes 更新器

此技能提供了一种强大且非交互式的功能，用于根据笔记的标题来更新其内容。它使用 `osascript` 直接与 Apple Notes 应用程序进行交互。

## 使用方法

该技能的主要功能是更新笔记的正文内容。

### 根据标题更新笔记

要更新笔记，您需要提供笔记的精确标题以及新的内容（新内容可以包含用于富文本格式化的 HTML 标签）。该技能通过临时文件来安全地传输内容，从而规避了命令行参数的限制。

**示例脚本用法：**
```bash
./skills/apple-notes-updater/update_note.sh "My Note Title" "<h1>New Content</h1><p>With <b>HTML</b> formatting.</p>"
```

**底层的 AppleScript 逻辑：**
```applescript
set noteTitle to "My Note Title"
set newBodyFilePath to (POSIX file "/path/to/temp/file.html") as alias -- Path to a temporary file containing HTML content

tell application "Notes"
    set theNote to first note whose name is noteTitle
    
    set fileRef to open for access newBodyFilePath
    set theContent to read fileRef as «class utf8»
    close access fileRef
    
    set body of theNote to theContent
end tell
```

## 实现细节**

- 使用 `osascript` 直接控制 Apple Notes 应用程序。
- 内容（包括 HTML）通过临时文件传递，以确保正确的转义和格式化。
- 支持在 `newBody` 中使用 HTML 进行富文本格式化。
- 需要 Apple Notes.app 正在运行且可访问。
- 仅适用于 macOS 系统。