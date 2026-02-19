---
name: authy
description: "通过环境变量将敏感信息注入到子进程中。你永远不会直接看到这些敏感值——authy 会负责直接处理它们的注入过程。适用于任何需要 API 密钥、凭据或令牌的命令。"
license: MIT
compatibility: Requires `authy` on PATH. Auth via AUTHY_TOKEN (run-only) + AUTHY_KEYFILE.
metadata:
  author: eric8810
  version: "0.3.0"
  homepage: https://github.com/eric8810/authy
  openclaw:
    requires:
      bins: ["authy"]
      env: ["AUTHY_KEYFILE", "AUTHY_TOKEN"]
      files: ["$AUTHY_KEYFILE"]
---
# Authy — 安全的秘密值注入机制

将秘密值以环境变量的形式注入到子进程中。你永远不会直接看到、处理或记录这些秘密值。

## 工作原理

你的令牌（token）仅用于执行操作（即“运行”命令）。你可以使用 `authy list` 命令来查看秘密值的名称，然后使用 `authy run` 命令将这些名称注入到子进程中。你永远不会直接看到这些秘密值的具体内容。

## 将秘密值注入到命令中

```bash
authy run --scope <policy> --uppercase --replace-dash '_' -- <command> [args...]
```

`--uppercase --replace-dash_'` 这两个参数会将像 `db-host` 这样的秘密值名称转换为 `DB_HOST` 这样的环境变量名称。

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

输出结果：`{"secrets":[{"name":"db-host","version":1,...}]`

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
| 2 | 认证失败 — 请检查 AUTHY_TOKEN 或 AUTHY_KEYFILE 文件 |
| 3 | 未找到相应的秘密值或策略 |
| 4 | 访问被拒绝或存在运行权限限制 |
| 6 | 令牌无效、已过期或已被撤销 |

## 规则

1. **仅使用 `authy run` 和 `authy list` 命令** — 这是你可以使用的唯一命令。
2. **切勿将凭证硬编码到代码中** — 应通过环境变量来传递凭证，并通过 `authy run` 来执行命令。
3. **切勿在子进程脚本中输出或记录环境变量的内容** — 秘密值仅存在于内存中。
4. **切勿将环境变量内容写入文件** — 不要将 `$SECRET` 变量写入磁盘。
5. **使用 `--scope` 参数** 来限制对所需秘密值的访问范围。