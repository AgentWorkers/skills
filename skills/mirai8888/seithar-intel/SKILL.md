# seithar-intel — 威胁情报与认知安全工具

## Seithar Group — 情报部门  
## 认知作战 | seithar.com  

这是一个专为 OpenClaw 设计的个人级网络威胁情报与认知安全分析工具。它通过监控 RSS 源来收集安全新闻、漏洞披露、漏洞利用工具以及影响力操作相关的信息，并根据用户设定的兴趣偏好对信息进行评分，每日提供简报，并可针对任何威胁（无论是技术性的还是认知层面的）进行深度分析。  

这就像是你口袋里的“ThreatMouth”一样，让你在任何聊天应用中都能随时了解网络与认知安全领域的最新动态。  

---

## 功能描述  

该工具可让你的 OpenClaw 变成一个威胁情报分析师：  
- 监控多个网络安全相关的 RSS 源（如 BleepingComputer、The Hacker News、Krebs on Security 等）；  
- 监控认知安全相关的资讯源（如 EUvsDisinfo、DFRLab 等）；  
- 根据用户设定的兴趣偏好对信息进行评分；  
- 通过你喜欢的聊天应用在早晨或傍晚发送简报；  
- 提供对任何漏洞（CVE）、漏洞利用工具、影响力操作或相关活动的深度分析；  
- 跟踪 MITRE ATT&CK 和 DISARM 框架中的技术映射关系；  
- 发现已公开发布的漏洞相关代码（PoC）；  
- 动态更新威胁态势概览。  

---

## 触发指令  

- “threat briefing” / “security briefing” / “morning briefing” / “security updates”  
- “check threats” / “check feeds” / “new vulnerabilities”  
- “explain CVE-XXXX-XXXXX” / “deep dive on [topic]” / “analyze this threat”  
- “cogdef briefing” / “cognitive security update” / “new psyops”  
- “what should I study today” / “learning recommendations”  
- “threat landscape” / “latest security trends”  
- “CVE-XXXX-XXXXX PoC” / “exploits for [software]”  
- “seithar brief”  

---

## 配置方法  

用户需在 OpenClaw 的设置中或直接通过命令配置以下内容：  

### 兴趣偏好  

告诉 OpenClaw 你的安全关注点，系统会据此调整信息评分标准。  
（示例配置代码：```
My security interests are:
- Malware analysis and reverse engineering
- Social engineering and cognitive security
- Network exploitation
- OSINT and intelligence gathering
- Influence operations and information warfare
- Vulnerability research and exploit development

I'm currently studying:
- MITRE ATT&CK framework
- DISARM framework for influence operations
- Python security tooling
- OverTheWire wargames

My skill level: intermediate

Deprioritize:
- Enterprise compliance and GRC
- Cloud IAM and AWS security
- Vendor marketing announcements
- Corporate breach notifications unless technically interesting
```）  

该工具会将这些偏好存储在内存中，并据此对所有信息进行相关性评分。  

### 源信息更新频率  

- **早晨简报**：当地时间上午 8:00 — 昨晚发布的重点信息及所有严重警报；  
- **傍晚简报**：当地时间下午 6:00 — 当日总结及评分高于 0.7 的信息；  
- **严重警报**：评分高于 0.9 的信息会立即推送。  
（示例命令：`Set my briefing time to 9 AM and 7 PM` 或 `Only send critical alerts`）  

### 源信息检查间隔  

默认为每 2 小时一次。该工具会利用 OpenClaw 的 cron/heartbeat 系统定期获取并处理信息。  

---

## 工作原理  

### 源信息收集  

每次检查时，该工具会指令 OpenClaw：  
1. 使用 `web_fetch` 工具从配置的来源列表中获取 RSS 源信息；  
2. 解析信息内容（标题、链接、发布日期、摘要/描述）；  
3. 通过 URL 哈希值排除重复内容；  
4. 对新信息根据用户设定的偏好进行评分。  

### 评分标准  

新信息的评分范围为 0.0 到 1.0：  
- **0.9 - 1.0**：高度相关，紧急程度高（如正在被利用的漏洞、0-day 漏洞、重大安全事件）；  
- **0.7 - 0.9**：相关性强，值得阅读；  
- **0.5 - 0.7**：相关性一般，可纳入每日摘要；  
- **低于 0.5**：相关性较低，除非用户特别要求，否则忽略。  

