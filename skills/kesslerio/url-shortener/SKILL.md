---
name: shorten
description: 使用 is.gd 来缩短 URL（无需身份验证）。该服务会返回一个永久有效的短链接。
---

# 简短化网址

使用 [is.gd](https://is.gd) 服务可以快速缩短网址。无需 API 密钥或账户。

## 使用方法

```bash
shorten "https://example.com/very/long/url"
```

## 示例

**标准用法：**
```bash
shorten "https://google.com"
# Output: https://is.gd/O5d2Xq
```

## 注意事项：
- 短缩后的链接是永久有效的。
- 该服务不提供任何分析功能（仅执行简单的重定向）。
- 服务存在速率限制，请合理使用。