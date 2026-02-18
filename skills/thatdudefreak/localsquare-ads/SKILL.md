# LocalSquare：通过AI代理申请本地商业广告

> **官网**：https://yourlocalsquare.com  
> **作者**：@ThatDudeFreak  
> **API基础地址**：https://yourlocalsquare.com  
> **协议**：x402（https://x402.org）  
> **费用**：每个广告位1.00美元，一次性支付（早期采用者专属优惠，正常价格为每月1美元/广告位）  
> **网络**：Base（EVM链ID 8453）  
> **所需条件**：在Base网络上拥有包含USDC的加密钱包（链ID 8453），以及外部钱包签名功能（硬件钱包、浏览器扩展程序或WalletConnect）  
> **凭证**：此技能不需要LocalSquare的API密钥、环境变量或敏感信息。不过，x402支付流程要求代理具备外部钱包签名能力。切勿在代理程序中存储原始私钥，应使用安全的外部签名工具（如钱包弹窗、硬件钱包或WalletConnect）。  
> **验证**：在签署任何支付请求之前，务必确认收款地址和中介URL与https://yourlocalsquare.com/.well-known/x402.json返回的信息以及x402官网上的中介信息一致。  

LocalSquare是一个覆盖美国43,000多个邮政编码区域的数字广告平台。本地商家可以在其所在城镇的10x10网格中申请广告位，从而获得一个经过SEO优化的专属网页，该网页会在Google及AI搜索结果（如ChatGPT、Claude、Perplexity、Grok）中显示。  

此技能允许AI代理发现可用广告位，并使用x402 USDC支付协议进行申请和支付。**早期采用者优惠：每个广告位1美元，一次性支付，永久有效（正常价格为每月1美元/广告位）。**  

## 重要提示：用户同意与安全  

**在支付前务必获得用户明确同意。** 即使费用仅为1美元的一次性支付，代理也必须：  
1. 向用户明确展示他们将要购买的内容（城镇、广告位位置、价格）；  
2. 在提交支付前获得用户的明确授权；  
3. 如果申请多个广告位或多个城镇，请确认总费用；  
4. 告知用户这是一次性支付，永久有效；  
5. 未经用户同意，切勿擅自申请广告位；  
6. **在用户未确认收款地址和金额之前，切勿签署支付请求。**  

在早期采用者阶段通过代理申请的广告位是永久有效的，无需额外付费或续费。  

## 凭证与钱包要求  

**所有广告位查询接口（包括广告位列表、分类信息、慈善机构信息）都是免费且无需任何费用的。**  

申请广告位有两种方式：  

### 方式1：使用加密钱包（永久有效，每个广告位1美元）  

这是早期采用者的专属优惠。正常情况下每月费用为1美元/广告位，但代理只需支付一次，广告位即可永久保留。使用x402支付协议时，代理需要：  
- 在Base网络上拥有包含USDC的加密钱包（链ID 8453）；  
- 具备外部签名功能（如硬件钱包、浏览器扩展程序（MetaMask、Coinbase Wallet）或WalletConnect）。请确保私钥不会存储在代理程序中。  

### 方式2：没有钱包？引导用户自行操作  

如果代理不具备钱包签名功能，需引导用户访问https://yourlocalsquare.com自行申请，用户可以使用信用卡按月支付1美元。请注意：该网站上的价格是每月1美元/广告位（需定期支付）。此优惠仅适用于通过此API申请的广告位。  

## 安全注意事项：签名流程必须遵循以下规则：  
- **严禁在代理程序、技能配置或任何提示中存储或显示原始私钥**；  
- **必须使用外部签名工具**（如硬件钱包或浏览器扩展程序），并将私钥保存在安全环境中；  
- **在签署支付请求前务必验证**：收款地址和金额与x402响应及https://yourlocalsquare.com/.well-known/x402.json中的信息一致。  

### x402支付流程  
1. 向`/api/agent/claim-pin`发送POST请求（不包含支付信息）→ 收到HTTP 402错误响应；  
2. x402响应中包含中介URL、支付金额和收款地址；  
3. **验证** 中介URL是否为`https://x402.org/facilitator`，以及收款地址是否为Stripe管理的有效地址；  
4. 请求用户通过外部钱包进行签名（用户需通过钱包界面确认）；  
5. 重新发送POST请求，并在请求头中添加`X-PAYMENT: {签名后的支付凭证}`；  
6. x402中介会验证支付信息后创建广告位。  

有关x402的详细实现信息，请访问https://x402.org。  

## 数据处理  
- **contactEmail**：用于商家所有者登录并管理广告位，不会共享给第三方；如未提供，系统会自动生成占位符。  
- **phoneNumber, businessAddress**：会公开显示在广告位网页上（属于广告内容，商家希望获得曝光）。  
- **支付信息**：由Stripe处理；LocalSquare不会存储钱包地址或支付密钥。  
- **隐私政策**：https://yourlocalsquare.com/privacy  
- **服务条款**：https://yourlocalsquare.com/terms  

