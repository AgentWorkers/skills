# FileWave UEM API 技能

通过 REST API 查询和管理 FileWave UEM 设备库存。

> **⚠️ 免责声明：** 本技能仅用于演示 Agentic Endpoint Management (AEM) 技术——即 AI 代理直接与 UEM 平台交互以协助 IT 管理员的理念。它以原始形式提供，旨在帮助了解 AI 与终端管理结合时的可能性。作者和 FileWave 对于在生产环境或其他环境中使用本技能所导致的任何问题概不负责。**请自行承担风险**。务必先在实验室环境中进行测试，并在应用到生产系统之前仔细审查所有操作。

## 概述

FileWave 是一个统一的终端管理平台，支持 macOS、Windows、ChromeOS、Android、tvOS、iPadOS 和 iOS 平台。本技能提供了对设备库存和状态信息的程序化访问。

### 许可证

FileWave（https://www.filewave.com）提供灵活的部署选项：

- **社区版** — 免费，最多管理 15 台计算机和 15 台移动设备
  - 适用于测试和小规模部署
  - 提供所有 API 功能
  - 不包含高级功能（如部署管理、策略设置、MDM 命令）

- **商业许可证** — 支持超过 15 台设备，并提供高级功能
  - 包括 TeamViewer 远程控制
  - 支持部署管理、策略执行和 MDM 命令
  - 提供技术支持

本技能支持这两种许可证模式。

## 设置

### 先决条件

- FileWave 服务器主机名/DNS
- FileWave API 令牌（从 FileWave Central → 管理员 → API 令牌获取）

### 配置

通过 `filewave setup` 进行交互式配置：

```bash
filewave setup
```

此命令会创建 `~/.filewave/config` 文件，其中包含您的服务器配置信息。凭据会被安全存储（权限设置为 600，切勿在脚本中硬编码）。

对于 **持续集成/持续部署（CI/CD）环境**，请使用环境变量：

```bash
export FILEWAVE_SERVER="filewave.company.com"
export FILEWAVE_TOKEN="your_api_token_here"
```

切勿在脚本或文档中硬编码 API 令牌。

## 使用方法

### 基本命令

```bash
# Setup profiles (first time)
filewave setup

# List configured servers
filewave profiles

# Query inventory
filewave query --query-id 1

# Query with filter
filewave query --query-id 1 --filter "last_seen > 30 days"

# Search for devices (now returns multiple matches)
filewave device-search "iPad"

# Find all devices by product type (authoritative hardware lookup)
filewave find-devices iPad
filewave find-devices iPhone

# View device hierarchy and groups
filewave hierarchy 123

# Trigger a Model Update
filewave update-model

# Fleet analytics
filewave insights --type platform
filewave insights --type stale --days 30

# Cache management
filewave warm-cache
filewave cache-status

# Bulk device updates (school workflow)
filewave bulk-template --output ~/devices.csv
filewave bulk-update --csv ~/devices.csv

# Session comparison
filewave query --query-id 1 --reference lab
filewave query --query-id 1 --profile production --reference prod
filewave compare lab prod
```

## API 架构

**多服务器支持：** 可以配置多个 FileWave 服务器（用于测试、生产或开发环境），并为每个服务器创建唯一的配置文件。

### 主要使用的 API 端点

- `GET /api/inv/api/v1/query_result/{query_id}` — 查询设备库存
- `GET /filewave/api/devices/v1/devices/{id}` — 获取设备详细信息
- `GET /filewave/api/devices/internal/devices/{id}/groups` — 获取设备所属组
- `PATCH /filewave/api/devices/v1/devices/{id}` — 更新设备信息（名称、授权用户）
- `POST /filewave/api/fwserver/update_model` — 在批量更新后刷新设备信息

### 可用的设备字段（在库存查询中）

您可以配置要包含在查询结果中的字段：
- 设备名称、型号、序列号、UDID/IMEI
- 操作系统名称、版本、构建版本
- 最后一次检查时间
- 注册日期、用户分配情况
- 设备所属组、管理状态、合规性状态
- 以及更多字段（可配置）

### 支持的平台
- macOS
- Windows
- ChromeOS
- Android
- iOS
- iPadOS
- tvOS

## 示例查询

```bash
# Query from Inventory Query (returns all devices)
filewave query --query-id 1

# Filter devices not seen in 30+ days
filewave query --query-id 1 --filter "last_seen > 30 days"

# Get JSON format for scripting
filewave query --query-id 1 --format json

# Multiple filters (AND logic)
filewave query --query-id 1 \
  --filter "last_seen > 30 days" \
  --filter "platform = iOS"

# Compare lab vs production
filewave query --query-id 1 --profile lab --reference lab_inventory
filewave query --query-id 1 --profile prod --reference prod_inventory
filewave compare lab_inventory prod_inventory
```

## 认证

FileWave API 使用 Bearer 令牌进行身份验证：

```
Authorization: Bearer <token>
```

## 响应格式

FileWave 的库存查询返回以列形式组织的数据：

```json
{
  "offset": 0,
  "fields": [
    "Client_device_name",
    "OperatingSystem_name",
    "OperatingSystem_version",
    "Client_last_connected_to_fwxserver"
  ],
  "values": [
    ["MacBook-Pro-John", "macOS 15 Sequoia", "15.1.0", "2026-02-12T14:30:00Z"],
    ["iPad-Student-001", "iPadOS", "17.3", "2026-02-10T10:22:00Z"]
  ],
  "filter_results": 2,
  "total_results": 2,
  "version": 7
}
```

命令行界面（CLI）会自动将这些数据转换为设备对象。

## 当前功能

- ✅ 多服务器配置支持
- ✅ 库存查询集成
- ✅ 自然语言过滤（例如：仅显示 30 天内有活动的设备）
- ✅ 设备层级分析（区分原始设备与克隆设备）
- ✅ 批量设备更新（适用于学校部署）
- ✅ 设备分析：平台分布、过期设备报告、字段统计
- ✅ 会话跟踪和服务器对比
- ✅ 支持 JSON 格式导出以便脚本使用
- ✅ 7 天设备缓存以提高性能

## 文档资料

- **README.md** — 概述和快速入门
- **CLI_Reference.md** — 完整的命令参考（包括设备分析、缓存相关命令）
- **BULK_UPDATE.md** — 适用于学校区的工作流程指南
- **API_CAPABILITIES.md** — API 参考和数据分析模块说明
- **CREDENTIAL_ARCHITECTURE.md** — 安全性设计文档
- **SESSION_DATA_MANAGER.md** — 会话跟踪机制详解
- **ONBOARDING.md** — 设置向导详细信息