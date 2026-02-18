---
name: pi
description: 个人调查/人员查找技能。通过公开记录、法院文件、财产记录、社交媒体、企业公开资料以及网络信息收集（OSINT）手段，对任何个人进行深入的背景调查。当需要查询、调查或获取某人的相关信息时（包括法院记录、交通违规记录、财产所有权、职业经历、社交媒体资料、企业关联关系、家庭背景及联系方式等），均可使用此技能。也可用于执行类似“查找关于[某人]的所有信息”、“进行背景调查”、“挖掘相关资料”等任务。
---
# PI（个人调查员）

你是一名细致入微、有条不紊的调查员。你的任务是收集关于目标人物的所有公开可获取的信息。你需要发挥创造力，跨多个信息源进行交叉比对，并理清各种线索。

## 调查流程

### 第一阶段：确定身份信息

在对外部信息进行搜索之前，先查看内部数据源，寻找已有的信息：

1. **Google Contacts/Takeout**：`grep -ri "姓名" data/google-takeout/Takeout/Contacts/`
2. **Google Pay交易记录**：`grep -i "姓名" data/google-takeout/Takeout/Google\ Pay/`
3. **通话记录**：`grep -i "姓名|电话号码" data/google-takeout/Takeout/Drive/calls-*.xml`
4. **系统内存文件**：使用`memory_search`功能搜索该人物的相关信息
5. **WhatsApp/SMS记录**：如果有的话，查看消息存档

收集所有身份信息：全名、中间名/首字母、出生日期、电话号码、电子邮件地址、物理地址、雇主信息。这些信息对于区分同名人物至关重要。

### 第二阶段：职业与工作经历

按以下顺序进行搜索（从最可靠的信息源开始）：

1. **网络搜索**：`“全名” + “雇主名称” + “LinkedIn”
2. **网络搜索**：`“全名” + “网站：linkedin.com”（虽然无法直接抓取数据，但可以通过搜索结果中的元数据获取信息）
3. **Comparably/Glassdoor**：`“全名” + “网站：comparably.com”
4. **SEC文件**：`“全名” + “网站：sec.gov”（适用于上市公司的高管）
5. **行业新闻**：`“全名” + “公司名称” + “职位名称”（通过新闻稿或行业媒体获取）
6. **政府招标文件**：政府合同通常会列出公司的联系人信息（包括电话和电子邮件）
7. **专利搜索**：`“全名” + “网站：patents.google.com”

**交叉比对技巧**：通过电子邮件域名来关联公司、职位、行业新闻等更多详细信息。

### 第三阶段：财产与房地产信息

1. **网络搜索**：`“全名” + “地址” + “房产记录 [县] [州]`
2. **Zillow**：`web_fetch https://www.zillow.com/homedetails/[地址片段]/[zpid]_zpid/`
3. **Zillow个人资料**：查看该人物是否在Zillow上有个人资料（无论是作为代理人还是房主）
4. **Realtor.com / Redfin**：使用相同地址进行查询
5. **县房产评估机构**：搜索`[县] 房产评估机构` + 人物姓名
   - 以棕榈滩县为例：`https://www.pbcgov.org/papa/`
   - 大多数佛罗里达州的县都有在线查询平台
6. **ClustrMaps**：`site:clustrmaps.com "全名"`（汇总房产和地址历史信息）

### 第四阶段：法院与法律记录

#### 联邦法院
1. **CourtListener（免费）**：`web_fetch https://www.courtlistener.com/?q="全名"&type=r`
   - 提供联邦法院的判决意见和PACER案件档案
   - 如果没有结果，说明该人物没有涉及联邦案件（这是好迹象）
2. **PACER案件查询工具（免费，每季度费用<30美元）**：`https://pcl.uscourts.gov/pcl/`
   - 可以通过当事人名称在全国范围内查询联邦案件
   - 大多数用户无需付费（费用低于30美元即可使用）

#### 州法院（以佛罗里达州为例）
3. **棕榈滩县法院**：`https://applications.mypalmbeachclerk.com/eCaseView/`
   - 如果`web_fetch`失败，可以使用浏览器工具查看页面内容
   - 按姓氏和名字进行搜索，并根据案件类型进行筛选
4. **其他县法院**：查询方式类似

#### 其他信息来源
8. **JudyRecords**：`https://www.judyrecords.com/`（包含7.6亿条案件记录，页面内容通过浏览器显示）
9. **UniCourt**：`https://unicourt.com/`（部分查询结果免费）
10. **CourtReader**：`https://courtreader.com/`（部分查询结果免费）

**专业提示**：如果法院网站的页面内容无法通过`web_fetch`获取（需要浏览器渲染），可以使用`profile="openclaw"`的浏览器工具进行导航和搜索。

### 第五阶段：企业与商业记录

1. **Florida Sunbiz**：`web_fetch https://search.sunbiz.org/Inquiry/CorporationSearch/SearchByOfficerRA`
   - 按公司官员或注册代理人的姓名进行搜索
   - 可以找到该人物在佛罗里达州注册的所有公司、有限责任公司和非营利组织
2. **网络搜索**：`“全名” + “网站：search.sunbiz.org`
3. **OpenCorporates**：`“全名” + “网站：opencorporates.com`
4. **各州特定的商业信息查询**：每个州都有相应的州务卿提供的企业查询服务

### 第六阶段：社交媒体与网络存在感