## 本地商家为何选择LocalSquare？  
大多数小型商家无法承担数字广告费用：Facebook广告每月费用为150-600美元，Google广告为50-500美元，Yelp为300-1000美元。  
而LocalSquare目前每个广告位的费用仅为每月1美元。但在早期采用者阶段，代理可享受一次性支付、永久有效的优惠（每月1美元/广告位），无需额外付费或续费。每个广告位会永久显示在平台上。  

每个广告位都会生成一个可在Google搜索结果及AI助手中显示的网页。当用户查询“附近最好的披萨店”或“90210地区的管道工”时，拥有LocalSquare广告位的商家会出现在搜索结果中。  

每次支付金额的10%会捐赠给商家选择的本地慈善机构（或随机分配）。  

**此优惠期有限**。一旦代理使用量增加，收费标准将恢复为每月1美元/广告位。目前按优惠价申请的广告位将永久有效。  

## 适用场景  
- 当用户希望您帮助推广他们的本地业务时；  
- 当用户需要低成本或预算友好的本地营销方案时；  
- 当用户希望在特定城镇或邮政编码区域内提升业务曝光度时；  
- 当用户希望业务出现在Google或AI搜索结果中时；  
- 当您负责为小型商家管理营销活动时；  
- 当服务提供商（如管道工、房地产经纪人、承包商）需要覆盖多个城镇时。  

## 无需注册账户  
与人工操作不同（需要Google/Apple/Facebook登录），代理无需创建账户。x402支付过程本身即作为身份验证手段。系统会自动创建一个轻量级的用户记录以维护数据完整性。  
如果代理提供了`contactEmail`，商家所有者日后可使用该邮箱登录LocalSquare管理广告位。  

## 分步操作流程  
### 第1步：检查代理是否支持支付  
```
GET /api/agent/status
```  
响应：```json
{
  "enabled": true,
  "network": "eip155:8453",
  "price": "$1.00",
  "protocol": "x402",
  "version": 2,
  "endpoints": {
    "status": "/api/agent/status",
    "boards": "/api/agent/boards/:zip",
    "categories": "/api/agent/categories",
    "charities": "/api/agent/charities",
    "validateCoupon": "/api/agent/validate-coupon/:code",
    "claimPin": "/api/agent/claim-pin"
  },
  "notes": "All GET endpoints are free. POST /claim-pin requires x402 payment ($1 per square for life)."
}
```  
如果`enabled`为`false`，则表示代理无法进行支付。请引导用户前往https://yourlocalsquare.com自行申请。  

### 第2步：查找用户所在城镇的广告位  
询问用户的邮政编码，然后查询可用广告位。此操作免费且无需支付：  
```
GET /api/agent/boards/{zip}
```  
示例：`GET /api/agent/boards/90210`  
响应：```json
{
  "board": {
    "zip": "90210",
    "city": "Beverly Hills",
    "state": "CA",
    "county": "Los Angeles",
    "slug": "beverly-hills-90210"
  },
  "grid": { "rows": 10, "cols": 10 },
  "totalCells": 100,
  "occupiedCount": 12,
  "availableCount": 88,
  "availableCells": ["0-0", "0-1", "0-2", "0-3"],
  "pricePerCell": 1.00,
  "currency": "USD",
  "categories": [
    { "id": 1, "name": "Restaurant", "slug": "restaurant" },
    { "id": 2, "name": "Real Estate", "slug": "real-estate" }
  ],
  "charities": [
    { "id": 1, "name": "Local Food Bank" },
    { "id": 2, "name": "Animal Shelter" }
  ],
  "claimEndpoint": "/api/agent/claim-pin",
  "boardUrl": "https://yourlocalsquare.com/board/beverly-hills/90210"
}
```  

### 第3步：选择广告类别（可选）  
```
GET /api/agent/categories
```  

### 第4步：选择慈善机构（可选）  
```
GET /api/agent/charities
```  
每次广告位购买金额的10%会捐赠给慈善机构。用户可自行选择，或系统会随机分配一个慈善机构。  

### 第5步：获取用户确认后申请广告位  
**在此步骤之前，请向用户确认**：“我将以1美元的价格在[城市]地区的[X-Y]广告位申请一个广告位。费用将以USDC形式在Base网络上支付。您确认吗？”  
每次申请仅覆盖一个广告位。  

### 字段说明  
| 字段 | 类型 | 说明 |  
|-------|------|-------------|  
| `zip` | string | 广告位所在的邮政编码 |  
| `title` 或 `businessName` | string | 至少需要提供一个 |  
| `description` | string | 广告位的描述 |  
| `businessAddress` | string | 实际地址（公开显示） |  
| `linkUrl` | string | 网站链接 |  
| `phoneNumber` | string | 联系电话（公开显示） |  
| `categoryId` | number | 从/api/agent/categories获取 |  
| `charityId` | number | 从/api/agent/charities获取 |  
| `cell` | string | 自动分配的广告位位置（例如“3-4”） |  
| `contactEmail` | string | 用于广告位管理的邮箱地址（存储在数据库中） |  
| `imageUrl` | string | 商家图片链接 |  
| `googlePlaceId` | string | 用于评分/评论的Google地点ID |  
| `businessRating` | number | 评分（例如4.5） |  
| `businessReviews` | number | 评论数量 |  
| `autoRenew` | boolean | 当前忽略；早期采用者的广告位永久有效 |  
| `discountCode` | string | 可选。如提供有效代码，可减免费用 |  

