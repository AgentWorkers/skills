---
name: broken-link-checker
description: 验证外部 URL（http/https）的可用性（状态码为 200-399）。
---
# 断裂链接检测器

用于验证外部URL是否可用。适用于检查文档链接或外部引用。

## 使用方法

```bash
node skills/broken-link-checker/index.js <url1> [url2...]
```

## 输出结果

结果以JSON数组的形式返回：
```json
[
  {
    "url": "https://example.com",
    "valid": true,
    "status": 200
  },
  {
    "url": "https://example.com/broken",
    "valid": false,
    "status": 404
  }
]
```