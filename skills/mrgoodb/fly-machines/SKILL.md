---
name: fly-machines
description: 部署和管理 Fly.io 机器：创建、启动、停止、删除以及监控容器化应用程序。该工具可用于部署容器、管理应用程序实例以及编排多租户工作负载。
metadata: {"clawdbot":{"emoji":"🪰"}}
---

# fly-machines

使用 Machines API 在 Fly.io 上部署和管理容器。

## 设置

1. 从 https://fly.io/user/personal_access_tokens 获取 Fly.io API 令牌。
2. 将其存储在以下位置：
```bash
mkdir -p ~/.config/fly
echo "your_token_here" > ~/.config/fly/token
```

或者使用环境变量：
```bash
export FLY_API_TOKEN="your_token_here"
```

## API 参考

基础 URL：`https://api.machines.dev/v1`

所有请求都需要：
```bash
FLY_TOKEN=$(cat ~/.config/fly/token 2>/dev/null || echo $FLY_API_TOKEN)
curl -H "Authorization: Bearer $FLY_TOKEN" \
     -H "Content-Type: application/json" \
     "https://api.machines.dev/v1/..."
```

## 应用管理

**列出所有应用：**
```bash
curl -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps?org_slug=personal"
```

**创建应用：**
```bash
curl -X POST -H "Authorization: Bearer $FLY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.machines.dev/v1/apps" \
  -d '{
    "app_name": "my-app",
    "org_slug": "personal"
  }'
```

**获取应用详情：**
```bash
curl -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app"
```

## 机器

**列出应用中的机器：**
```bash
curl -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/machines"
```

**创建机器：**
```bash
curl -X POST -H "Authorization: Bearer $FLY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.machines.dev/v1/apps/my-app/machines" \
  -d '{
    "name": "worker-1",
    "region": "iad",
    "config": {
      "image": "nginx:latest",
      "env": {
        "MY_VAR": "value"
      },
      "services": [{
        "ports": [{"port": 443, "handlers": ["tls", "http"]}],
        "protocol": "tcp",
        "internal_port": 80
      }],
      "guest": {
        "cpu_kind": "shared",
        "cpus": 1,
        "memory_mb": 256
      }
    }
  }'
```

**获取机器信息：**
```bash
curl -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/machines/{machine_id}"
```

**启动机器：**
```bash
curl -X POST -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/machines/{machine_id}/start"
```

**停止机器：**
```bash
curl -X POST -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/machines/{machine_id}/stop"
```

**删除机器：**
```bash
curl -X DELETE -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/machines/{machine_id}?force=true"
```

**等待机器状态变化：**
```bash
curl -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/machines/{machine_id}/wait?state=started&timeout=60"
```

## 卷（Volumes）

**列出所有卷：**
```bash
curl -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/volumes"
```

**创建卷：**
```bash
curl -X POST -H "Authorization: Bearer $FLY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.machines.dev/v1/apps/my-app/volumes" \
  -d '{
    "name": "data_vol",
    "region": "iad",
    "size_gb": 1
  }'
```

**将卷挂载到机器上：**
```bash
# Include in machine config:
{
  "config": {
    "mounts": [{
      "volume": "vol_abc123",
      "path": "/data"
    }]
  }
}
```

## 机器配置选项**

```json
{
  "name": "my-machine",
  "region": "iad",
  "config": {
    "image": "registry.fly.io/my-app:latest",
    "env": {"KEY": "value"},
    "guest": {
      "cpu_kind": "shared",
      "cpus": 1,
      "memory_mb": 256
    },
    "services": [{
      "ports": [
        {"port": 80, "handlers": ["http"]},
        {"port": 443, "handlers": ["tls", "http"]}
      ],
      "protocol": "tcp",
      "internal_port": 8080
    }],
    "mounts": [{"volume": "vol_id", "path": "/data"}],
    "auto_destroy": false,
    "restart": {"policy": "on-failure"}
  }
}
```

## 地区（Regions）

常见地区：
- `iad` - 弗吉尼亚州阿什本（美国东部）
- `lax` - 洛杉矶（美国西部）
- `cdg` - 巴黎
- `lhr` - 伦敦
- `nrt` - 东京
- `sin` - 新加坡
- `syd` - 悉尼

## 自动停止/启动

机器在空闲一段时间后（默认为 5 分钟）会自动停止。收到请求后会立即启动（启动延迟约 3 秒）。

**禁用自动停止功能：**
```json
{
  "config": {
    "auto_destroy": false,
    "services": [{
      "auto_stop_machines": false,
      "auto_start_machines": true
    }]
  }
}
```

## 秘密信息（Secrets）

**设置秘密信息：**
```bash
curl -X POST -H "Authorization: Bearer $FLY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.machines.dev/v1/apps/my-app/secrets" \
  -d '{"MY_SECRET": "secret_value"}'
```

这些秘密信息可以作为环境变量在所有机器上使用。

## 常见用法模式

### 部署机器人实例
```bash
FLY_TOKEN=$(cat ~/.config/fly/token)
APP="botspawn"
BOT_ID="user123"

curl -X POST -H "Authorization: Bearer $FLY_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.machines.dev/v1/apps/$APP/machines" \
  -d '{
    "name": "bot-'"$BOT_ID"'",
    "region": "iad",
    "config": {
      "image": "registry.fly.io/botspawn-bot:latest",
      "env": {
        "BOT_ID": "'"$BOT_ID"'",
        "AI_PROVIDER": "anthropic"
      },
      "guest": {"cpu_kind": "shared", "cpus": 1, "memory_mb": 256}
    }
  }'
```

### 将资源规模缩减至零
机器在空闲时会自动停止。如需重新启动，请执行相应操作：
```bash
curl -X POST -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/machines/{id}/start"
```

### 健康检查（Health Check）
```bash
MACHINE=$(curl -s -H "Authorization: Bearer $FLY_TOKEN" \
  "https://api.machines.dev/v1/apps/my-app/machines/{id}")
echo $MACHINE | jq '{state: .state, region: .region, updated: .updated_at}'
```

## 命令行工具（CLI）替代方案

对于交互式操作，`flyctl` 命令行工具通常更为方便：
```bash
# Install
curl -L https://fly.io/install.sh | sh

# Auth
fly auth login

# Deploy
fly deploy

# List machines
fly machines list -a my-app

# SSH into machine
fly ssh console -a my-app
```

## 注意事项

- Machines API 与 Fly 的主要 GraphQL API 是分开的。
- 每台机器都是一个独立的虚拟机（使用 Firecracker 技术实现）。
- 卷具有地域限制，只能挂载到同一地区的机器上。
- 机器之间通过 `.internal` DNS 进行私有网络通信。
- 日志记录：可以使用 `fly logs -a my-app` 命令查看，或通过 Fly 仪表板查看。