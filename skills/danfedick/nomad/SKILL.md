---
name: nomad
version: 1.0.0
description: 查询 HashiCorp Nomad 集群的信息。可以列出作业（jobs）、节点（nodes）、资源分配情况（allocations）、评估结果（evaluations）以及所提供的服务（services）。这些操作仅限读取，主要用于监控和故障排查。
homepage: https://github.com/danfedick/nomad-skill
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["nomad"]}}}
---

# Nomad 技能

使用 `nomad` CLI 查询 HashiCorp Nomad 集群。支持仅用于监控和故障排查的读操作。

## 前提条件

- 已安装 `nomad` CLI
- 设置了 `NOMAD_ADDR` 环境变量（默认值为 http://127.0.0.1:4646）
- 如果启用了 ACL（访问控制列表），则需要 `NOMAD_TOKEN`

## 命令

### 作业（Jobs）

- 列出所有作业：
    ```bash
nomad job status
```

- 获取作业详情：
    ```bash
nomad job status <job-id>
```

- 作业历史记录：
    ```bash
nomad job history <job-id>
```

- 作业部署信息：
    ```bash
nomad job deployments <job-id>
```

### 分配（Allocations）

- 列出某个作业的分配信息：
    ```bash
nomad job allocs <job-id>
```

- 分配详情：
    ```bash
nomad alloc status <alloc-id>
```

- 分配日志（标准输出）：
    ```bash
nomad alloc logs <alloc-id>
```

- 分配日志（标准错误输出）：
    ```bash
nomad alloc logs -stderr <alloc-id>
```

- 跟踪分配日志：
    ```bash
nomad alloc logs -f <alloc-id>
```

### 节点（Nodes）

- 列出所有节点：
    ```bash
nomad node status
```

- 节点详情：
    ```bash
nomad node status <node-id>
```

- 节点分配信息：
    ```bash
nomad node status -allocs <node-id>
```

### 评估（Evaluations）

- 列出最近的评估结果：
    ```bash
nomad eval list
```

- 评估详情：
    ```bash
nomad eval status <eval-id>
```

### 服务（Services）

- 列出 Nomad 自带的服務发现功能：
    ```bash
nomad service list
```

- 服务信息：
    ```bash
nomad service info <service-name>
```

### 命名空间（Namespaces）

- 列出所有命名空间：
    ```bash
nomad namespace list
```

### 变量（Variables）

- 列出所有变量：
    ```bash
nomad var list
```

- 获取变量值：
    ```bash
nomad var get <path>
```

### 集群（Cluster）

- 集群成员信息：
    ```bash
nomad server members
```

- 代理信息：
    ```bash
nomad agent-info
```

## JSON 输出

- 在大多数命令后添加 `-json` 选项可获取 JSON 格式输出：
    ```bash
nomad job status -json
nomad node status -json
nomad alloc status -json <alloc-id>
```

## 过滤

- 使用 `-filter` 选项根据表达式进行过滤：
    ```bash
nomad job status -filter='Status == "running"'
nomad node status -filter='Status == "ready"'
```

## 常用操作模式

- **查找失败的分配（Find failed allocations）**
    ```bash
nomad job allocs <job-id> | grep -i failed
```

- **获取最新分配的日志（Get logs from latest allocation）**
    ```bash
nomad alloc logs $(nomad job allocs -json <job-id> | jq -r '.[0].ID')
```

- **检查集群健康状况（Check cluster health）**
    ```bash
nomad server members
nomad node status
```

## 环境变量

- `NOMAD_ADDR` — Nomad API 地址（默认：http://127.0.0.1:4646）
- `NOMAD_TOKEN` — 用于身份验证的 ACL 令牌
- `NOMAD_NAMESPACE` — 默认命名空间
- `NOMAD_REGION` — 默认区域
- `NOMAD_CACERT` — TLS 证书的路径
- `NOMAD_CLIENT_CERT` — TLS 客户端证书的路径
- `NOMAD_CLIENT_KEY` — TLS 客户端密钥的路径

## 注意事项

- 该技能仅支持读操作，无法提交、停止或修改作业。
- 使用 `nomad-tui` 进行交互式集群管理。
- 要部署作业，直接使用 `nomad job run <file.nomad.hcl>` 命令。