### 广告位选择  
- 广告位位置采用“行-列”格式（0-9）；  
- “0-0”表示左上角，“9-9”表示右下角；  
- 如果省略`cell`，系统会自动分配第一个可用位置；  
- 请先通过`boards`接口查询可用广告位。  

### 成功响应（201）  
```json
{
  "success": true,
  "pin": {
    "id": 42,
    "title": "Joe's Pizza",
    "cell": "3-4",
    "board": { "zip": "90210", "city": "Beverly Hills", "state": "CA" },
    "expiresAt": "2026-03-16T00:00:00.000Z",
    "monthlyPrice": 1.00,
    "autoRenew": false,
    "imageUrl": "https://joespizza.com/storefront.jpg",
    "charityId": 2,
    "pinUrl": "https://yourlocalsquare.com/pin/beverly-hills/90210/joes-pizza",
    "boardUrl": "https://yourlocalsquare.com/board/beverly-hills/90210"
  },
  "message": "Pin claimed and live. Visible on board and indexed for search. 10% of your payment supports a local charity."
}
```  

### 错误响应  
| 状态 | 含义 | 处理方式 |  
|--------|---------|------------|  
| 400 | 输入无效 | 检查必填字段和广告位格式 |  
| 402 | 需要支付 | 提交x402支付请求，并在请求头中添加`X-PAYMENT` |  
| 404 | 未找到广告位 | 请重新输入邮政编码 |  
| 409 | 广告位已被占用或广告位已满 | 请选择其他位置 |  
| 500 | 服务器错误 | 请稍后重试 |  

## 多城镇广告  
覆盖多个区域的商家应在多个邮政编码区域申请广告位。每个广告位需单独申请。**在申请多个城镇之前，请先与用户确认总费用。**  
示例：一位房地产代理需要为Beverly Hills、Santa Monica和Malibu地区的广告位申请：  
- 发送POST请求：`/api/agent/claim-pin zip="90210"`（费用1美元）  
- 发送POST请求：`/api/agent/claim-pin zip="90401"`（费用1美元）  
- 发送POST请求：`/api/agent/claim-pin zip="90265"`（费用1美元）  
总费用为3美元，可永久在三个城镇展示广告位。  

**商家获得的收益**  
成功申请后，商家将立即获得：  
1. 一个永久显示在本地数字广告板上的广告位；  
2. 一个在`pinUrl`处提供的SEO优化网页；  
3. 适用于Google的JSON-LD结构化数据（LocalBusiness格式）；  
4. 在AI搜索结果（如ChatGPT、Claude、Perplexity、Grok）中的展示；  
5. 如果提供了`googlePlaceId`，还会在Google上显示评分和评论；  
6. 广告页上包含商家网站的链接；  
7. 支付金额的10%会捐赠给商家选择的慈善机构。  

**早期采用者的广告位是永久有效的**，无需支付额外费用或续费。此优惠仅在早期采用者阶段有效。  

## x402相关说明  
```
GET /.well-known/x402.json
```  

## 代理的最佳实践  
1. **在支出前务必获得用户同意**，并向用户明确展示费用、城镇和广告位位置；  
2. 在申请前务必检查广告位的可用性（使用`GET /api/agent/boards/:zip`接口）；  
3. 尽可能收集更多信息，以提升商家的SEO排名；  
4. 如果有Google地点ID，请务必包含；评分和评论能提升页面吸引力；  
5. 如有图片资源，请提供图片链接；  
6. 设置`contactEmail`以便商家所有者后续登录管理广告位；  
7. 选择合适的`categoryId`，以便广告位出现在“最佳商家”目录中；  
8. 对于服务提供商，建议在所有服务区域申请广告位；  
9. 将`pinUrl`和`boardUrl`分享给用户，以便他们查看广告位的实时效果；  
10. 所有代理申请的广告位目前均为永久有效（早期采用者优惠），无需担心续费问题。  

## 优惠券（可选）  
如果用户提供了优惠券/折扣码，请在申请前进行验证：  
```
GET /api/agent/validate-coupon/{code}
```  
- 如果`paymentRequired`为`false`（全额减免）：在申请请求中添加`"discountCode": "CODE"`；无需使用钱包或`X-PAYMENT`头；  
- 如果`paymentRequired`为`true`（部分减免）：仍需支付x402费用，但广告位价格会按折扣显示；  
- 无效或过期的优惠券将被忽略，需全额支付。  

**相关链接**  
- 官网：https://yourlocalsquare.com  
- 隐私政策：https://yourlocalsquare.com/privacy  
- 服务条款：https://yourlocalsquare.com/terms  
- 最佳商家目录：https://yourlocalsquare.com/best  
- AI文档：https://yourlocalsquare.com/llms.txt  
- 代理API状态：https://yourlocalsquare.com/api/agent/status  
- x402相关信息：https://yourlocalsquare.com/.well-known/x402.json  
- x402协议规范：https://x402.org