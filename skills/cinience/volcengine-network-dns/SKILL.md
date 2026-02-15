---
name: volcengine-network-dns
description: Volcengine网络服务中的DNS记录管理功能：适用于用户需要查询/更新区域记录、调整流量路由或排查DNS传播问题的场景。
---

# volcengine-network-dns

用于管理 DNS 记录的系统，具备严格的变更范围控制及验证流程。

## 执行检查清单

1. 确认域名区域、记录类型以及目标值。
2. 在进行修改之前，先查询现有的 DNS 记录。
3. 在执行添加、更新或删除操作时，需遵守相关的 TTL（Time To Live）时间限制。
4. 通过权威 DNS 服务器和递归 DNS 服务器的查询来验证 DNS 记录的传播情况。

## 安全规则

- 避免盲目覆盖现有记录；应与现有记录进行差异对比。
- 在输出结果中保留回滚所需的参数。
- 在迁移操作前，尽量缩短 DNS 记录的 TTL 值。

## 参考资料

- `references/sources.md`