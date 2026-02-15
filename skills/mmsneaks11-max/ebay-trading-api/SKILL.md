# eBay交易API技能

该技能用于创建、管理和查询eBay上的集换式卡牌和收藏品的列表。

## 使用场景

- 从照片或商品描述创建eBay列表
- 查找已售商品的价格以辅助定价决策
- 管理现有列表（修改或删除）
- 构建自动化的照片到列表的转换流程

## 快速入门

### 创建列表
```bash
cd ~/clawd/ebay && python3 trading_api.py --create
```

### 无列表验证（模拟运行）
```bash
cd ~/clawd/ebay && python3 trading_api.py
```

### 查看已售商品价格
```bash
cd ~/clawd/ebay && python3 comps.py "2024 Topps Chrome Mike Trout"
```

## 可用的API调用

| 调用 | 功能 | 脚本 |
|------|---------|--------|
| `AddItem` | 创建新列表 | `trading_api.py` |
| `VerifyAddItem` | 无列表情况下进行验证 | `trading_api.py` |
| `ReviseItem` | 修改现有列表 | `revise.py`（待完成） |
| `EndItem` | 删除列表 | `end.py`（待完成） |
| `GetItem` | 获取列表详情 | `get_item.py`（待完成） |
| `findCompletedItems` | 查询已售商品价格 | `comps.py` ✅ |

## 卡片状态

### 未分级卡片（状态ID：4000）
| 状态 | 描述符ID |
|-----------|---------------|
| 几乎全新 | 400010 |
| 优秀 | 400011 |
| 非常好 | 400012 |
| 较差 | 400013 |

### 分级卡片（状态ID：2750）
支持的分级机构：PSA、BGS、SGC、CGC、CSG、BVG、BCCG、KSA、GMA、HGA

等级：10、9.5、9、8.5、8、7.5、7、6.5、6、5.5、5、4.5、4、3.5、3、2.5、2、1.5、1、真品

## 配置

### 必需的环境变量
在`~/.env.ebay`中设置或直接导出：

```bash
EBAY_DEV_ID=your-dev-id
EBAY_APP_ID=your-app-id  
EBAY_CERT_ID=your-cert-id
```

### OAuth令牌
存储在`~/clawd/ebay/.tokens.json`中（自动管理）：
```json
{
  "access_token": "v^1.1#i^1#...",
  "refresh_token": "v^1.1#i^1#...",
  "expires_at": 1706644800
}
```

运行`oauth_setup.py`初始化令牌，或运行`refresh_token.py`刷新过期令牌。

## 使用示例

### Python：创建运动卡片列表
```python
from trading_api import load_credentials, create_sports_card_listing

creds = load_credentials()

card_info = {
    "title": "2024 Topps Chrome Mike Trout #1 Refractor",
    "player": "Mike Trout",
    "year": "2024",
    "set_name": "Topps Chrome",
    "card_number": "1",
    "parallel": "Refractor",
    "sport": "Baseball",
    "manufacturer": "Topps",
    "condition": "Near Mint or Better",
    "graded": False
}

item_id = create_sports_card_listing(creds, card_info, price="29.99")
print(f"Listed: https://www.ebay.com/itm/{item_id}")
```

### Python：分级卡片列表
```python
card_info = {
    "title": "2020 Panini Prizm LaMelo Ball RC PSA 10",
    "player": "LaMelo Ball",
    "year": "2020",
    "set_name": "Panini Prizm",
    "card_number": "278",
    "sport": "Basketball",
    "manufacturer": "Panini",
    "graded": True,
    "grader": "PSA",
    "grade": "10",
    "cert_number": "12345678"
}

item_id = create_sports_card_listing(creds, card_info, price="199.99")
```

## 速率限制

| API | 每日限制 | 重置时间 |
|-----|-------------|------------|
| Trading API | 5,000次调用 | 太平洋时间午夜 |
| Finding API | 5,000次调用 | 太平洋时间午夜 |

**最佳实践**：
- 使用`VerifyAddItem`进行测试（计入调用次数）
- 在遇到503错误时采用指数级退避策略
- 缓存查询结果以减少Finding API的调用次数

