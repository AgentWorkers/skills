---
name: aegis
description: "自动化应急地缘政治情报系统——为冲突地区的平民提供实时威胁监测和安全警报。适用场景：  
(1) 为特定地区设置战区/危机安全监测机制；  
(2) 用户询问安全状况或威胁等级；  
(3) 配置紧急警报的发送方式；  
(4) 生成安全简报；  
(5) 制定应急准备计划。  
系统所需工具：curl、python3。  
可选功能：使用 NewsAPI 密钥以获取更全面的信息。"
---
# AEGIS — 自动化紧急地缘政治情报系统

该系统为冲突地区的平民提供基于地理位置的威胁情报和安全警报。信息来源优先为官方渠道，其次为信誉良好的媒体。系统具备反谣言验证功能，并支持多语言显示。

**请注意：** 本系统并非用于引发恐慌的工具，所提供的信息均基于现实情况，内容真实可靠，并遵循政府官方指导。

## 快速入门

### 首次设置（交互式）
```bash
python3 scripts/aegis_onboard.py
```
此操作会生成 `~/.openclaw/aegis-config.json` 文件，用于配置地理位置、语言及警报偏好设置。

### 手动配置
创建 `~/.openclaw/aegis-config.json` 文件：
```json
{
  "location": { "country": "AE", "city": "Dubai", "timezone": "Asia/Dubai" },
  "language": "en",
  "alerts": { "critical_instant": true, "high_batch_minutes": 30, "medium_digest_hours": 6 },
  "briefings": { "morning": "07:00", "evening": "22:00" },
  "scan_interval_minutes": 15,
  "api_keys": {}
}
```

### 运行扫描
```bash
python3 scripts/aegis_scanner.py
```

### 设置定时任务监控
```
openclaw cron add --expr "*/15 * * * *" --message "Run AEGIS scan: python3 <skill-dir>/scripts/aegis_scanner.py --cron"
openclaw cron add --expr "0 3 * * *" --message "Generate AEGIS morning briefing: python3 <skill-dir>/scripts/aegis_briefing.py morning"
openclaw cron add --expr "0 18 * * *" --message "Generate AEGIS evening briefing: python3 <skill-dir>/scripts/aegis_briefing.py evening"
```
请根据用户所在的时区调整定时任务的执行时间（以上时间均为 UTC 格式）。

## 工作原理

### 信息来源层级（信任等级）
0. **政府紧急响应系统**（最高信任等级）：NCEMA、FEMA、民防部门
1. **主要新闻源（RSS）**：路透社（Reuters）、半岛电视台（Al Jazeera）、英国广播公司（BBC）、美联社（AP）
2. **航空/基础设施相关信息**：航行通告（NOTAMs）、机场运行状态
3. **分析/开源情报（OSINT）**：Crisis Group、ACLED、War on the Rocks
4. **高级功能（需API密钥）**：NewsAPI、GDELT

### 扫描流程
1. 根据用户位置获取所有信息来源的数据
2. 对数据进行去重处理（基于48小时内的数据变化）
3. 检索包含威胁关键词的文本（支持多语言）
4. 通过大型语言模型（LLM）进行分析：交叉验证信息来源的可靠性、对威胁进行分类并生成应对措施
5. 根据信任等级将警报信息分阶段发送（🔴 即时通知 / 🟠 批量发送 / ℹ️ 摘要形式）

### 反谣言机制
- 信任等级为0-1的信息源：直接发出警报
- 信任等级为2及以上的信息源：需要至少来自一个信任等级为0-1的信息源的佐证
- 来自社交媒体的信息或未经验证的消息：不发出警报，仅记录以供后续审核
- 特殊或离奇的声明：需要至少来自三个独立信息源的确认
- 与官方声明相矛盾的信息：标记为异常情况，并以官方信息为准

## 警报等级
🔴 **紧急**：对生命构成直接威胁，立即发送警报，包含官方指导及应对措施。
🟠 **高风险**：发生重大事件，每30分钟批量发送警报，包含影响评估。
ℹ️ **中等风险**：提供当前局势概览，每小时或每天发送一次摘要。

## 情报简报
每日早晚会发布简报，内容包括：
- 整体威胁等级及其变化趋势
- 自上次简报以来的重要事件
- 政府部门的最新动态（机场、学校、政府服务相关）
- 应急准备清单
- 信息来源链接

## 国家概况
每个支持的国家在 `references/country-profiles/` 目录下都有对应的资料文件，内容包括：
- 当地应急机构的联系方式和热线电话
- 大使馆联系方式（针对美国、英国等国家）
- 该国的特定新闻来源
- 应急避难和疏散指南
- 该地区的常见威胁关键词

如需添加新的国家，请复制 `references/country-profiles/_template.json` 文件，填写相关信息后提交 Pull Request（PR）。

## 应急准备资源
请参阅 `references/preparedness/` 目录：
- `go-bag-checklist.md`：应急包准备清单
- `communication-plan.md`：家庭沟通计划
- `shelter-guidance.md：就地避难指南
- `evacuation-guidance.md：疏散指南`

## 配置参考
详细配置选项请参阅 `references/config-reference.md`。

## 成本
- **基础版本（无需API密钥）**：每天消耗约0.03-0.05美元的LLM代币（或使用Copilot/本地模型可免费使用）
- **使用NewsAPI**：免费 tier（每天100次请求）即可满足需求
- **RSS/网络爬虫功能**：始终免费提供

## 添加信息来源
请编辑 `references/source-registry.json` 文件以添加或删除信息来源。每个信息来源需包含以下信息：
- `name`（名称）
- `url`（网址）
- `type`（类型：rss、web、api）
- `tier`（信任等级：0-4）
- `countries`（覆盖的国家范围：ISO代码或“全球”）
- 用于数据提取的 `parser` 规范