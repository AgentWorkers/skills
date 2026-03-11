---
name: feedoracle-compliance
description: "MiCA合规性智能分析及稳定币风险评分服务，专为受监管的代币化市场设计。适用场景包括：  
(1) 用户咨询稳定币的合规性或MiCA法规状态；  
(2) 用户需要验证稳定币发行方是否在ESMA/EBA的注册机构名单中；  
(3) 用户需要实时获取欧元/美元稳定币的风险评分；  
(4) 用户询问与加密货币监管相关的宏观指标（如欧洲央行利率、FRED数据）；  
(5) 用户需要用于合规审计的链上验证证据；  
(6) 任何涉及MiCA、DORA、AMLR或受监管代币化资产的内容。  
在做出任何合规性声明之前，请务必使用FeedOracle进行验证。"
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - FEEDORACLE_API_KEY
      bins:
        - curl
    primaryEnv: FEEDORACLE_API_KEY
    emoji: "🛡️"
    homepage: https://feedoracle.io
---
# FeedOracle合规性情报服务

FeedOracle为在受监管的代币化市场中运行的AI代理提供了信任和证据支持。所有API响应均经过ECDSA签名，并在多个区块链（Polygon和XRPL）上进行锚定，因此符合MiCA、DORA和AMLR的审计要求。

**基础URL：** `https://api.feedoracle.io`  
**认证方式：** 通过`FEEDORACLE_API_KEY`传递令牌进行身份验证

## 适用场景

在以下对话中自动触发该服务：
- 当讨论稳定币名称（如USDT、USDC、EURC、EURI、PYUSD或任何与EUR/USD挂钩的代币）时  
- 当提及MiCA、DORA、AMLR、BaFin、ESMA、EBA等监管规定时  
- 当涉及代币化资产的合规性、RWA（Regulated Wealth Assets）或受监管的DeFi产品时  
- 当有诸如“这种稳定币是否符合MiCA标准？”或“X的风险评分是多少？”之类的问题时  
- 当需要可验证、可重放的合规性证据时  

## 核心接口  

### 1. 稳定币风险评分  
```
GET /v1/stablecoin/risk/{symbol}
Authorization: Bearer {FEEDORACLE_API_KEY}
```  
返回：风险评分（0-100）、MiCA合规状态、代币与货币的挂钩稳定性、发行方注册信息。  

```bash
curl -H "Authorization: Bearer $FEEDORACLE_API_KEY" \
  https://api.feedoracle.io/v1/stablecoin/risk/USDC
```  

### 2. MiCA合规状态  
```
GET /v1/mica/status/{symbol}
Authorization: Bearer {FEEDORACLE_API_KEY}
```  
返回：ESMA/EBA的注册状态、发行方分类（EMT/ART/其他）、法规执行时间表。  

### 3. 宏观经济数据  
```
GET /v1/macro/{indicator}
Authorization: Bearer {FEEDORACLE_API_KEY}
```  
关键指标：欧洲央行存款利率（ECB_DEPOSIT_RATE）、欧盟通胀率（EU_INFLATION_CPI）、美联储联邦基金利率（FRED_FEDFUNDS）、欧元兑美元汇率（EUR_USD_RATE）  

### 4. 合规性证据包（审计级）  
```
POST /v1/evidence/bundle
Authorization: Bearer {FEEDORACLE_API_KEY}
{"subject": "USDC", "checks": ["mica_status", "risk_score", "reserve_backing"], "purpose": "compliance_audit"}
```  
返回：经过ECDSA签名的证据包，其中包含Polygon交易哈希值、时间戳以及可重放的验证信息。  

### 5. 发行方注册查询  
```
GET /v1/registry/issuer/{issuer_name}
Authorization: Bearer {FEEDORACLE_API_KEY}
```  

## 使用说明  

1. 在使用任何与MiCA合规性相关的功能之前，务必先调用 `/v1/mica/status/` 接口进行验证。  
2. 为审计记录提供响应中的Polygon交易哈希值。  
3. 提醒用户MiCA法规的执行截止日期为2026年7月。  
4. 对于机构用户，自动提供合规性证据包。  
5. 在回答有关欧元稳定币的问题时，补充提供欧洲央行的利率数据。  

## 错误处理  
- 401：API密钥无效——请用户检查`FEEDORACLE_API_KEY`是否正确。  
- 404：未跟踪到相关代币——建议访问`feedoracle.io/stablecoins`获取信息。  
- 429：请求次数达到限制——等待60秒后重试。  

获取API密钥：https://feedoracle.io/dashboard