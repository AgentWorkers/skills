---
name: osint-investigator
description: 深度开源情报（OSINT）调查：当用户需要利用公开可获取的信息来研究、查找或调查任何个人、地点、组织、用户名、域名、IP地址、电话号码、图片、车辆或物体时，可以使用此功能。该功能会在用户输入诸如“查找关于……的信息”、“进行调查”、“查询”、“这个人是谁”、“追踪这个……”、“深入调查”、“OSINT搜索”、“背景调查”等关键词时被触发。系统会通过网页搜索、社交媒体、DNS/WHOIS、图片搜索、地图、公共记录等多种渠道进行多源数据分析，并生成结构化的情报报告。
---
# OSINT调查工具

该工具支持多源开源情报收集，能够识别目标类型，并运行所有适用的模块，最终生成结构化的报告。

## 目标分类

在运行任何模块之前，先对目标进行分类：

- **个人**（真实姓名、别名、面部信息） → 可使用的模块：社交网络、网页、图像、用户名
- **用户名/昵称** → 可使用的模块：用户名、社交网络、网页
- **域名/网站** → 可使用的模块：DNS查询、WHOIS查询、网页、社交网络
- **IP地址** → 可使用的模块：IP查询、DNS查询、网页
- **组织/公司** → 可使用的模块：网页、社交网络、DNS查询、地图服务、企业信息
- **电话号码** → 可使用的模块：电话查询、网页、社交网络
- **电子邮件地址** → 可使用的模块：电子邮件查询、网页、社交网络
- **位置/地址** → 可使用的模块：地图服务、网页、社交网络、地理信息
- **图片/照片** → 可使用的模块：图片查询、反向图像搜索
- **物体/资产** → 可使用的模块：网页、图片、社交网络

请并行运行所有适用的模块。切勿在获取到一个信息源后就停止搜索。

## 模块使用指南

### 🌐 网页搜索（`web_search`工具）
针对每个目标至少执行5-8次搜索查询。请使用不同的搜索操作符：
```
"full name" site:linkedin.com
"username" -site:twitter.com
target filetype:pdf
target inurl:profile
"target" "email" OR "contact" OR "phone"
target site:reddit.com
target site:github.com
```
使用`web_fetch`工具获取顶级URL的内容。

### 🔗 DNS / WHOIS查询
```bash
whois <domain>
dig <domain> ANY
dig <domain> MX
dig <domain> TXT
nslookup <domain>
host <domain>
```
同时通过`web_fetch`工具访问：`https://rdap.org/domain/<domain>`

### 🌍 IP信息查询
```bash
curl -s https://ipinfo.io/<ip>/json
curl -s https://ip-api.com/json/<ip>
```
同时通过`web_fetch`工具访问：`https://www.shodan.io/host/<ip>`

### 📱 用户名搜索
使用`web_fetch`工具检查所有平台（只需检查HTTP状态码和页面标题，无需加载完整内容）：
- `https://github.com/<username>`
- `https://twitter.com/<username>`
- `https://instagram.com/<username>`
- `https://reddit.com/user/<username>`
- `https://tiktok.com/@<username>`
- `https://youtube.com/@<username>`
- `https://linkedin.com/in/<username>`
- `https://medium.com/@<username>`
- `https://pinterest.com/<username>`
- `https://twitch.tv/<username>`
- `https://steamcommunity.com/id/<username>`
- `https://keybase.io/<username>`
- `https://t.me/<username>`（Telegram）

### 🐦 社交媒体深入分析
对于每个确认的目标账户，使用`web_fetch`工具提取以下信息：
- 个人简介/描述
- 个人资料图片链接
- 关注者/被关注者数量
- 注册日期
- 所在地（如果有的话）
- 个人简介中的链接
- 固定发布的帖子/近期活动

对于Twitter和X平台，还可以通过`web_search`工具搜索`site:twitter.com "<target>"`以及相关的镜像链接。

### 🗺️ 地图与位置信息
```bash
# Use web_fetch or browser for:
# Google Maps search
https://maps.googleapis.com/maps/api/geocode/json?address=<address>&key=<key>
# Or use goplaces skill if available
# Streetview metadata check
https://maps.googleapis.com/maps/api/streetview/metadata?location=<lat,lng>&key=<key>
```
同时使用`web_search`工具搜索：`"<target location>" site:maps.google.com OR site:wikimapia.org OR site:openstreetmap.org`

