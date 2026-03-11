---
name: exposure-sentinel
description: 检查 IP 地址是否被列在 OpenClaw 暴露监控板上（openclaw.allegro.earth）。当需要验证特定 IP 地址是否作为 OpenClaw 实例被公开暴露时，请使用此功能。该工具会扫描所有 3,357 个暴露实例的页面，以查找目标 IP 地址的存在。
---
# Exposure Sentinel

这是一个用于监控 OpenClaw Exposure Watchboard 的工具，用于检查您的 IP 地址是否被公开列为受攻击的实例。

## 使用场景

- **安全审计**：检查您的基础设施 IP 地址是否意外被公开
- **主动监控**：验证关键端点的暴露状态
- **事件响应**：确认疑似被攻击的 IP 地址是否已被公开

## 快速入门

### 检查单个 IP 地址

```bash
python3 skills/exposure-sentinel/scripts/check_ip.py 1.2.3.4
```

### 检查多个 IP 地址

```bash
python3 skills/exposure-sentinel/scripts/check_ip.py 1.2.3.4 5.6.7.8
```

### 显示扫描进度

```bash
python3 skills/exposure-sentinel/scripts/check_ip.py 1.2.3.4 -v
```

### JSON 格式输出（适用于自动化）

```bash
python3 skills/exposure-sentinel/scripts/check_ip.py 1.2.3.4 --json
```

## 工作原理

1. **并发扫描**：使用 50 个并发连接来扫描全部 3,357 个页面
2. **模式匹配**：支持完整的 IP 地址和部分掩码的 IP 地址（例如 `1.2.3.•••`）
3. **全面覆盖**：检查暴露数据库的每一页面
4. **扫描时间**：完整扫描大约需要 85-95 秒

## 结果解读

- **✅ 未找到**：该 IP 地址未出现在暴露数据库中（安全）
- **⚠️ 被暴露**：该 IP 地址出现在 Watchboard 上，并提供详细信息的链接

## 技术细节

- **来源**：https://openclaw.allegro.earth
- **总页面数**：3,357 页（每页 100 条记录）
- **总受攻击实例数**：约 335,000 个
- **扫描速度**：约 40 页/秒

## 关于 OpenClaw Exposure Watchboard

这是一个公开的安全研究数据库，用于列出可公开访问的 OpenClaw 实例，以帮助提高防御意识。如果您的 IP 地址出现在这里，说明：

1. 该实例直接暴露在互联网上
2. 可能存在身份验证问题或身份验证机制较弱
3. 建议立即采取行动：启用身份验证、限制访问或修补漏洞