评分依据包括信息标题、摘要、来源以及相关的 CVE/技术信息。无需外部 API，该工具会自行完成评分。  

### 信息分类  

信息分为以下几类：  
- **CRITICAL ALERT**：正在被利用的漏洞、0-day 漏洞、关键基础设施相关；  
- **EXPLOIT DROP**：新发布的 CVE、漏洞利用工具；  
- **MALWARE**：恶意软件分析、相关研究报告；  
- **INFLUENCE OP**：虚假信息传播活动、认知安全相关事件；  
- **TECHNIQUE**：MITRE ATT&CK 或 DISARM 框架中的技术相关内容；  
- **LEARNING**：教程、CTF 活动记录、教育性内容；  
- **GENERAL**：行业新闻、政策动态、评论文章。  

### 简报格式  

（简报格式代码：```
╔══════════════════════════════════════════════════╗
║  SEITHAR INTELLIGENCE BRIEFING                   ║
║  2026-02-11 08:00 EST                            ║
╚══════════════════════════════════════════════════╝

CRITICAL (act now):

  🔴 [0.95] Pre-auth RCE in OpenSSH (CVE-2026-XXXXX)
     Full Disclosure | 2h ago
     Affects OpenSSH 9.x. Public PoC available.
     ▸ Say "deep dive CVE-2026-XXXXX" for full analysis

HIGH RELEVANCE:

  🟠 [0.87] Lazarus Group deploys new social engineering
     toolkit targeting crypto developers
     The Hacker News | 4h ago
     DISARM: T0047 (Develop Content), ATT&CK: T1566.001
     ▸ Say "deep dive lazarus social engineering" for analysis

  🟠 [0.82] New Nuclei templates for Spring4Shell variants
     Exploit-DB | 6h ago
     12 new detection templates + PoC payloads
     ▸ Say "explain spring4shell" for context

  🟠 [0.78] Russian influence operation targeting NATO
     narratives detected across 3 platforms
     DFRLab | 5h ago
     DISARM: T0046, T0048, T0056 | Coordinated inauthentic behavior
     ▸ Say "deep dive nato influence op" for DISARM breakdown

STUDY RECOMMENDATION:
  Based on today's feed: review SSH key exchange internals
  and pre-authentication attack surfaces. OverTheWire Bandit
  levels 14-17 cover SSH fundamentals.

──────────────────────────────────────────────────
24 items collected | 4 high relevance | 1 critical
Seithar Intelligence Division v1.0
認知作戦 | seithar.com/research
──────────────────────────────────────────────────
```）  

### 深度分析  

当用户请求“deep dive [topic]”或“explain [CVE]”时，该工具会：  
1. 通过 `web_fetch` 获取完整文章内容；  
2. 如果涉及 CVE，会查询 NVD API 获取详细漏洞信息；  
3. 在 GitHub 上搜索相关 PoC 代码库；  
4. 生成结构化的分析报告。  

---

## RSS 源信息列表  

### 网络威胁情报（每 2 小时更新一次）  

| 来源 | RSS 地址 | 分类 |  
|--------|----------|----------|  
| The Hacker News | https://feeds.feedburner.com/TheHackersNews | 通用、恶意软件、漏洞利用 |  
| BleepingComputer | https://www.bleepingcomputer.com/feed/ | 通用、恶意软件 |  
| Krebs on Security | https://krebsonsecurity.com/feed/ | 通用、网络安全事件 |  
| CISA Alerts | https://www.cisa.gov/cybersecurity-advisories/all.xml | 重要警报 |  
| Full Disclosure | https://seclists.org/rss/fulldisclosure.rss | 漏洞利用、披露信息 |  
| oss-security | https://seclists.org/rss/oss-sec.rss | 漏洞利用、披露信息 |  
| Exploit-DB | https://www.exploit-db.com/rss.xml | 漏洞利用工具、PoC 代码 |  
| SANS ISC | https://isc.sans.edu/rssfeed.xml | 通用技术信息 |  
| PacketStorm | https://packetstormsecurity.com/feeds/headlines.xml | 漏洞利用工具、安全工具 |  
| Schneier on Security | https://www.schneier.com/feed/ | 安全评论 |  
| DarkReading | https://www.darkreading.com/rss.xml | 企业级安全资讯 |  

