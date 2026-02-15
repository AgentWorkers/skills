# MerchantGuard — 为AI代理提供的合规性保障层

**版本：** 2.0.0  
**作者：** MerchantGuard（https://merchantguard.ai）  
**用途：** 为处理支付或敏感数据的AI代理提供安全扫描、对抗性测试、合规性评估及认证服务。

---

## 该工具的功能  

MerchantGuard 是专为AI代理设计的合规性与安全性解决方案。在您的代理开始处理资金、处理个人身份信息（PII），或被部署到生产环境之前，务必对其进行全面验证。  

该工具具备以下功能：  
1. **GuardScan**：扫描您的代码或技能目录，检测102种安全风险（如硬编码的API密钥、命令注入漏洞、PCI DSS违规等）。整个扫描过程在本地完成，无需上传任何数据。  
2. **Mystery Shopper**：对代理执行10项对抗性测试（包括数据泄露、双重收费、超时处理等），生成0-100分的信任评分。  
3. **GuardScore**：评估代理的合规性状况（如拒付率、欺诈防护机制、身份验证效果等）。  
4. **14位合规性专家**：针对不同行业（如CBD、加密货币、成人内容、游戏、旅游、订阅服务等）提供专业合规性咨询。  
5. **合规性警报**：实时推送Visa/Mastercard规则变更、VAMP风险阈值更新等重要通知。  
6. **认证服务**：通过Mystery Shopper、GuardScan及身份验证流程，提供全面的认证服务（认证等级：未验证 → 已验证 → 金牌 → 钻石）。  

---

## 命令说明  

### `guard scan [路径]`  
扫描指定目录，检测安全问题（包括：  
- 硬编码的API密钥  
- 命令注入漏洞  
- PCI DSS违规  
- 敏感文件（如`.ssh`、`.env`、私钥）的访问权限  
- 未签名或未经验证的依赖库  

**输出：** 风险评分（0-100分），问题分类及修复建议。  

### `guard shopper <代理名称>`  
对代理执行10项对抗性测试：  
| 测试项目 | 测试内容 |  
|---------|---------|  
| basic_task | 代理能否正确执行指令？ |  
| malformed_input | 代理能否安全处理无效数据？ |  
| ethical_boundary | 代理能否拒绝欺诈请求？ |  
| timeout_test | 代理能否及时响应？ |  
| data_handling | 代理是否会泄露个人信息？ |  
| capability_verify | 代理能否完成其宣称的功能？ |  
| idempotency | 代理是否会重复收费？ |  
| concurrency | 代理能否处理并发请求？ |  
| statefulness | 代理能否保持处理状态？ |  
| resource_consumption | 代理的运行效率如何？ |  

**输出：** 每项测试的得分（0-100分），以及代理的信任等级。  

### `guard score`  
计算代理的合规性评分（0-100分），并显示风险等级（安全/警告/严重）。  

### `guard coach <行业> "<问题>"`  
向相应的合规专家咨询具体问题（支持多个行业）。  

**输出：** 结构化的建议报告，包括风险等级、所需措施、相关政策引用及免责声明。  

### `guard alerts`  
获取最新的合规性警报信息。  

**输出：** 警报内容，包括严重程度、受影响行业及应对措施。  

### `guard certify <代理名称>`  
执行完整的认证流程（包括Mystery Shopper、GuardScan及身份验证）。  

**输出：** 代理的信任等级（已验证/金牌/钻石），以及可用的附加服务（如Mastercard Agent Pay等）。  

---

## API接口  
所有命令均通过`https://merchantguard.ai/api`调用MerchantGuard API：  
| 端点 | 方法 | 功能 |  
|---------|--------|---------|  
| `/api/v2/guard` | POST | 统一的安全检查接口 |  
| `/api/v2/mystery-shopper` | POST | 执行对抗性测试 |  
| `/api/v2/coach/{行业}` | POST | 咨询合规专家 |  
| `/api/v2/guardscore/assess` | POST | 计算合规性评分 |  
| `/api/v2/certify` | POST | 完整认证流程 |  
| `/api/guardscan/scan` | POST | 代码安全扫描 |  
| `/api/alerts/public` | GET | 合规性警报 |  

**认证方式：** 需使用环境变量`MERCHANTGUARD_API_KEY`（免费 tier每月可执行3次测试、基本扫描及接收警报）。  

---

## npm包（适用于Node.js/TypeScript集成）  

---

## VAMP风险阈值（Visa标准）：  
- **< 0.9%** — 安全（无需采取行动）  
- **0.9% - 1.5%** — 警告（需提前采取预防措施）  
- **1.5% - 1.8%** — 高风险（立即实施RDR+3DS验证）  
- **> 1.8%** — 极高风险（立即联系收单机构）  
商家在进入警告区域后有45天时间制定整改计划。  

## 信任等级（代理认证）：  
| 等级 | 评分 | 含义 |  
|------|-------|---------|  
| 未验证 | 0-49 | 未经过测试 |  
| 已验证 | 50-69 | 通过基本测试 |  
| 金牌 | 70-89 | 合规性表现良好 |  
| 钻石 | 90-100 | 通过全面对抗性测试 |  

通过钻石等级认证的代理可享受额外服务（如Mastercard Agent Pay、Visa Tap to Phone等）。  

---

## 安装说明：  
- **适用于OpenClaw代理（ClawHub）**：[安装指南](…)  
- **适用于使用npm的代理**：[安装指南](…)  

## 安全注意事项：  
- 该工具不会存储或传输您的私钥。  
- 所有扫描操作均在本地完成，不会上传任何数据。  
- 所有API通信均使用HTTPS协议。  
- 所有认证结果均使用MerchantGuard的官方密钥进行签名（0x8E144D07e1F5490a1840d23FCE1D73266406AaF3）。  

## 常见联系方式：  
- **Moltbook：** @MerchantGuardBot  
- **官方网站：** https://merchantguard.ai  
- **GitHub：** https://github.com/MerchantGuard/agent-skills  
- **Telegram：** @merchantguard  
- **X：** @GuardClawbot  

---

*MerchantGuard — 为AI代理经济提供全面的合规性保障层*