---
name: pihole-ctl
description: 管理和监控本地的 Pi-hole 实例。通过 CLI 查询 FTL 数据库以获取统计信息（被拦截的广告数量、主要使用该服务的用户等），并控制 Pi-hole 的运行状态。当用户询问“拦截了多少广告”、“Pi-hole 的当前状态”或“更新配置参数”时，可以使用此功能。
---

# Pi-hole 控制器

## 使用方法
- **功能**：网络守护者。
- **触发条件**：执行“检查 Pi-hole 状态”、“查看 Adblock 的运行状态”或“查询访问量最高的域名”等操作。
- **输出结果**：以 JSON 格式显示统计数据或通过 CLI 命令返回结果。

## 功能特性
1. **数据统计**：从 FTL 数据库中查询准确的日志信息（过去 24 小时的数据、访问量最高的域名等）。
2. **管理功能**：启用/禁用 Pi-hole 的阻止功能（`pihole enable/disable`）。
3. **阻止列表管理**：更新 Gravity 的阻止规则（`pihole -g`）。
4. **审计功能**：识别频繁发送请求的客户端或被频繁阻止的域名。

## 脚本
- `scripts/query_db.py`：一个使用 Python 的 `sqlite3` 库来安全地查询 Pi-hole 统计数据的脚本。
  - 需要具有对 `/etc/pihole/pihole-FTL.db` 文件的读取权限。
  - 使用方法：`python3 scripts/query_db.py --summary --hours 24`（查看过去 24 小时的统计信息）
  - 使用方法：`python3 scripts/query_db.py --top 10`（查询访问量最高的 10 个域名）

## 权限要求
- **数据库访问权限**：执行该功能的用户必须具有对 `/etc/pihole/pihole-FTL.db` 文件的读取权限。
  - 建议：将用户添加到 `pihole` 组中（`usermod -aG pihole ubuntu`）。
- **管理命令**：使用 `pihole` CLI 命令（如启用/禁用功能）需要 `sudo` 权限，或者必须由具有相应权限的用户来执行。

## 参考资料
- [数据库架构](references/db-schema.md)