---
name: addis-assistant
description: 通过 Addis Assistant API (api.addisassistant.com) 提供语音转文本（STT）和文本翻译功能。当用户需要将音频文件转换为文本（尤其是阿姆哈拉语），或在不同语言之间进行文本翻译（例如从阿姆哈拉语翻译成英语）时，可以使用该服务。使用该服务需要 'x-api-key' 这个访问密钥。
---

# Addis Assistant

## 概述

该技能支持使用 Addis Assistant API 进行语音转文本（STT）和文本翻译操作。

## 使用方法

该技能提供两个主要功能：

1. **语音转文本（STT）：** 将音频文件（例如阿姆哈拉语）转换为文本。
2. **翻译：** 将文本从源语言翻译成目标语言。

### 认证

这两个功能都需要一个 `x-api-key`。该密钥应作为参数传递给相应的脚本。

### 语音转文本（STT）功能

- **端点：** `api.addisassistant.com/api/v2/stt`
- **方法：** `POST`
- **参数：**
    - `audio`：音频文件的路径（例如：`"@/path/to/file"`）
    - `request_data`：包含 `"language_code": "am"` 的 JSON 字符串（目前仅支持阿姆哈拉语）。

### 翻译功能

- **端点：** `api.addisassistant.com/api/v1/translate`
- **方法：** `POST`
- **参数：**
    - `text`：需要翻译的文本。
    - `source_language`：输入文本的语言（例如：`"am"`）。
    - `target_language`：目标语言（例如：`"en"`）。

## 资源

该技能包含用于直接执行的 `scripts/` 文件和 API 详细信息的 `references/` 文件。

### scripts/

- `stt.py`：用于语音转文本的 Python 脚本。
- `translate.py`：用于文本翻译的 Python 脚本。

### references/

- `api_spec.md`：详细的 API 规范和 curl 示例。