---
name: flowtriq-monitor
description: 使用 Flowtriq API 实时监控和管理 Flowtriq 的 DDoS 检测功能。当用户询问有关活跃攻击、节点状态、事件历史记录、流量指标、PCAP 捕获数据、代理配置或其被 Flowtriq 监控的基础设施的缓解状态等信息时，可使用此技能。触发语句包括：“检查我的节点”、“是否有攻击”、“什么在攻击我的服务器”、“显示事件记录”、“是否有系统正在受到攻击”、“Flowtriq 的状态”、“检查流量”、“获取我的事件记录”，以及任何与 Flowtriq 监控、警报、状态或流量相关的请求。需要使用 FLOWTRIQ_API_KEY 和 FLOWTRIQ_NODE_UUID 环境变量。
metadata:
  openclaw:
    requires:
      env:
        - FLOWTRIQ_API_KEY
        - FLOWTRIQ_NODE_UUID
---
# Flowtriq 监控技能

该技能允许您直接通过 OpenClaw 代理监控受 Flowtriq 保护的基础设施。您可以提出自然语言问题，代理会查询 Flowtriq API 并为您解读结果。

**基础 URL：** `https://flowtriq.com`  
**所有代理端点都需要以下认证头：**  
```
Authorization: Bearer $FLOWTRIQ_API_KEY
X-Node-UUID: $FLOWTRIQ_NODE_UUID
```  

---

## 您可以提出的问题  
- “目前是否有任何节点正在遭受攻击？”  
- “我的服务器当前的流量情况如何？”  
- “显示最近的攻击事件。”  
- “上次攻击时的峰值 PPS 是多少？”  
- “我的代理是否在线？”  
- “获取我的节点配置和阈值信息。”  
- “最近是否有任何 IOC（Incident Object Count）匹配？”  

---

## API 调用参考  

### 检查代理健康状况/节点状态  
```
GET https://flowtriq.com/api/health
```  
无需认证。返回 `{ "status": "ok" }`。在发起需要认证的请求之前，先使用此接口确认 Flowtriq 平台是否可访问。  

---

### 获取节点配置及当前阈值  
```
GET https://flowtriq.com/api/v1/agent/config
Headers: Authorization + X-Node-UUID
```  
返回节点当前的 PPS 阈值、基准统计数据（p99、平均值）、已加载的 IOC 模式以及代理队列中待处理的命令。  
需要展示给用户的字段：  
- `pps_threshold`：触发事件的 PPS 阈值  
- `baseline.p99_pps`：节点的正常 p99 流量水平  
- `baseline.mean_pps`：平均基准流量  
- `ioc_patterns`：已加载的 IOC 模式数量  
- `pending_commands`：存在的待处理命令  

---

### 获取最新指标（当前流量）  
```
POST https://flowtriq.com/api/v1/agent/metrics
Headers: Authorization + X-Node-UUID
```  
代理每秒会向此端点发送一次流量数据。要查看当前的流量状态，请使用仪表板 API；由于仪表板端点需要会话认证，请指导用户访问 `https://flowtriq.com/dashboard` 进行实时查看，或从配置端点获取基准信息。  

---

### 提交/检查攻击事件  
```
POST https://flowtriq.com/api/v1/agent/incident
Headers: Authorization + X-Node-UUID
```  
代理使用此接口来创建和更新攻击事件。在解读用户返回或确认的事件数据时，需向用户展示以下信息：  
| 字段 | 向用户说明的内容 |  
|---|---|  
| `attack_family` | 用通俗语言描述攻击类型（例如：UDP 洪水攻击、SYN 洪水攻击等）  
| `severity` | 严重程度（低/中/高/危急）  
| `peak_pps` | 攻击峰值（以每秒数据包数表示）  
| `peak_bps` | 转换为 Gbps 或 Mbps 以便阅读  
| `source_ip_count` | 来源 IP 的数量  
| `geo_breakdown` | 按流量量排序的来源国家  
| `ioc_matches` | 匹配的僵尸网络/攻击模式  
| `spoofing_detected` | 如果为真，则警告用户  
| `botnet_detected` | 如果为真，则警告用户  

