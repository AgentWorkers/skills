---
name: sla-monitor
description: 为AI代理和服务设置SLA监控和运行时间跟踪机制。生成监控配置文件、警报规则以及事件响应方案。在将代理部署到生产环境并需要确保可靠性的情况下使用该功能。
---
# SLA监控技能

## 目的  
帮助团队为AI代理和自动化服务设置生产级监控机制。涵盖运行时间跟踪、响应时间SLA、错误预算以及事件升级流程。

## 使用场景  
- 部署AI代理到生产环境  
- 为面向客户的自动化系统设置监控  
- 为服务协议创建SLA文档  
- 建立事件响应流程  

## 监控工具选择  

### 选项1：UptimeRobot（提供免费 tier）  
- 免费提供50个监控指标，监控间隔为5分钟  
- 支持HTTP、关键词检测、ping测试和端口监控  
- 支持通过电子邮件、Slack和Webhook发送警报  

### 选项2：Better Stack（前身为Uptime.com）  
- 内置状态页面和事件管理功能  
- 免费 tier支持10个监控指标  

### 选项3：自托管（使用Uptime Kuma）  
```bash
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
```  

## SLA等级  

### 第1级：标准级（每月1,500美元）  
- 99.5%的运行时间保障（每年平均停机时间为4.38小时）  
- 工作时间内响应时间不超过4小时  
- 提供每月性能报告  

### 第2级：专业级（每月3,000美元）  
- 99.9%的运行时间保障（每年平均停机时间为8.76小时）  
- 工作时间内响应时间不超过1小时  
- 提供每周性能报告  
- 每季度进行优化评估  

### 第3级：企业级（每月5,000美元以上）  
- 99.95%的运行时间保障（每年平均停机时间为4.38小时）  
- 24/7小时内响应  
- 提供实时监控仪表盘  
- 提供专属技术支持  

## 警报配置模板  
```yaml
monitors:
  - name: "Agent Health Check"
    type: http
    url: "https://your-agent-endpoint/health"
    interval: 300  # 5 minutes
    alerts:
      - type: email
        threshold: 1  # alert after 1 failure
      - type: slack
        webhook: "${SLACK_WEBHOOK}"
        threshold: 2  # alert after 2 consecutive failures
      - type: sms
        threshold: 3  # escalate after 3 failures

  - name: "API Response Time"
    type: http
    url: "https://your-agent-endpoint/api"
    interval: 60
    expected_response_time: 2000  # ms
    alerts:
      - type: slack
        condition: "response_time > 5000"

error_budget:
  monthly_target: 99.9
  burn_rate_alert: 2.0  # Alert if burning 2x normal rate
```  

## 事件响应流程  

### 严重级别1：完全中断  
1. 5分钟内确认收到警报  
2. 10分钟内更新状态页面  
3. 30分钟内查明根本原因  
4. 2小时内解决问题或提供临时解决方案  
5. 24小时内进行事后分析  

### 严重级别2：性能下降  
1. 15分钟内确认收到警报  
2. 30分钟内展开调查  
3. 4小时内解决问题  
4. 48小时内提交总结报告  

### 严重级别3：小问题  
1. 1小时内确认收到警报  
2. 24小时内解决问题  
3. 将问题记录在下次评估周期中  

## 错误预算计算器  
```
Monthly minutes: 43,200 (30 days)
99.9% SLA = 43.2 minutes downtime allowed
99.5% SLA = 216 minutes downtime allowed
99.0% SLA = 432 minutes downtime allowed

Burn rate = (actual downtime / budget) × 100
If burn rate > 50% with 2+ weeks remaining → review needed
If burn rate > 80% → freeze deployments
```  

## 状态页面模板  
向客户提供公开的状态页面，显示：  
- 当前系统状态（正常运行/性能下降/中断中）  
- 各组件的运行状态（代理A、代理B、API、仪表盘）  
- 近30天的运行时间百分比  
- 事件历史记录及解决详情  
- 预定的维护时间  

## 下一步行动  
需要具备内置SLA监控功能的AI代理管理服务吗？  
→ AfrexAI可提供每月1,500美元的部署、监控和维护服务  
→ 预约咨询：https://calendly.com/cbeckford-afrexai/30min  
→ 了解更多信息：https://afrexai-cto.github.io/aaas/landing.html