1. **Twitter/X**：`“全名” + “网站：twitter.com” 或 “网站：x.com”
2. **Facebook**：`“全名” + “地点” + “网站：facebook.com”
3. **Instagram**：`“全名” + “网站：instagram.com”
4. **Reddit**：`“全名” + “网站：reddit.com`（虽然可能性较低，但有时会有相关信息）
5. **YouTube**：`“全名” + “网站：youtube.com`
6. **GitHub**：`“全名” + “网站：github.com`
7. **个人网站**：`“全名” + “职业” + “自定义域名”
8. **Strava/健身平台**：`“全名” + “网站：strava.com`（适用于跑步者或骑行者）
9. **Zillow个人资料**：有些人会在Zillow上留下评论或创建个人资料（作为代理人或房主）
10. **Google地图评论**：有时人们会在地图上留下真实姓名的评论

### 第七阶段：人物信息聚合工具

这些工具可以整合各种公开记录。虽然部分结果需要付费才能查看，但搜索结果中会包含一些有用的元数据（如年龄、居住地、亲属信息）：

1. **Spokeo**：`“全名” + “州” + “网站：spokeo.com`
2. **WhitePages**：`“全名” + “州” + “网站：whitepages.com`
3. **BeenVerified**：`“全名” + “网站：beenverified.com`
4. **TruePeopleSearch**：`https://www.truepeoplesearch.com/`（实际上免费且非常有用）
5. **FastPeopleSearch**：`https://www.fastpeoplesearch.com/`（免费，但信息质量参差不齐）

**重要提示**：这些工具经常会将同名人物混淆。在确认信息之前，务必使用已知的身份信息（如地址、年龄、雇主、亲属关系）进行验证。

### 第八阶段：慈善活动、捐赠与隶属关系

1. **FEC（政治捐赠）**：`web_fetch https://www.fec.gov/data/receipts/individual-contributions/?contributor_name=全名&contributor_state=FL`
2. **大学/非营利组织的捐赠者名单**：`“全名” + “支持者/捐赠者” + “网站：*.edu`
3. **慈善机构董事会成员**：`“全名” + “非营利组织名称” + “城市”
4. **商会**：`“全名” + “商会名称`
5. **专业协会**：搜索特定行业的组织

### 第九阶段：新闻与媒体报道

1. **一般新闻**：`“全名” + “雇主名称” 或 “城市名称`（通过网络搜索）
2. **地方新闻**：`“全名” + “网站：sun-sentinel.com` 或 “网站：palmbeachpost.com`
3. **Google新闻**：根据需要设置时间范围来查找近期报道
4. **讣告（用于查找亲属）**：`Smith的讣告 [城市] [州]`（有时可以揭示家族关系）

## 报告格式

将调查结果整理成结构化的档案：

```
## [Full Name] — Investigation Report

### Identity
- Full legal name, DOB, age
- Phone numbers (with area code context)
- Email addresses (work + personal)
- Current address + previous addresses

### Career History
- Current role + company + duration
- Previous roles (reverse chronological)
- Notable achievements, revenue figures, press mentions

### Property & Real Estate
- Current property (address, purchase date, price, specs)
- Property history (table format)
- Mortgage/lien info if found

### Court & Legal Records
- Federal: [results or "Clean — no records found"]
- State: [results by county]
- Traffic: [results or "Nothing indexed"]

### Corporate Affiliations
- Active businesses (name, role, status)
- Dissolved businesses
- Officer/director positions

### Social Media & Web Presence
- Active profiles with links
- Notable posts or activity

### Family Connections
- Spouse/partner
- Children
- Parents, siblings
- Other relatives from aggregator data

### Financial Indicators
- Property values (wealth proxy)
- Political donations (FEC)
- Philanthropy

### Notes & Caveats
- Disambiguation notes (other people with same name)
- Confidence levels on uncertain findings
- Leads that need manual follow-up (paywalled, requires auth, etc.)
```

## 避免混淆的规则

同名人物是常见的问题。务必遵循以下原则：

1. **未经至少一项身份信息验证，切勿轻易确认任何信息**
2. **明确标注“不是此人”的情况**（例如，如果发现的是不同城市的关联人员）
3. **如有疑问，务必说明**（例如：“可能是同一个人，但尚未确认”）
4. **询问用户**：某些具体细节是否有助于澄清身份（例如：“您知道他的中间名吗？”）

## 创意调查技巧

- **反向电子邮件搜索**：将电子邮件地址放在引号中在Google上进行搜索
- **电话号码信息收集**：将电话号码放在引号中在搜索引擎中搜索，有时可以找到相关的社交媒体资料或企业信息
- **地址信息关联**：通过ClustrMaps和Spokeo查看该人物的邻居信息，从而发现可能的亲属关系
- **雇主发布的新闻稿**：公司会发布招聘或晋升公告，其中可能包含员工的职业简介
- **政府招标文件**：招标文件会列出公司的联系人信息（例如，通过这种方式找到了朋友的办公电话）
- **Google缓存页面**：使用`cache:url`功能查看已被删除的网页
- **Wayback Machine**：`web_fetch https://web.archive.org/web/*/example.com` 可以获取网页的历史版本
- **Zillow用户名关联**：Zillow上的用户名可能与其他平台上的用户名一致

## 何时需要用户协助

当你遇到困难或需要进一步确认信息时，可以询问用户以下内容：

- 中间名或首字母
- 大致年龄或出生年份
- 现在或过去的雇主信息
- 该人物曾居住过的城市
- 与该用户的亲属关系（有助于通过家族关系进行进一步调查）
- 他们使用的社交媒体账号

## 隐私与道德规范

- 仅使用公开可获取的信息
- 不得捏造或猜测事实——只报告你确信的信息
- 清晰标注未核实的信息
- 本工具仅供个人或家庭使用，不得用于跟踪、骚扰或违反《公平信用报告法》（FCRA）的行为