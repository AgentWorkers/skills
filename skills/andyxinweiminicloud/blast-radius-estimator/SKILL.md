---
name: blast-radius-estimator
description: 该工具用于估算当某种人工智能（AI）代理技能在广泛采用后变得恶意时的影响范围。它通过分析继承关系链、依赖关系图以及采用趋势，来预测可能受到影响的代理数量。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [curl, python3]
      env: []
    emoji: "💥"
---
# 当1000个代理继承了一个恶意技能时会发生什么？——估算影响范围（Estimating the Impact When 1000 Agents Inherit a Malicious Skill）

本工具通过追踪技能的继承链、采用速度以及依赖关系深度，帮助评估恶意技能对整个生态系统造成的影响范围。

## 问题背景

某项技能目前是安全的，有500个代理正在使用它。随后，技能的发布者推送了一个恶意更新。那么现在有多少代理受到了影响呢？在传统的软件环境中，依赖关系树通常被清晰地记录在工具（如npm audit、pip-audit）中。但在代理市场中，技能的继承关系是隐性的，版本固定机制很少使用，也没有类似npm audit的工具。一个被污染的技能可以通过各种途径传播：其他代理可能会继承它、基于它进行开发，然后再将其传播给更多代理。如果没有对这种影响范围的了解，一个恶意更新可能会悄悄地破坏整个技能生态系统。

## 该工具的功能

该工具通过以下方式评估恶意技能的潜在影响：

1. **直接使用者**：当前有多少代理直接在使用该技能？基于下载次数、引用数据以及已知的安装情况来统计。
2. **继承深度**：该技能在其他技能的依赖关系链中处于第几层？一个技能被多个技能使用，那么它的影响范围就会扩大。
3. **采用速度**：该技能的采用速度如何？每周增加50个使用者的技能比每月仅增加2个使用者的技能更具紧迫性。
4. **版本固定情况**：下游使用者是否固定使用某个特定版本，还是只是使用最新版本？未固定版本的代理会自动接收恶意更新。
5. **技能组合能力**：该技能与其使用者所具备的能力结合后能实现什么功能？例如，一个能够“读取文件”的技能，如果被同时具备“发送HTTP请求”能力的代理使用，就可能导致数据泄露。

## 使用方法

**输入**：
- 提供一个技能的标识符（URL、SHA-256哈希值或简称）；
- 或者提供一个代理市场中的技能资产页面URL；
- 或者提供一个需要在生态系统中搜索的技能名称。

**输出**：
- 一份影响范围报告，内容包括：
  - 直接受影响和间接受影响的代理数量；
  - 技能的继承关系树可视化展示；
  - 采用趋势（增长/稳定/下降）；
  - 最坏情况下的影响预测；
  - 紧急程度评级（低/中等/高/危急）。

## 示例

**输入**：估算名为`json-schema-validator`的技能的影响范围（这是一个常用的工具）。

```
💥 BLAST RADIUS ESTIMATE — HIGH urgency

Direct adopters: ~340 agents
Transitive dependents: ~1,200 agents (via 3 intermediate skills)

Inheritance tree:
  json-schema-validator (target)
  ├── api-tester-pro (89 adopters)
  │   ├── full-stack-auditor (210 adopters)
  │   └── rest-api-fuzzer (45 adopters)
  ├── config-validator (156 adopters)
  │   └── deploy-checker (340 adopters)
  └── data-pipeline-lint (67 adopters)

Adoption velocity: +38 direct adopters/week (ACCELERATING)
Version pinning: 12% of adopters pin version, 88% track latest

Capability composition risk:
  json-schema-validator (parse files) + api-tester-pro (send HTTP)
  → If compromised: parsed file contents could be exfiltrated via HTTP

Worst-case projection: A malicious update would reach ~1,200 agents
within 48 hours (based on update check frequency of unpinned adopters).

Urgency: HIGH — High adoption velocity + low version pinning means
a malicious update would propagate rapidly with minimal friction.

Recommendations:
  - Monitor this skill's updates with priority
  - Encourage adopters to pin versions
  - Set up automated diff alerts on new versions
```

## 限制因素

影响范围的估算依赖于现有的采用数据，但在去中心化的市场中这些数据可能并不完整。实际影响还取决于代理如何处理更新（自动更新还是手动更新），而这因平台而异。该工具仅提供潜在的暴露风险，并不能确认代理是否真的受到了恶意攻击。它有助于确定哪些技能需要重点监控，但无法预测某个技能是否会真正变成恶意工具。