### 🖼️ 图片搜索与反向图像搜索

**查找个人图片（如果没有提供图片）：**
1. 在所有确认的社交媒体平台上搜索个人资料图片——从页面源代码或`og:image`元标签中提取图片链接。
2. 使用`web_search`工具搜索`"<name>" site:linkedin.com`——LinkedIn的`og:image`通常会直接返回个人资料图片链接。
3. 计算可能的电子邮件地址的MD5值，并通过`https://www.gravatar.com/<md5>.json`查询头像。
4. 在新闻/媒体中搜索`"<name>" filetype:jpg OR filetype:png`。
5. 使用`web_fetch`工具从任何确认的个人资料页面中提取`og:image`。

**反向图像搜索（提供图片URL或本地文件）：**
```bash
# Direct URL-based reverse search (use web_fetch):
https://yandex.com/images/search?rpt=imageview&url=<image_url>
https://tineye.com/search?url=<image_url>

# Google Lens (requires browser tool):
https://lens.google.com/uploadbyurl?url=<image_url>

# For avatars and profile images — extract URL then feed into:
# 1. Yandex (best for face matching, indexes more than Google)
# 2. TinEye (exact match/copy detection)
# 3. Google Lens via browser tool
```

**EXIF/元数据提取（如果文件在本地）：**
```bash
exiftool <image>            # full metadata dump
exiftool -gps:all <image>   # GPS coordinates only
exiftool -DateTimeOriginal <image>  # when photo was taken
```
在线工具：`web_fetch https://www.metadata2go.com` 或 `https://www.pic2map.com`

**图片地理位置信息（如果没有EXIF GPS信息）：**
- 通过`web_search`工具搜索街道标志、商店名称、车牌等来识别位置。
- 通过`https://www.suncalc.org`根据建筑风格、植被和道路标记来估计地理位置。
- 使用浏览器工具与Google Street View进行交叉验证。

**通过社交媒体图片查找个人时：**
1. 使用`web_fetch`工具获取个人资料页面，并查找页面渲染后的`og:image`或`<img>`标签。
2. 提取完整的CDN图片链接。
3. 将图片链接输入Yandex ImageView和TinEye工具进行分析。

### 📧 电子邮件信息查询
```bash
# Breach/exposure check
curl -s "https://haveibeenpwned.com/api/v3/breachedaccount/<email>" -H "hibp-api-key: <key>"
# Format validation + domain MX check
dig $(echo <email> | cut -d@ -f2) MX
# Gravatar (hashed MD5 of email)
curl -s "https://www.gravatar.com/<md5_hash>.json"
```
同时使用`web_search`工具搜索`"<email>" site:pastebin.com OR site:ghostbin.com`。

### 📞 电话信息查询
```bash
# Carrier / region lookup
curl -s "https://phonevalidation.abstractapi.com/v1/?api_key=<key>&phone=<number>"
```
同时使用`web_search`工具搜索`"<phone_number>"`，并检查`site:truecaller.com`和`site:whitepages.com`。

### 🏢 企业/组织信息查询
使用`web_fetch`工具查询：
- `https://opencorporates.com/companies?q=<name>`
- 英国公司注册信息：`https://find-and-update.company-information.service.gov.uk/search?q=<name>`
- LinkedIn公司页面：`https://linkedin.com/company/<slug>`
- Crunchbase：`web_search`查询`site:crunchbase.com "<company>"`

### 📄 文档与数据泄露查询
```bash
web_search queries:
"<target>" filetype:pdf OR filetype:xlsx OR filetype:docx
"<target>" site:pastebin.com
"<target>" site:github.com password OR secret OR key
"<target>" site:trello.com OR site:notion.so
```

### 🔍 缓存与归档
```bash
# Wayback Machine
curl -s "https://archive.org/wayback/available?url=<url>"
web_fetch "https://web.archive.org/web/*/<url>" for snapshots
# Google Cache via web_search: cache:<url>
```

## 调查工作流程

1. **对目标类型进行分类**
2. **制定计划**——列出所有需要运行的模块
3. **并行执行**所有模块（尽可能使用多个工具）
4. **关联信息**——跨来源对比结果，注意数据的一致性和矛盾之处
5. **生成报告**——输出结构化报告（详见下文）

