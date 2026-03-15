---
name: HashGen
description: "哈希生成器和文件完整性验证工具。可为文本和文件生成 MD5、SHA1、SHA256、SHA512 哈希值，验证文件的完整性是否与预期的哈希值一致，通过哈希值比较两个文件，并能同时查看所有可用的哈希算法。这是一个非常重要的安全与验证工具。"
version: "1.0.0"
author: "BytesAgain"
tags: ["hash","md5","sha256","checksum","security","verify","integrity","crypto"]
categories: ["Security", "Developer Tools", "Utility"]
---
# HashGen

这是一个用于对任何内容进行哈希处理并验证其完整性的工具包。

## 命令

- `text [algo] <text>` — 对文本字符串进行哈希处理（默认使用 sha256 算法）
- `file [algo] <file>` — 对文件进行哈希处理
- `verify <file> <expected_hash> [algo]` — 根据预期的哈希值验证文件
- `compare <file1> <file2> [algo]` — 通过哈希值比较两个文件
- `all <text>` — 显示该文本支持的所有哈希算法
- `help` — 显示所有可用的命令

## 使用示例

```bash
hashgen text sha256 "hello world"
hashgen file sha256 download.iso
hashgen verify package.tar.gz abc123def456
hashgen compare file1.txt file2.txt
hashgen all "my secret"
```

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com

## 提示

- 使用 `hashgen help` 可以查看所有可用的命令。