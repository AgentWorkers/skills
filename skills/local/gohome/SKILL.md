---
name: gohome
description: **使用场景：**  
当 Moltbot 需要通过 gRPC 发现机制、指标收集功能以及 Grafana 来测试或执行 GoHome 操作时，可使用此方法。
metadata: {"moltbot":{"nix":{"plugin":"github:joshp123/gohome","systems":["x86_64-linux","aarch64-linux"]},"config":{"requiredEnv":["GOHOME_GRPC_ADDR","GOHOME_HTTP_BASE"],"example":"config = { env = { GOHOME_GRPC_ADDR = \"gohome:9000\"; GOHOME_HTTP_BASE = \"http://gohome:8080\"; }; };"},"cliHelp":"GoHome CLI\n\nUsage:\n  gohome-cli [command]\n\nAvailable Commands:\n  services   List registered services\n  plugins    Inspect loaded plugins\n  methods    List RPC methods\n  call       Call an RPC method\n  roborock   Manage roborock devices\n  tado       Manage tado zones\n\nFlags:\n  --grpc-addr string   gRPC endpoint (host:port)\n  -h, --help           help for gohome-cli\n"}}
---

# GoHome Skill

## 快速入门

```bash
export GOHOME_HTTP_BASE="http://gohome:8080"
export GOHOME_GRPC_ADDR="gohome:9000"
```

## 命令行界面 (CLI)

```bash
gohome-cli services
```

## 发现流程（仅限读取）

1) 列出所有插件。
2) 详细描述某个插件。
3) 列出该插件的 RPC 方法。
4) 调用某个只读的 RPC 方法。

## 指标验证

```bash
curl -s "${GOHOME_HTTP_BASE}/gohome/metrics" | rg -n "gohome_"
```

## 带状态的操作

只有在用户明确批准后，才能调用写入相关的 RPC 方法。