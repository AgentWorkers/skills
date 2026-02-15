---
name: aws-ecs-monitor
description: **使用 CloudWatch 日志分析进行 AWS ECS 生产环境健康监控**  
该方案可监控 ECS 服务的运行状态、ALB（应用负载均衡器）目标服务器的运行状况以及 SSL 证书的有效性，并提供深入的 CloudWatch 日志分析功能。这些分析功能有助于错误分类、自动检测服务器重启情况以及及时发出生产环境异常警报。
---

# AWS ECS 监控器

用于监控 AWS ECS 服务的运行状态并分析日志。

## 功能概述

- **运行状态检查**：通过 HTTP 请求检查您的域名、ECS 服务的运行状态（是否正常运行）、ALB 目标组的健康状况以及 SSL 证书的有效期。
- **日志分析**：从 CloudWatch 中获取日志，对错误类型进行分类（如 panic、fatal、OOM、timeout、5xx 错误），检测容器重启事件，并过滤掉与运行状态无关的日志信息。
- **自动诊断**：根据日志分析结果自动诊断出现问题的服务。

## 前提条件

- 需要配置具有相应 IAM 权限的 `aws` CLI，具备以下权限：
  - `ecs:ListServices`, `ecs:DescribeServices`
  - `elasticloadbalancing:DescribeTargetGroups`, `elasticloadbalancing:DescribeTargetHealth`
  - `logs:FilterLogEvents`, `logs:DescribeLogGroups`
- 需要 `curl` 命令工具用于执行 HTTP 健康状态检查。
- 需要 `python3` 用于处理 JSON 数据和日志分析。
- （可选）需要 `openssl` 工具用于检查 SSL 证书的有效性。

## 配置方式

所有配置均通过环境变量完成：

| 变量          | 是否必填 | 默认值         | 说明                                      |
|---------------|---------|------------------|-----------------------------------------|
| `ECS_CLUSTER`     | 是       | —            | ECS 集群名称                                      |
| `ECS_REGION`     | 否       | `us-east-1`       | AWS 区域                                      |
| `ECS_DOMAIN`     | 否       | —            | 用于 HTTP/SSL 检查的域名（未设置时可省略）                   |
| `ECS_SERVICES`     | 否       | 自动检测        | 用逗号分隔的待监控服务名称                          |
| `ECS_HEALTH_STATE`     | 否       | `./data/ecs-health.json` | 用于存储健康状态信息的 JSON 文件路径                 |
| `ECS_health_OUTDIR` | 否       | `./data/`        | 日志和警报的输出目录                             |
| `ECS_LOG_PATTERN`     | 否       | `/ecs/{service}`     | CloudWatch 日志组匹配模式（`{service}` 会被替换）             |
| `ECS_HTTP_ENDPOINTS`     | 否       | —            | 用于 HTTP 请求的 URL 列表（用逗号分隔）                        |

## 脚本说明

### `scripts/ecs-health.sh` — 运行状态监控脚本

```bash
# Full check
ECS_CLUSTER=my-cluster ECS_DOMAIN=example.com ./scripts/ecs-health.sh

# JSON output only
ECS_CLUSTER=my-cluster ./scripts/ecs-health.sh --json

# Quiet mode (no alerts, just status file)
ECS_CLUSTER=my-cluster ./scripts/ecs-health.sh --quiet
```

退出代码说明：
- `0`：服务运行正常
- `1`：服务运行异常/性能下降
- `2`：脚本执行错误

### `scripts/cloudwatch-logs.sh` — 日志分析脚本

```bash
# Pull raw logs from a service
ECS_CLUSTER=my-cluster ./scripts/cloudwatch-logs.sh pull my-api --minutes 30

# Show errors across all services
ECS_CLUSTER=my-cluster ./scripts/cloudwatch-logs.sh errors all --minutes 120

# Deep analysis with error categorization
ECS_CLUSTER=my-cluster ./scripts/cloudwatch-logs.sh diagnose --minutes 60

# Detect container restarts
ECS_CLUSTER=my-cluster ./scripts/cloudwatch-logs.sh restarts my-api

# Auto-diagnose from health state file
ECS_CLUSTER=my-cluster ./scripts/cloudwatch-logs.sh auto-diagnose

# Summary across all services
ECS_CLUSTER=my-cluster ./scripts/cloudwatch-logs.sh summary --minutes 120
```

可选参数：
- `--minutes N`（默认值：60）：日志分析的间隔时间（分钟）
- `--json`：以 JSON 格式输出日志
- `--limit N`（默认值：200）：每次分析的日志条目数量
- `--verbose`：详细输出日志信息

## 自动检测机制

当未设置 `ECS_SERVICES` 时，这两个脚本会自动从 ECS 集群中检测服务。

```bash
aws ecs list-services --cluster $ECS_CLUSTER
```

日志组通过指定的模式 `/ecs/{service}` 进行匹配；如需自定义模式，可修改 `ECS_LOG_PATTERN`。

```bash
# If your log groups are /ecs/prod/my-api, /ecs/prod/my-frontend, etc.
ECS_LOG_PATTERN="/ecs/prod/{service}" ECS_CLUSTER=my-cluster ./scripts/cloudwatch-logs.sh diagnose
```

## 集成方式

当检测到问题时，运行状态监控脚本可以触发日志分析脚本进行自动诊断。请将 `ECS_health_OUTDIR` 设置为共享目录，并同时运行这两个脚本。

## 错误分类

日志分析脚本将错误类型分为以下几类：

- `panic`：Go 语言程序中的 panic 错误
- `fatal`：致命错误
- `oom`：内存溢出错误
- `timeout`：连接/请求超时错误
- `connection_error`：连接请求被拒绝或重置
- `http_5xx`：HTTP 500 级错误响应
- `python_traceback`：Python 程序中的异常堆栈跟踪
- `exception`：其他通用异常
- `auth_error`：权限/认证失败
- `structured_error`：结构化的错误日志
- `error`：其他一般的错误信息

来自 ALB 的 `/health`（GET/HEAD 请求）请求产生的无关日志信息会自动从错误统计和 HTTP 状态分布数据中过滤掉。