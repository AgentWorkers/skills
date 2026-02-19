---
name: authy
description: "通过环境变量将密钥值注入到子进程中。你永远不会直接看到这些密钥值，因为 `authy` 会负责自动执行注入操作。适用于任何需要 API 密钥、凭据或令牌的命令。"
license: MIT
compatibility: Requires `authy` on PATH. Auth via AUTHY_TOKEN (run-only) + AUTHY_KEYFILE.
metadata:
  author: eric8810
  version: "0.2.0"
  homepage: https://github.com/eric8810/authy
  openclaw:
    requires:
      bins: ["authy"]
      env: ["AUTHY_KEYFILE", "AUTHY_TOKEN"]
      files: ["$AUTHY_KEYFILE"]
---
# Authy — 安全的秘密值注入机制

将秘密值以环境变量的形式注入到子进程中。你永远不会看到、处理或记录这些秘密值。

## 工作原理

你的令牌仅用于执行操作（即“运行”子进程）。你可以使用 `authy list` 命令来查看秘密值的名称，然后使用 `authy run` 命令将这些名称注入到子进程中。你永远不会直接看到这些秘密值本身。

## 将秘密值注入到命令中

```bash
authy run --scope <policy> --uppercase --replace-dash '_' -- <command> [args...]
```

`--uppercase` 和 `--replace-dash_'` 标志会将像 `db-host` 这样的秘密值名称转换为 `DB_HOST` 这样的环境变量名称。

示例：
```bash
authy run --scope deploy --uppercase --replace-dash '_' -- ./deploy.sh
authy run --scope backend --uppercase --replace-dash '_' -- node server.js
authy run --scope testing --uppercase --replace-dash '_' -- pytest
```

## 查看秘密值名称

```bash
authy list --scope <policy> --json
```

输出：`{"secrets":[{"name":"db-host","version":1,...}]`

## 编写使用秘密值的脚本

编写代码来读取环境变量，然后使用 `authy run` 命令来执行这些代码：

```bash
cat > task.sh << 'EOF'
#!/bin/bash
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/data
EOF
chmod +x task.sh
authy run --scope my-scope --uppercase --replace-dash '_' -- ./task.sh
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 操作成功 |
| 2 | 认证失败 — 请检查 AUTHY_TOKEN 或 AUTHY_KEYFILE |
| 3 | 未找到相应的秘密值或策略 |
| 4 | 访问被拒绝或存在运行限制 |
| 6 | 令牌无效、已过期或已被撤销 |

## 规则

1. **仅使用 `authy run` 和 `authy list` 命令** — 这些是你能使用的唯一命令。
2. **切勿将凭证硬编码到代码中** — 应通过环境变量来传递凭证，并使用 `authy run` 来执行操作。
3. **切勿在子进程脚本中输出或记录环境变量** — 秘密值仅存在于内存中。
4. **切勿将环境变量写入文件** — 不要将 `$SECRET` 这样的变量值保存到磁盘上。
5. **使用 `--scope` 标志** 来限制对所需秘密值的访问范围。