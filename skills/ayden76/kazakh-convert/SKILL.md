---
name: kazakh-convert
version: 1.0.0
license: MIT
description: 这是一个用于转换哈萨克语文本（从西里尔字母到阿拉伯字母，或从阿拉伯字母到西里尔字母）的工具。该工具支持哈萨克语的双向转换，并能够正确处理包含特殊字符（如 ә, і, ү, ө, ң, ғ, ұ, қ, һ）的文本。
homepage: https://github.com/ayden-omega/kazakh-convert
metadata: {
  "clawdbot": {
    "emoji": "🇰🇿",
    "requires": {"bins": ["python3"]},
    "tags": ["kazakh", "language", "converter", "cyrillic", "arabic", "translation"]
  },
  "license": "MIT",
  "acceptLicenseTerms": true
}
---
# Kazakh Convert - 卡扎克语文本转换器

这是一个支持卡扎克语双向文本转换的工具，能够在这两种文字编码（西里尔字母和阿拉伯字母）之间进行转换。

## 主要功能

- ✅ 双向转换（西里尔字母 ↔ 阿拉伯字母）
- ✅ 完全支持卡扎克语的特殊字符
- ✅ 处理多行文本
- ✅ 自动修正语法错误
- ✅ 兼容 Windows PowerShell

## 使用方法

### 将西里尔字母转换为阿拉伯字母
```bash
python kazConvert.py A "сәлем"
# Output: سالەم
```

### 将阿拉伯字母转换为西里尔字母
```bash
python kazConvert.py C "قالايسىز؟"
# Output: қалайсыз？
```

## 参数说明

| 参数 | 说明 |
|-----------|-------------|
| `A` | 将文本转换为阿拉伯字母编码 |
| `C` | 将文本转换为西里尔字母编码 |
| `text` | 需要转换的卡扎克语文本（请用引号括起来） |

## 使用示例

### 示例 1：问候语
```bash
python kazConvert.py A "Қалың қалай?"
# Output: قالىڭ قالاي؟
```

### 示例 2：自我介绍
```bash
python kazConvert.py C "مەنىڭ اتىم ومەگا"
# Output: Менің атым Омега
```

### 示例 3：多行文本
```bash
python kazConvert.py A "Сәлем! Мен қазақпын. Алматыдан келдім."
```

## Windows PowerShell 使用技巧

### 注意事项

- 该工具支持所有卡扎克语特有的字母：
  - **西里尔字母：** ә, і, ү, ө, ң, ғ, ұ, қ, һ
  - **阿拉伯字母：** ە, ى, ۇ, و, ڭ, ع, ۇ, ق, ھ

## 技术细节

- **字符映射：** 完整的卡扎克语字母表映射表
- **语法修正：** 自动处理特殊字符组合（如 ё→yо 等）
- **多行支持：** 可批量转换多行文本

## 相关文件

- 脚本文件：`kazConvert.py`
- 技能文档：`SKILL.md`

## 相关技能

- `kazakh-image-gen`：用于生成卡扎克语传统图案的 AI 工具
- `edge-tts`：卡扎克语文本转语音的软件
- `whisper-asr`：卡扎克语语音识别系统

---

*作者：ayden-omega-agent*
*版本：1.0.0*
*许可证：MIT*