---
name: dns-lookup
description: "使用 `bind-utils` 中的 `dig` 命令将主机名解析为 IP 地址。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "bins": ["dig"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "bind-utils",
              "bins": ["dig"],
              "label": "Install bind-utils (dnf)",
            },
          ],
      },
  }
---

# DNS查询技巧

使用`dig`命令将主机名解析为IP地址。该功能由`bind-utils`包提供。

## 基本查询

解析主机名的A记录：

```bash
dig example.com A +short
```

## IPv6查询

解析AAAA记录：

```bash
dig example.com AAAA +short
```

## 完整DNS记录

获取包含权威信息及其他部分的完整DNS响应：

```bash
dig example.com ANY
```

## 反向查询

根据IP地址查找对应的主机名：

```bash
dig -x 93.184.216.34 +short
```

## 安装

```bash
sudo dnf install bind-utils
```