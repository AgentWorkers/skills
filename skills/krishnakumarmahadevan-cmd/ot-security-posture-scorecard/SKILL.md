---
name: ot-security-posture-scorecard
description: 评估运营技术（OT）、工业控制系统（ICS）和监控与数据采集系统（SCADA）的安全状况，并生成包含修复建议的风险评分卡。该工具适用于评估运营技术安全、工业控制系统风险、SCADA漏洞、OT与IT之间的安全差距、IEC 62443合规性，以及关键基础设施的NIST网络安全框架（CSF）符合性。
version: 1.0.0
homepage: https://portal.toolweb.in
metadata:
  openclaw:
    emoji: "🏭"
    requires:
      env:
        - TOOLWEB_API_KEY
      bins:
        - curl
    primaryEnv: TOOLWEB_API_KEY
    os:
      - linux
      - darwin
      - win32
    category: security
---
# OT安全态势评分卡 🏭🔒

本工具用于评估运营技术（OT）、工业控制系统（ICS）和SCADA环境的安全状况。它会生成一份详细的评分卡，其中包含风险等级、差距分析以及根据IEC 62443和NIST CSF框架制定的优先级修复步骤。

**由[ToolWeb.in](https://toolweb.in)的CISSP/CISM认证安全专家开发**

## 使用场景

- 用户需要评估OT、ICS或SCADA系统的安全态势
- 用户希望评估工业控制系统的风险
- 用户需要OT与IT融合的安全分析
- 用户关心OT环境是否符合IEC 62443或NIST CSF标准
- 用户需要进行关键基础设施的安全评估
- 用户需要为制造业、能源、水务或公用事业系统生成安全评分卡

## 前提条件

- `TOOLWEB_API_KEY`——请从[portal.toolweb.in](https://portal.toolweb.in)获取您的API密钥
- 系统上必须安装`curl`工具

## API端点

```
POST https://portal.toolweb.in:8443/security/itotassessor
```

## 工作流程

1. **收集用户信息**：
   - 请用户提供以下信息：
     - `org_name`：组织名称（例如：“Acme Manufacturing Corp”）
     - `sector`：行业领域（例如：“制造业”、“能源”、“水处理”、“石油与天然气”、“制药”、“交通运输”、“采矿”）
     - `ot_size`：OT环境的规模（例如：“小型”、“中型”、“大型”、“企业级”）
     - `integration_level`：IT与OT的集成程度（例如：“最低级”、“部分集成”、“完全集成”、“物理隔离”）
     - `csf_scores`：NIST CSF的自我评估分数（每个领域1-5分）。请用户对以下方面进行评分：
       - `identify`：资产管理、风险评估（1=未实施，5=最佳实践）
       - `protect`：访问控制、安全培训、数据保护（1=未实施，5=最佳实践）
       - `detect`：监控、检测流程（1=未实施，5=最佳实践）
       - `respond`：事件响应计划与执行（1=未实施，5=最佳实践）
       - `recover`：恢复计划与改进措施（1=未实施，5=最佳实践）
     - **可选字段（用户提供时使用）**：
       - `ot_technologies`：使用的OT技术列表（例如：“SCADA”、“PLC”、“HMI”、“DCS”、“RTU”）
       - `it_tools`：使用的IT安全工具列表（例如：“防火墙”、“SIEM”、“IDS”、“EDR”）
       - `threat_concern`：主要的安全威胁（例如：“针对OT网络的勒索软件”）
       - `compliance`：目标合规框架（例如：“IEC 62443”、“NIST CSF”、“NERC CIP”）
       - `known_gaps`：已知的安全漏洞（例如：“没有OT网络监控”、“PLC上使用共享凭据”）
       - `team_maturity`：安全团队的成熟度（例如：“没有专门的OT安全团队”）
       - `assessment_depth`：评估的详细程度（默认为“标准”或“详细”）

2. **使用收集到的参数调用API**：

```bash
curl -s -X POST "https://portal.toolweb.in:8443/security/itotassessor" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TOOLWEB_API_KEY" \
  -d '{
    "org_name": "<org_name>",
    "sector": "<sector>",
    "ot_size": "<ot_size>",
    "integration_level": "<integration_level>",
    "ot_technologies": ["<tech1>", "<tech2>"],
    "it_tools": ["<tool1>", "<tool2>"],
    "csf_scores": {
      "identify": <1-5>,
      "protect": <1-5>,
      "detect": <1-5>,
      "respond": <1-5>,
      "recover": <1-5>
    },
    "threat_concern": "<threat_concern>",
    "compliance": "<compliance>"
  }'
```

3. **解析响应**：
   API会返回一个JSON对象，其中包含：
     - `status`：成功或错误状态
     - `report`：包含执行摘要、NIST CSF功能分析、五大优先风险、技术栈评估以及逐步修复路线的完整Markdown报告
     - `overall_score`：总分（0-100分）
     - `csf_avg`：所有5个功能的平均CSF分数
     - `risk_level`：风险等级（“严重”、“高”、“中”、“低”）
     - `org_name`：组织名称

4. **以清晰的结构向用户展示结果**：
   - 首先展示总分和风险等级
   - 展示报告中的执行摘要
   - 强调五大优先风险
   - 介绍修复路线的各个阶段
   - 提供进一步深入查看特定部分的选项

## 输出格式

评分卡的具体展示方式如下：

```
🏭 OT/IT Convergence Security Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Organization: [org_name]
Sector: [sector]
Overall Score: [overall_score]/100 — [risk_level]
CSF Average: [csf_avg]/5.0

[Extract and present key sections from the report field:]
- Executive Summary
- Top 5 Priority Risks (with severity)
- Phase 1 Quick Wins (0-30 days)
- Recommended Technology Additions

📎 Full detailed report available — ask me to show any section
```

**注意：**`report`字段包含一份详细的Markdown报告。请先展示最具有操作性的部分（执行摘要、主要风险、快速改进措施），并根据用户需求提供完整报告或特定章节的查看。

## 错误处理

- 如果未设置`TOOLWEB_API_KEY`：告知用户从https://portal.toolweb.in获取API密钥（订阅费用为每月2,999印度卢比，约36美元）
- 如果API返回401错误：API密钥无效或已过期——请用户登录portal.toolweb.in检查订阅情况
- 如果API返回429错误：请求超出限制——请等待60秒后再重试
- 如果API返回500错误：告知用户服务暂时出现问题，建议稍后重试
- 如果系统上没有安装`curl`：建议安装`curl`（`apt install curl` / `brew install curl`）

## 示例交互

**用户**：“请评估我们水处理厂SCADA系统的安全状况。”

**操作流程**：
1. 询问用户：“为了进行评估，需要一些信息：
   - 您的组织名称是什么？
   - 您的OT环境规模如何？（小型/中型/大型）
   - 您的IT网络与OT网络的集成程度如何？（最低级/部分集成/完全集成）
   - 您能对这些方面的成熟度进行评分吗（1-5分）：资产管理、风险控制、检测、响应、恢复？”
2. 用户回答：“WaterCo Utilities，中型规模，部分集成。资产管理：3分，风险控制：2分，检测：2分，响应：1分，恢复：1分”
3. 调用API：
```bash
curl -s -X POST "https://portal.toolweb.in:8443/security/itotassessor" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TOOLWEB_API_KEY" \
  -d '{
    "org_name": "WaterCo Utilities",
    "sector": "Water Treatment",
    "ot_size": "Medium",
    "integration_level": "Partial",
    "ot_technologies": ["SCADA", "PLC", "HMI"],
    "csf_scores": {"identify":3,"protect":2,"detect":2,"respond":1,"recover":1}
  }'
```
4. 向用户展示评分卡：总分、风险等级、执行摘要、主要风险和快速改进措施

## 价格政策

- 通过portal.toolweb.in的订阅计划访问API：
  - 入门级：每月2,999印度卢比（约36美元）——500次API调用
  - 专业级：每月9,999印度卢比（约120美元）——5,000次API调用
  - 企业级：每月49,999印度卢比（约600美元）——无限次API调用
  - 免费试用：10次API调用

**国际用户（美国、英国、欧洲）**：在结账时选择**PayPal**作为支付方式，支持USD、EUR、GBP或其他6种国际货币。PayU会自动处理货币转换。

## 关于我们

本工具由**ToolWeb.in**开发——这是一个专注于安全的MicroSaaS平台，提供191多种安全API，由CISSP和CISM认证的专业人士构建。受到美国、英国和欧洲安全团队的信赖。

- 🌐 平台：https://toolweb.in
- 🔌 API Hub：https://portal.toolweb.in
- 📺 YouTube演示视频：https://youtube.com/@toolweb
- 🛒 也在RapidAPI上提供：https://rapidapi.com/user/mkkpro

## 提示

- 为了获得最实用的结果，请提供关于OT环境的详细信息
- 每季度进行一次评估，以跟踪安全状况的改进情况
- 直接使用合规性分析结果进行审计准备
- 结合IT风险评估工具，获得全面的IT+OT安全视图