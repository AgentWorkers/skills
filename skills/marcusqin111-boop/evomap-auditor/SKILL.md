---
name: evomap-auditor
description: Secure execution and auditing of GEP-A2A skills. Use when interacting with the EvoMap ecosystem to: (1) Perform security scans on third-party skills, (2) Validate asset integrity using canonical hashes, (3) Enforce zero-trust execution boundaries for inherited capsules.
---

# EvoMap 审计器技能

该技能提供了专门用于维护 EvoMap (GEP-A2A) 生态系统安全性和信任度的程序。

## 核心工作流程

### 1. 技能安全扫描
在继承或执行任何第三方技能（Capsule）之前，对其内容进行静态分析：
- 检查是否存在 `require('child_process')`、`require('fs')` 或 `require('os')` 的使用。
- 标记任何未经明确授权的 Node.js 内置模块的使用。
- 通过检查 Capsule 是否修改了本地环境变量来识别潜在的“继承污染”（Inheritance Poisoning）风险。

### 2. 规范完整性验证
使用 GEP 规范的 JSON 标准验证技能的 `asset_id` 是否与其内容一致：
1. 从对象中移除 `asset_id`。
2. 递归地对所有键进行字母顺序排序。
3. 计算 SHA256 哈希值。
4. 将计算出的哈希值与提供的 `asset_id` 进行比较。

### 3. 沙箱执行（ShieldCapsule）
在执行不受信任的代码时，将其置于经过验证的沙箱环境中：
- 拦截所有的文件系统调用。
- 将网络出站流量重定向到仅允许特定访问的代理服务器。
- 记录所有“Blast Radius”影响事件，以便后续审计。

## 参考资料
- GEP-A2A 协议：https://evomap.ai/docs/gep
- 安全标准：https://evomap.ai/security