## 故障排除

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `Auth token is hard expired` | 访问令牌过期（2小时） | 运行`oauth_setup.py` |
| `Invalid refresh token` | 刷新令牌过期（18个月） | 通过`oauth_setup.py`重新认证 |
| `Exceeded the number of times` | 被eBay限制了调用次数 | 等待1小时或查看eBay开发者控制台 |
| `Invalid App ID` | 凭据错误 | 确保`.env.ebay`中包含`EBAY_PROD_APP_ID` |
| `Category not found` | 类别ID错误 | 使用正确的类别名称（如`basketball`、`baseball`） |
| `Missing item specifics` | 必填字段为空 | 添加球员名称、年份、系列和卡片编号 |
| `No items found` | 查询过于具体 | 扩大搜索范围 |
| `Connection timeout` | eBay API响应缓慢 | 30秒后重试 |
| `503 Service Unavailable` | API负载过高 | 等待后重试并采用退避策略 |

## 安全注意事项

### 🔑 令牌管理
- 令牌存储在`.tokens.json`文件中 — 确保文件权限设置为`600`：`chmod 600 .tokens.json`
- 访问令牌2小时后过期（通过`refresh_token`自动刷新）
- 刷新令牌18个月后过期 — 建议设置提醒
- 如果刷新失败，重新运行`oauth_setup.py`进行重新认证

### 🔒 凭据安全
- **切勿将`.tokens.json`或`.env.ebay`文件提交到git仓库**
- 将这些文件添加到`.gitignore`中：`.tokens.json`, `.env.ebay`, `*.log`
- 使用环境变量而非硬编码值
- 令牌泄露后立即更换
- API凭据（开发/应用/证书ID）虽然不是机密信息，但仍需保密

### ✅ 输入验证
- 所有用户输入在API调用前都会通过`html.escape()`进行转义
- 标题长度限制为80个字符（符合eBay规定）
- 描述内容使用CDATA标签以防止XML注入
- 卡片编号和等级信息仅保留字母数字字符

### 📋 日志记录
- 失败的列表操作会记录到`~/clawd/ebay/errors.log`
- 成功的列表操作会记录ItemID、时间戳和价格
- 日志至少保留90天（符合eBay争议处理要求）

### 🛡️ API响应处理
- **切勿记录完整的API响应内容**（可能包含个人隐私信息）
- 在非调试日志中屏蔽ItemID：例如`1234***789`
- 在显示给用户之前对错误信息进行清洗
- 从日志中删除买家/卖家信息

## 沙盒环境与生产环境

通过`sandbox`参数切换环境：
```python
# Sandbox (testing)
response = call_trading_api(creds, "AddItem", xml, sandbox=True)

# Production (real listings)
response = call_trading_api(creds, "AddItem", xml, sandbox=False)
```

沙盒URL：`https://api.sandbox.ebay.com/ws/api.dll`
生产环境URL：`https://api.ebay.com/ws/api.dll`

## 文件结构

```
~/clawd/ebay/
├── .env.ebay          # API credentials (gitignored)
├── .tokens.json       # OAuth tokens (gitignored)
├── trading_api.py     # Core Trading API wrapper
├── description_template.py  # HTML listing templates
├── oauth_setup.py     # Initial OAuth flow
├── exchange_token.py  # Token refresh
├── create_listing.py  # Inventory API approach
└── pending.json       # Pending listings queue
```

## 待完成事项

- [x] `comps.py` — 实现查询已售商品价格的函数 ✅
- [ ] `revise.py` — 修改列表功能的实现
- [ ] `end.py` — 删除列表功能的实现
- [ ] `upload.py` — 与eBay图片服务的集成
- [ ] 实现基于指数级退避的速率限制
- [ ] 实现结构化的错误日志记录

## 已知限制

### 速率限制
- **Finding API**：每日5,000次调用（新应用可能更低）
- **Trading API**：每日5,000次调用
- 如果达到限制，`comps.py`会返回`fallback: true`——此时需手动定价
- 限制在太平洋时间午夜重置
- 新应用可能初始时有更严格的临时调用限制

### 令牌过期
- **访问令牌**2小时后过期（自动刷新）
- **刷新令牌**18个月后过期——建议设置提醒
- 如果刷新失败，重新运行`oauth_setup.py`进行重新认证

### Finding API需要生产环境凭据
`Finding API`（`findCompletedItems`）不支持沙盒环境。查询已售商品价格时必须使用生产环境的eBay凭据。请在`.env.ebay`文件中添加`EBAY_PROD_APP_ID`。

## 参考资料

- [eBay交易API文档](https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/index.html)
- [AddItem调用文档](https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/AddItem.html)
- [Finding API（查询已售商品价格）](https://developer.ebay.com/Devzone/finding/Concepts/FindingAPIGuide.html)
- [卡片状态描述符](https://developer.ebay.com/devzone/finding/callref/Enums/conditionIdList.html)

---

*该技能由Clawd 🐾 和 Electron 🦞 为Text2List.app开发*