## 报告格式

必须生成结构化的报告。根据实际收集到的信息调整报告内容：

```
# OSINT Report: <Target>
**Date:** <UTC timestamp>
**Target Type:** <classification>
**Query:** <original user request>

## Identity Summary
[Key identifying information — name, aliases, age, location, nationality]

## Online Presence
[Confirmed profiles with URLs, follower counts, activity level]

## Contact & Technical
[Email addresses, phone numbers, domains, IPs]

## Location Intelligence
[Known locations, addresses, coordinates, map links]

## Corporate / Organisational Links
[Companies, roles, affiliations]

## Historical Data
[Archived content, old usernames, past locations]

## Document & Data Exposure
[Public documents, paste sites, leak mentions]

## Image Intelligence
[Profile photos, reverse image results, photo metadata]

## Confidence & Gaps
[Confidence level per finding — High/Medium/Low; list gaps]

## Sources
[All URLs consulted]
```

## 配置与认证

配置信息存储在：`<skill_dir>/config/osint_config.json`（权限设置为600，首次保存时会自动生成）。

用户可以通过对话方式配置所有设置——无需编写终端脚本。当用户需要添加凭证、设置PDF输出格式或API密钥时，请按照以下流程操作。

### 对话式配置流程

当用户需要配置该工具时，直接在聊天中询问他们的需求，然后使用`write`工具将答案写入配置文件。

**步骤1 — 询问配置内容：**
> “您想设置什么？我可以配置以下内容：
> - 平台凭证（Instagram、Twitter/X、LinkedIn、Facebook）
> - API密钥（Google Maps、Shodan、HaveIBeenPwned、Hunter.io、AbstractAPI Phone）
- PDF报告输出（是否启用、是否保存位置信息）”

**步骤2 — 收集配置信息**（一次配置一个平台）：
- 对于API密钥：让用户在聊天中直接输入密钥。
- 对于密码：提醒用户信息会被保存在本地JSON文件中。
- 对于输出设置：询问用户是否需要保存报告，并提供保存路径。

**步骤3 — 编写配置文件：**
```python
# Read existing config (or start fresh)
import json, os
cfg_path = "<skill_dir>/config/osint_config.json"
os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {"platforms": {}, "output": {}}

# Example: save Twitter bearer token
cfg["platforms"]["twitter"] = {"configured": True, "method": "api_key", "bearer_token": "<VALUE>"}

# Example: enable PDF
cfg["output"]["pdf_enabled"] = True
cfg["output"]["pdf_output_dir"] = "~/Desktop"

# Write back
with open(cfg_path, "w") as f:
    json.dump(cfg, f, indent=2)
os.chmod(cfg_path, 0o600)
```
直接使用`write`工具进行配置——无需运行Python脚本。

### 支持的平台集成

| 平台 | 需要收集的字段 | 可获取的信息 |
|----------|--------|-----------------|
| Instagram | `username`, `password` | 登录后的个人资料内容（建议使用临时账户） |
| Twitter/X | `bearer_token`（可选 `api_key`, `api_secret`） | 通过API v2获取完整推文/个人资料/搜索信息（免费 tier可用） |
| LinkedIn | `username`（电子邮件）、`password` | 个人资料信息（请谨慎使用，因使用频率有限制） |
| Facebook | `email`, `password` | 公开个人资料/群组信息 |
| Google Maps | `api_key` | 地理编码、地点搜索、街景信息 |
| Shodan | `api_key` | 深度IP/主机信息查询 |
| HaveIBeenPwned | `api_key` | 电子邮件泄露查询（每月费用3.95美元） |
| Hunter.io | `api_key` | 通过域名查询电子邮件信息（每月25次查询） |
| AbstractAPI Phone | `api_key` | 电话运营商/地区查询（app.abstractapi.com/api/phone-validation） |

### 在搜索过程中读取凭证信息
```bash
# Read config and extract a value in one line:
BEARER=$(python3 -c "import json; c=json.load(open('<skill_dir>/config/osint_config.json')); print(c['platforms']['twitter']['bearer_token'])")

# Then use it:
curl -s -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/users/by/username/<handle>?user.fields=description,location,created_at,public_metrics"
```

