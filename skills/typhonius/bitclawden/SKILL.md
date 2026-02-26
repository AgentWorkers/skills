---
name: bitclawden
description: 通过 `bw CLI` 在 Bitwarden 密码库中查询、创建和编辑凭证。当需要存储、检索、查找或管理密码、密钥或凭证时，请使用该工具。
homepage: https://bitwarden.com/help/cli/
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["bw", "jq"], "env": ["BW_SESSION"] },
        "primaryEnv": "BW_SESSION",
        "install":
          [
            {
              "id": "bw-binary",
              "kind": "script",
              "script": "PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]'); [ \"$PLATFORM\" = 'darwin' ] && PLATFORM='macos'; curl -sL \"https://vault.bitwarden.com/download/?app=cli&platform=${PLATFORM}\" -o /tmp/bw.zip && unzip -o /tmp/bw.zip -d ~/.local/bin/ && chmod +x ~/.local/bin/bw && rm /tmp/bw.zip",
              "bins": ["bw"],
              "requires": ["curl", "unzip"],
              "label": "Install Bitwarden CLI to ~/.local/bin",
            },
          ],
      },
  }
---
# Bitwarden CLI

用于管理 Bitwarden 保管库中的凭证。请遵循官方的 CLI 文档，切勿随意猜测命令的使用方法。

## 工作流程

1. 验证 CLI 是否可用：`bw --version`。
2. 检查保管库的状态：`bw status`。
3. 如果保管库被锁定，提示用户运行 `bw unlock` 并设置 `BW_SESSION`。
4. 在执行任何保管库操作之前，必须确保 `bw status` 显示为 “unlocked”（未锁定）状态。
5. 创建或编辑凭证后，运行 `bw sync` 以同步数据。

## 查找凭证

```bash
bw list items --search "query"
bw get item "name"
bw get password "name"
bw get username "name"
bw get totp "name"
bw list items --folderid <folder-id>
bw list folders
```

## 创建凭证

```bash
# Login item (type 1=Login, 2=Secure Note, 3=Card, 4=Identity)
echo '{"type":1,"name":"Example","login":{"username":"user@example.com","password":"s3cret","uris":[{"uri":"https://example.com"}]}}' | bw encode | bw create item

# Folder
bw create folder "$(echo '{"name":"Work"}' | bw encode)"
```

## 编辑凭证

```bash
bw get item <id> | jq '.login.password = "newpass"' | bw encode | bw edit item <id>
bw get item <id> | jq '.folderId = "<folder-id>"' | bw encode | bw edit item <id>
```

## 生成新密码

```bash
bw generate -ulns --length 24
bw generate --passphrase --words 4 --separator "-"
```

## 安全准则

- 绝不要将凭证信息粘贴到日志、聊天记录或代码中。
- 建议仅显示用户名和网站名称；只有在用户明确要求时才透露密码。
- 除非用户提供密码，否则始终使用 `bw generate` 命令生成强密码。
- 如果命令返回 “Vault is locked”（保管库被锁定）的提示，请立即停止操作并让用户先解锁保管库。