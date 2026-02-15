---
name: volcengine-storage-tos
description: Volcengine TOS（对象存储服务）的操作指南。适用于用户需要执行上传/下载/同步文件、检查存储桶策略、生成带签名的URL，或解决存储相关问题的场景。
---

# volcengine-storage-tos

用于管理 TOS（Terms of Service）相关的存储桶和对象，支持显式的路径映射以及权限验证功能。

## 执行流程

1. 确认存储桶、区域以及对象的路径。
2. 验证身份认证（auth）和存储桶策略（bucket policy）。
3. 执行上传/下载/同步操作。
4. 返回包含对象键（object keys）和URL的结果清单（result manifest）。

## 安全规则

- 未经明确确认，禁止执行破坏性删除操作。
- 在上传过程中保留元数据（metadata）和内容类型（content type）。
- 在可能的情况下，提供校验和（checksum）或文件大小验证（size verification）。

## 参考资料

- `references/sources.md`