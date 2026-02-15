---
description: 使用 `translate-shell` 在不同语言之间翻译文本——无需 API 密钥。
---

# 文本翻译器

使用免费且无需API密钥的方法在语言之间进行文本翻译。

## 必备工具

- `translate-shell`（`trans`）：安装命令：`sudo apt-get install translate-shell`

## 使用说明

### 基本翻译
```bash
# Translate with explicit source/target
trans -b en:ja "Hello, how are you?"

# Auto-detect source language
trans -b :en "こんにちは"

# Detailed output with alternatives and pronunciation
trans en:de "Good morning"

# Translate a file
trans -b en:fr -i input.txt -o output.txt
```

### 常见语言代码
`en`：英语  
`ja`：日语  
`zh`：中文  
`ko`：韩语  
`fr`：法语  
`de`：德语  
`es`：西班牙语  
`pt`：葡萄牙语  
`it`：意大利语  
`ru`：俄语  
`ar`：阿拉伯语  
`hi`：印地语  
`th`：泰语  
`vi`：越南语

### 批量翻译
```bash
# Translate multiple lines (one per line)
while IFS= read -r line; do
  trans -b :en "$line"
  sleep 0.5  # Rate limit courtesy
done < input.txt
```

### 输出格式
```
**Translation** (en → ja):
| Original | Translation |
|----------|-------------|
| Hello | こんにちは |
| Thank you | ありがとうございます |

*Powered by Google Translate via translate-shell*
```

## 特殊情况

- **`trans`未安装**：使用`which trans`检查是否已安装。根据用户的操作系统提供相应的安装命令。
- **请求限制**：Google Translate在接收大量请求后可能会限制访问速度。建议在批量翻译请求之间添加`sleep 0.5`（等待0.5秒）的延迟。
- **长文本**：将长文本分割成多个段落，以提高翻译质量并避免超时。
- **不支持的语言**：使用`trans -R`可以查看所有支持的语言，并选择最接近的目标语言进行翻译。
- **特殊字符**：需要将输入字符串用引号括起来，以防shell程序误解其内容。
- **离线使用**：`trans`需要互联网连接，不支持离线翻译功能。

## 安全性

- 翻译过程会将文本发送到Google Translate服务器，请**切勿翻译敏感数据**（如密码、API密钥或私人文件）。
- 如果输入文本中包含凭证或个人身份信息（PII），系统会向用户发出警告。

## 注意事项

- `translate-shell`是推荐的使用方法，它在大多数Linux发行版中都已被稳定集成。
- Google Translate的API接口可能随时发生变化（无官方通知），因此建议优先使用`translate-shell`。