**攻击类型对照表：**  
- `udp_flood` = UDP 洪水攻击  
- `syn_flood` = SYN 洪水攻击  
- `http_flood` = HTTP 洪水攻击  
- `icmp_flood` = ICMP/Ping 洪水攻击  
- `dns_flood` = DNS 放大攻击  
- `multi_vector` = 多向量攻击（多种攻击类型的组合）  
- `unknown` = 未分类的攻击  

**严重程度说明：**  
- **低**：低于基准值的 2 倍，属于信息提示级别  
- **中**：为基准值的 2 至 5 倍，需要密切监控  
- **高**：为基准值的 5 至 20 倍，可能需要采取缓解措施  
- **危急**：超过基准值的 20 倍，进入全面响应模式  

---

### 注册新节点（如果用户请求）  
```
POST https://flowtriq.com/api/deploy
Headers: Authorization: Bearer YOUR_DEPLOY_TOKEN
Body: { "name": "node-name", "ip": "x.x.x.x" }
```  
注意：此操作使用的是 **部署令牌**（deploy token），而非节点 API 密钥。用户需要单独提供部署令牌。返回新节点的 `node_uuid` 和 `api_key`。  

---

## 向用户解释结果  

始终将原始 API 数据转换为易于理解的 NOC（Network Operations Center）风格摘要。例如：  
- **一切正常：**  
  > “您的节点已在线。基准 p99 为 12,000 PPS，阈值设置为 50,000 PPS。没有活跃事件。已加载 8 个 IOC 模式。”  
- **发生攻击：**  
  > “[节点] 发生攻击，严重程度为危急。峰值达到 47,821 PPS（1.7 Gbps）。来自 3,241 个唯一 IP 地址，检测到欺骗行为。IOC 匹配结果：mirai-variant（置信度 94%）。建议检查仪表板上的 FlowSpec 规则状态。”  
- **系统降级/代理离线：**  
  > “Flowtriq 平台可访问，但您的节点最近没有发送心跳信号。可能是代理出现故障。请在服务器上运行 `sudo systemctl status ftagent` 命令进行检查。”  

---

## 错误处理  
| HTTP 状态码 | 含义 | 告诉用户的提示 |  
|---|---|---|  
| 401 | API 密钥错误 | “您的 API 密钥无效或已过期。请在 Flowtriq 仪表板中更新密钥。”  
| 402 | 订阅问题 | “您的 Flowtriq 订阅可能已过期，请检查账单信息。”  
| 409 | 节点名称重复 | “工作区中已存在同名节点。”  
| 400 | 缺少字段 | 显示缺失的字段，并要求用户提供相应信息  
| 5xx | 平台错误 | “Flowtriq 返回了服务器错误。请访问 https://flowtriq.com/status 查看故障详情。”  

---

## 设置提醒（如果用户未配置环境变量）  
如果 `FLOWTRIQ_API_KEY` 或 `FLOWTRIQ_NODE_UUID` 未设置，请告知用户：  
> “要使用此技能，您需要在 OpenClaw 中配置两个环境变量：  
> - `FLOWTRIQ_API_KEY`：可在 Flowtriq 仪表板的 **设置 > API 密钥** 中找到  
> - `FLOWTRIQ_NODE_UUID`：可在节点的设置页面中找到  
>  
> 请将这些变量添加到 OpenClaw 的环境配置中，然后重新加载代理。”  

---

## 参考文件  
- `references/attack-types.md`：详细介绍所有 8 种攻击类型、其原因及推荐的应对措施  
- `references/api-endpoints.md`：包含所有端点的完整参考信息，便于在复杂任务中快速查找参数