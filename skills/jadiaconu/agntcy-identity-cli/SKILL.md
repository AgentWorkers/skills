---
description: AGNTCY Identity Issuer CLI（命令行工具）和Node Backend（节点后端）用于管理可验证的代理身份、元数据以及徽章（badges）。
  verifiable agent identities, metadata, and badges.
homepage: "https://github.com/agntcy/identity"
metadata:
  openclaw:
    emoji: 🪪
    install:
      - id: go
        kind: go
        label: Install via go install
        module: github.com/agntcy/identity/cmd/issuer
    requires:
      anyBins:
        - identity

      # Required/optional environment variables used by examples and typical IdP-backed issuer flows
      env:
        # Base URL of the AGNTCY Identity issuer / node backend (e.g., http://localhost:9090)
        - ISSUER_URL
        # OAuth/OIDC client ID for the configured Identity Provider (IdP) (only needed for IdP-backed issuer flows)
        - CLIENT_ID
        # OAuth/OIDC client secret for the configured Identity Provider (IdP) (only needed for IdP-backed issuer flows)
        - CLIENT_SECRET

      # Local configuration paths this skill instructs users to create/read.
      # The vault may contain private keys and MUST be treated as sensitive.
      config:
        - skills.entries.agntcy-identity.config.vaultPath
name: agntcy-identity
---
# AGNTCY 身份管理（Issuer CLI + 节点后端）

使用 `identity` CLI 在 AGNTCY 生态系统中创建、管理、颁发和验证去中心化的代理身份及徽章。

该工具支持以下功能：
- 身份创建（代理、MCP 服务器、MAS）
- 基于 BYOID 的身份验证（例如，基于 Okta 的身份）
- 元数据生成
- 徽章颁发与发布
- 可验证凭证（VC）的验证

---

## 系统要求

- Docker Desktop 或者：
  - Docker Engine v27+
  - Docker Compose v2.35+
- （演示用途可选）：
  - Okta CLI
  - Ollama CLI

---

## 核心命令

### 密钥库管理

管理加密密钥库和签名密钥：

```bash
identity vault connect file -f \~/.identity/vault.json -v "My Vault"
identity vault key generate
```

---

### 发行者管理

注册和管理发行者配置：

```bash
identity issuer register -o "My Organization" -c "$CLIENT_ID" -s "$CLIENT_SECRET" -u "\$ISSUER_URL"
```

---

### 元数据管理

生成和管理身份元数据：

```bash
identity metadata generate -c "$CLIENT_ID" -s "$CLIENT_SECRET" -u "\$ISSUER_URL"
```

---

### 徽章颁发

颁发并发布徽章（可验证凭证）：

```bash
identity badge issue mcp -u <http://localhost:9090> -n "My MCP Server"
identity badge publish
```

---

### 验证

验证已发布的徽章：

```bash
identity verify -f vcs.json
```

---

## 运行节点后端

使用 Docker 在本地运行：

```bash
git clone <https://github.com/agntcy/identity.git> cd identity
./deployments/scripts/identity/launch_node.sh
```

或者：

```bash
make start_node
```

---

## 典型工作流程

1. 安装 CLI
2. 启动节点后端
3. 创建密钥库及密钥
4. 注册发行者
5. 生成元数据
6. 颁发徽章
7. 发布徽章
8. 验证徽章

## 安全注意事项（在提供敏感信息前请阅读）

- 文件 `~/.identity/vault.json` 包含签名密钥信息，应被视为**高价值秘密**。请使用专门的测试密钥库进行测试，切勿在生产环境中重复使用这些密钥。
- `CLIENT_SECRET` 是**高价值秘密**。只有在您仔细审查了将要运行的代码/二进制文件，并且确保处于受控环境中时，才可提供该密钥。
- 避免将敏感信息粘贴到聊天记录、日志、工单或问题跟踪系统中。建议使用安全的密钥注入机制。

---

## 其他说明

- CLI 的二进制文件名为 `identity`。
- 公共发行者密钥可通过以下路径访问：`/v1alpha1/issuer/{common_name}/.well-known/jwks.json`
- 已发布的可验证凭证（VC）可通过以下路径访问：`/v1alpha1/vc/{metadata_id}/.well-known/vcs.json`
- 该工具支持代理（Agents）、MCP 服务器（MCP Servers）和 MAS（MASs）。
- 遵循去中心化身份管理标准（例如 W3C DIDs）。