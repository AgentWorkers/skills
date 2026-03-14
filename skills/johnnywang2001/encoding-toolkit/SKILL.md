---
name: encoding-toolkit
description: 多格式编码器、解码器和哈希工具，支持 Base64、Base64URL、Base32、十六进制（Hex）、URL 编码、HTML 实体编码、ROT13 编码、二进制（Binary）以及 ASCII85 编码。同时能够计算 MD5、SHA-1、SHA-256、SHA-512 和 SHA3-256 哈希值。该工具可自动检测数据的编码格式，适用于数据编码/解码、文件或字符串哈希值的计算、不同格式之间的转换，以及识别未知编码的字符串。支持的操作包括：`encode base64`（将数据编码为 Base64 格式）、`decode hex`（将十六进制数据解码为字符串）、`hash sha256`（计算数据的 SHA-256 哈希值）、`what encoding is this`（判断数据的编码格式）、`url encode`（将字符串编码为 URL 格式）、`html decode`（将 HTML 实体解码为普通文本）、`convert to binary`（将数据转换为二进制格式）。
---
# 编码工具包

这是一个集编码、解码和哈希功能于一体的工具。支持9种编码格式和5种哈希算法，并具备自动检测编码格式的功能。

## 快速入门

```bash
# Encode
python3 scripts/encode_decode.py encode base64 "Hello World"
python3 scripts/encode_decode.py encode url "hello world & goodbye"
python3 scripts/encode_decode.py encode hex "Hello"

# Decode
python3 scripts/encode_decode.py decode base64 "SGVsbG8gV29ybGQ="
python3 scripts/encode_decode.py decode hex "48656c6c6f"
python3 scripts/encode_decode.py decode url "hello%20world"

# Hash
python3 scripts/encode_decode.py hash sha256 "my secret"
python3 scripts/encode_decode.py hash md5 "test" --all  # show all algorithms

# Auto-detect encoding
python3 scripts/encode_decode.py detect "SGVsbG8gV29ybGQ="

# List all supported formats
python3 scripts/encode_decode.py list

# Read from stdin or file
echo "data" | python3 scripts/encode_decode.py encode base64 --stdin
python3 scripts/encode_decode.py hash sha256 --file secret.txt
```

## 支持的格式

**编码格式：** base64、base64url、base32、hex、url、html、rot13、binary、ascii85

**哈希算法：** md5、sha1、sha256、sha512、sha3-256

## 功能特点

- 一个工具即可完成编码、解码、哈希、检测及列表显示功能
- 具有自动检测未知编码字符串的能力
- 所有操作均支持标准输入（stdin）和文件输入
- 无需依赖任何外部库——完全使用Python标准库实现