### Twitter/X API v2（配置完成后）
```bash
# Profile lookup
curl -s -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/users/by/username/<handle>?user.fields=description,location,created_at,public_metrics,entities"

# Recent tweets
curl -s -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/users/<user_id>/tweets?max_results=10&tweet.fields=created_at,geo,entities"

# Search recent tweets
curl -s -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/tweets/search/recent?query=<query>&max_results=10"
```

### Shodan API（配置完成后）
```bash
curl -s "https://api.shodan.io/shodan/host/<ip>?key=$SHODAN_KEY"
curl -s "https://api.shodan.io/dns/resolve?hostnames=<domain>&key=$SHODAN_KEY"
```

### Hunter.io API（配置完成后）
```bash
curl -s "https://api.hunter.io/v2/domain-search?domain=<domain>&api_key=$HUNTER_KEY"
curl -s "https://api.hunter.io/v2/email-verifier?email=<email>&api_key=$HUNTER_KEY"
```

### HaveIBeenPwned API（配置完成后）
```bash
curl -s "https://haveibeenpwned.com/api/v3/breachedaccount/<email>" \
  -H "hibp-api-key: $HIBP_KEY" -H "User-Agent: osint-investigator"
```

### Google Maps API（配置完成后）
```bash
curl -s "https://maps.googleapis.com/maps/api/geocode/json?address=<address>&key=$GMAPS_KEY"
curl -s "https://maps.googleapis.com/maps/api/place/textsearch/json?query=<query>&key=$GMAPS_KEY"
curl -s "https://maps.googleapis.com/maps/api/streetview/metadata?location=<lat,lng>&key=$GMAPS_KEY"
```

## PDF报告生成

### 检查PDF功能是否启用
```bash
python3 -c "import json; c=json.load(open('<skill_dir>/config/osint_config.json')); print(c.get('output',{}).get('pdf_enabled', False))"
```

### 生成PDF报告
将Markdown报告写入临时文件，然后运行shell脚本（如果`fpdf2`未安装，则会自动安装）：
```bash
cat > /tmp/osint_report.md << 'ENDREPORT'
<full markdown report>
ENDREPORT

bash <skill_dir>/scripts/generate_pdf.sh \
  --input /tmp/osint_report.md \
  --target "Target Name" \
  --output ~/Desktop
```

该脚本会：
1. 检查是否安装了`fpdf2`——如果未安装则自动安装。
2. 使用相同的参数调用`generate_pdf.py`。
3. 打印输出路径：`PDF保存路径：/path/to/OSINT_Name_20260225_1035.pdf`

**用户无需进行任何额外设置**——该工具支持任何安装了Python 3和pip的机器。

### PDF报告的色彩编码
报告中的颜色编码会根据内容的可靠性自动生成：
- 🟢 **绿色** `[HIGH]` — 来自多个可靠来源的验证信息
- 🟠 **橙色** `[MED]` — 可能正确，但来源单一或未经验证
- 🔴 **红色** `[LOW]** — 可能匹配，但证据不足
- ⚪ **灰色** `[UNVERIFIED]** — 用户提供的数据，未经独立验证

### 通过对话切换PDF输出功能
当用户请求“启用PDF报告”或“禁用PDF输出”时：
1. 读取配置文件。
2. 将`cfg["output"]["pdf_enabled"]`设置为`true`或`false`。
3. 将设置更新后写回配置文件。
4. 通知用户设置结果。

## 道德与合法性准则

- 仅使用公开可获取的数据——严禁尝试访问私人系统。
- 不得以任何可能用于跟踪或骚扰的方式整合数据。
- 遵守robots.txt协议；在直接爬取被禁止的情况下使用缓存/归档版本。
- 如果调查对象是未经同意的私人个体，请在继续操作前明确标注。
- 对于Instagram/LinkedIn/Facebook的凭证信息，建议使用临时账户，切勿使用用户的个人账户。

## 参考文件

- `references/osint-sources.md` — 按类别整理的OSINT数据库、API和搜索工具
- `references/social-platforms.md` — 各平台特定的数据提取技巧和URL模式
- `scripts/generate_pdf.py` — PDF生成工具（需要`fpdf2`，通过shell脚本自动安装）
- `scripts/generate_pdf.sh` — shell脚本；用于安装`fpdf2`并调用`generate_pdf.py`
- `config/osint_config.json` — 实时配置文件（首次保存时会自动生成，权限设置为600）