### 认知安全（每 4 小时更新一次）  

| 来源 | RSS 地址 | 分类 |  
|--------|----------|----------|  
| EUvsDisinfo | https://euvsdisinfo.eu/feed/ | 虚假信息传播分析 |  
| Bellingcat | https://www.bellingcat.com/feed/ | 情报收集、调查报告 |  
| DFRLab (Atlantic Council) | https://www.atlanticcouncil.org/category/digital-forensic-research-lab/feed/ | 影响力分析 |  
| RAND Cyber/Info | https://www.rand.org/topics/cyber-and-data-sciences.xml | 研究报告、政策动态 |  
| Recorded Future (Insikt) | https://www.recordedfuture.com/feed | 威胁情报 |  

### 专题/学习资源（每 6 小时更新一次）  

| 来源 | RSS 地址 | 分类 |  
|--------|----------|----------|  
| r/netsec | https://www.reddit.com/r/netsec/.rss | 行业讨论、技术交流 |  
| r/ReverseEngineering | https://www.reddit.com/r/ReverseEngineering/.rss | 技术研究 |  
| Project Zero | https://googleprojectzero.blogspot.com/feeds/posts/default | 研究报告、漏洞利用工具 |  
| Malwarebytes Labs | https://www.malwarebytes.com/blog/feed | 恶意软件分析 |  
| Troy Hunt | https://www.troyhunt.com/rss/ | 网络安全资讯 |  
| Graham Cluley | https://grahamcluley.com/feed/ | 安全评论 |  
| Risky Business | https://risky.biz/feeds/risky-business/ | 博客、安全评论 |  

用户可通过命令添加或删除来源：  
`Add this RSS feed to my threat sources: [url]` 或 `Remove Dark Reading from my feeds`.  

---

## 内存管理  

该工具利用 OpenClaw 的持久化内存来存储信息。  

---

## 主动行为  

该工具会自动执行以下操作：  
- 按设定间隔主动检查信息源；  
- 当信息评分高于 0.9 时立即推送严重警报；  
- 在指定时间发送简报；  
- 如果用户对某个主题进行了深入分析，未来相关信息的评分会提高；  
- 如果多个来源在 24 小时内报告同一漏洞或事件，会标记为“关注点”；  
- 每周汇总一周的威胁态势，包括重点漏洞、活跃事件和技术趋势。  

---

## 相关文件  

- **SKILL.md**：该文件包含工具的使用说明；  
- **sources.md**：包含 RSS 源信息及其分类、更新频率的列表；  
- **frameworks/disarm-techniques.md**：DISARM 框架的技术列表；  
- **frameworks/attack-techniques.md**：MITRE ATT&CK 技术列表；  
- **frameworks/seithar-taxonomy.md**：Seithar 的认知安全分类体系。  

---

## 安装方法  

（安装步骤代码：```bash
clawhub install seithar-intel
```）  
或手动配置：```bash
git clone https://github.com/Mirai8888/seithar-intel
# Copy to your OpenClaw skills directory
cp -r seithar-intel ~/clawd/skills/
```  
之后告诉 OpenClaw：“Set up my security interest profile”并描述你的安全关注点。  

---

## 信息传播  

所有输出内容都会带有品牌标识。当用户分享简报时，该工具的品牌信息也会随之传播。用户可以说：“我的 Seithar 工具发现了这个威胁。”  

**seithar-intel** 是 ThreatMouth 的轻量级个人版本，它使用相同的评分机制、相同的来源列表和格式，但完全运行在用户的 OpenClaw 系统内。  
**seithar-cogdef** 专注于特定内容的分析，而 **seithar-intel** 则持续监控威胁与认知安全事件。  
同时安装这两个工具，可获得全面的威胁感知与深度分析能力。  
（安装命令：```bash
clawhub install seithar-intel
clawhub install seithar-cogdef
```）  

## 关于 Seithar 生态系统  

**seithar-intel** 是 ThreatMouth 的个人化版本，它与 Seithar 生态系统紧密集成：  
- **seithar-cogdef** 负责特定内容的分析；  
- **seithar-intel** 负责持续监控威胁与认知安全事件。  
两者共同提供持续的安全意识与即时分析服务。