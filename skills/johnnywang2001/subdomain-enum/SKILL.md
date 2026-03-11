---
name: subdomain-enum
description: 使用 DNS 暴力破解方法和证书透明度日志（crt.sh）来枚举任意域名的子域名。当用户需要发现子域名、进行侦察、审计攻击面、查找被遗忘或暴露的服务，或映射域名的基础设施时，可以使用该工具。无需 API 密钥。支持自定义单词列表、多线程操作以及 JSON 格式的输出结果。
---
# 子域名枚举器

使用两种互补的技术来发现任何域名的子域名：DNS暴力解析和通过 `crt.sh` 进行的证书透明度日志挖掘。

## 快速入门

```bash
python3 scripts/subenum.py example.com
```

## 命令

```bash
# Basic enumeration (built-in wordlist + crt.sh)
python3 scripts/subenum.py example.com

# Custom wordlist
python3 scripts/subenum.py example.com --wordlist /path/to/wordlist.txt

# Faster with more threads
python3 scripts/subenum.py example.com --threads 20

# DNS only (skip crt.sh)
python3 scripts/subenum.py example.com --no-crtsh

# JSON output
python3 scripts/subenum.py example.com --json

# Save results to file
python3 scripts/subenum.py example.com --output subdomains.txt

# Verbose progress
python3 scripts/subenum.py example.com -v
```

## 选项

| 标志 | 默认值 | 描述 |
|------|---------|-------------|
| `--wordlist, -w` | 内置（约120个单词） | 自定义单词列表文件 |
| `--threads, -t` | `10` | 并行DNS解析线程数 |
| `--timeout` | `15` | `crt.sh` 查询的HTTP超时时间 |
| `--no-crtsh` | 关闭 | 跳过证书透明度查询 |
| `--json` | 关闭 | 以JSON格式输出 |
| `--output, -o` | — | 将结果写入文件 |
| `--verbose, -v` | 关闭 | 扫描过程中显示进度 |

## 技术原理

1. **DNS暴力解析** — 对单词列表中的每个单词，使用DNS解析 `{word}.{domain}`，返回活跃子域名的IP地址。
2. **证书透明度（crt.sh）** — 查询公共CT日志中颁发给 `*.domain` 的证书，从而发现那些可能不响应DNS但拥有TLS证书的子域名。

## 依赖项

```bash
pip install requests
```

## 注意事项

- 内置的单词列表涵盖了常见的子域名（如 www、api、mail、staging 等）。
- 如需进行全面扫描，请使用更大的单词列表（例如 SecLists DNS 单词列表）。
- 结果会从多个来源中去重。
- 请谨慎使用该工具——仅扫描您拥有权限或被允许测试的域名。