---
name: healthkit-sync
description: iOS HealthKit 数据同步的 CLI 命令及使用模式。适用于使用 healthsync CLI 时获取 Apple Health 数据（步数、心率、睡眠记录、运动数据），通过局域网配对 iOS 设备，以及了解 iOS Health Sync 项目的架构，包括 mTLS 证书绑定、Keychain 存储机制和审计日志记录等功能。
license: Apache-2.0
compatibility: macOS with healthsync CLI installed (~/.healthsync/config.json)
metadata:
  category: development
  platforms: ios,macos
  author: mneves
---

# HealthKit 同步 CLI

使用 mTLS 协议，通过本地网络安全地将 Apple HealthKit 数据从 iPhone 同步到 Mac。

## 适用场景

- 用户询问如何同步健康数据
- 用户提到 `healthsync` CLI 命令
- 用户需要获取步数、心率、睡眠或锻炼数据
- 用户需要将 Mac 与 iOS 设备配对
- 用户想了解 iOS Health Sync 项目的架构
- 用户提及证书固定（certificate pinning）或 mTLS 安全机制

## CLI 快速参考

### 配对流程（首次使用）

```bash
# 1. Discover devices on local network
healthsync discover

# 2. On iOS app: tap "Share" to generate QR code, then "Copy"
# 3. Scan QR from clipboard (Universal Clipboard)
healthsync scan

# Alternative: scan from image file
healthsync scan --file ~/Desktop/qr.png
```

### 获取健康数据

```bash
# Check connection status
healthsync status

# List enabled data types
healthsync types

# Fetch data as CSV (default)
healthsync fetch --start 2026-01-01T00:00:00Z --end 2026-12-31T23:59:59Z --types steps

# Fetch multiple types as JSON
healthsync fetch --start 2026-01-01T00:00:00Z --end 2026-12-31T23:59:59Z \
  --types steps,heartRate,sleepAnalysis --format json | jq

# Pipe to file
healthsync fetch --start 2026-01-01T00:00:00Z --end 2026-12-31T23:59:59Z \
  --types steps > steps.csv
```

### 可用的健康数据类型

**活动（Activity）**：步数（steps）、步行距离（walkingDistance）、跑步距离（runningDistance）、骑行距离（cyclingDistance）、消耗的活跃能量（activeEnergyBurned）、基础能量消耗（basalEnergyBurned）、锻炼时间（exerciseTime）、站立时间（standHours）、爬升高度（flightsClimbed）、锻炼记录（workouts）

**心率（Heart Rate）**：心率（heartRate）、静息心率（restingHeartRate）、步行平均心率（walkingHeartRateAverage）、心率变异性（heartRateVariability）

**生命体征（Vitals）**：收缩压（bloodPressureSystolic）、舒张压（bloodPressureDiastolic）、血氧饱和度（bloodOxygen）、呼吸频率（respiratoryRate）、体温（bodyTemperature）、最大摄氧量（vo2Max）

**睡眠（Sleep）**：睡眠分析（sleepAnalysis）、在床睡眠时间（sleepInBed）、睡眠状态（sleepAsleep）、睡眠清醒时间（sleepAwake）、快速眼动睡眠（sleepREM）、深度睡眠（sleepDeep）

**身体信息（Body）**：体重（weight）、身高（height）、身体质量指数（bodyMassIndex）、体脂百分比（bodyFatPercentage）、瘦体重（leanBodyMass）

## 配置

配置信息存储在 `~/.healthsync/config.json` 文件中（权限：0600）：
```json
{
  "host": "192.168.1.x",
  "port": 8443,
  "fingerprint": "sha256-certificate-fingerprint"
}
```

令牌（Token）存储在 macOS 的 Keychain 中，服务名称为 `org.mvneves.healthsync.cli`。

## 安全架构

### 证书固定（Certificate Pinning）

CLI 通过 SHA256 指纹（TOFU 模型）验证服务器证书：
1. 首次配对时会从 QR 码中存储证书指纹。
2. 后续连接时会验证指纹是否匹配。
3. 如果指纹不匹配，连接将被拒绝（防止中间人攻击）。

### 仅限本地网络

主机验证限制连接范围为：
- `localhost`
- `*.local` 域名
- 私有 IPv4 地址：`192.168.*`, `10.*`, `172.16-31.*`
- IPv6 回环地址：`::1`, 链路本地地址：`fe80::`

### Keychain 存储

令牌从不存储在配置文件中，始终保存在 Keychain 中，具有以下保护设置：
- `kSecAttrAccessibleWhenUnlocked` 保护级别
- 服务名称：`org.mvneves.healthsync.cli`
- 账户名称：`token-{host}`

## 项目架构

```
ai-health-sync-ios-clawdbot/
├── iOS Health Sync App/          # Swift 6 iOS app
│   ├── Services/Security/        # CertificateService, KeychainStore, PairingService
│   ├── Services/HealthKit/       # HealthKitService, HealthSampleMapper
│   ├── Services/Network/         # NetworkServer (TLS), HTTPTypes
│   └── Services/Audit/           # AuditService (SwiftData)
└── macOS/HealthSyncCLI/          # Swift Package CLI
```

## 故障排除

**“未找到设备”**：
- 确保 iOS 应用已启用数据共享功能。
- 两台设备必须处于同一 Wi-Fi 网络中。
- 检查防火墙是否阻止了 mDNS（端口 5353）。

**“配对代码过期”**：
- 在 iOS 应用中生成新的 QR 码（代码有效期为 5 分钟）。

**“证书不匹配”**：
- 删除 `~/.healthsync/config.json` 文件并重新配对。
- 可能是服务器证书已更新。

**“连接被拒绝”**：
- iOS 应用服务器可能未运行。
- 运行 `healthsync status --dry-run` 命令进行无连接测试。

## 参考资料

- [CLI 参考文档](references/CLI-REFERENCE.md) - 详细命令说明
- [安全机制](references/SECURITY.md) - mTLS 和证书固定相关内容
- [项目架构](references/ARCHITECTURE.md) - iOS 应用架构详情