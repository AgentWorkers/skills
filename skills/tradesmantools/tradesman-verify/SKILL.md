---
name: tradesman-verify
version: 2.1.0
description: 通过 OpenCorporates 的企业实体查询服务（覆盖 140 多个司法管辖区）来验证承包商的资质，并收集相关的区块链身份验证数据（ADI）。同时，生成符合 W3C 标准的可验证凭证（Verifiable Credentials），用于完成客户尽职调查（KYC）、承包商许可证审核、保险信息验证以及企业实体身份确认等工作。该流程参考了 ACME 基金会的实现规范。
homepage: https://gitlab.com/lv8rlabs/tradesman-verify
metadata:
  openclaw:
    emoji: "🔐"
    primaryEnv: OPENCORPORATES_API_KEY
    requires:
      env:
        - OPENCORPORATES_API_KEY
    install:
      - kind: node
        package: tradesman-verify
        bins:
          - tradesman-verify
---
# 工匠技能验证

**这是一种用于承包商身份验证的“凭证证明”（Proof-of-Credential）基础设施**，它结合了 OpenCorporates 的企业实体验证、州级许可委员会的审核以及与区块链兼容的凭证认证机制。该系统类似于 Centrifuge 的 Proof-of-Index (SPXA)，但专为建筑和贸易行业中的服务提供商身份验证而设计。

## 概述

BIMPassport 的“凭证证明”系统通过多层验证机制，为承包商、工匠和服务提供商建立可信赖的信任体系：

- **第一层**：企业实体验证（通过 OpenCorporates，在 140 多个司法管辖区进行）
- **第二层**：专业执照验证（由各州许可委员会负责）
- **第三层**：风险评估和合规性筛查（可选）
- **第四层**：区块链认证（采用与去中心化工作力（deRWA）兼容的凭证格式）

此技能提供了基础的身份验证层，为后续的凭证发放流程奠定基础。

## 特点

### 凭证证明基础设施

**什么是“凭证证明”？**

类似于 Centrifuge 的 Proof-of-Index (SPXA) 用于验证 DeFi 借贷中的真实世界资产的存在性和特征，BIMPassport 的“凭证证明”机制用于验证服务提供商凭证的存在性和合法性，从而支持去中心化的工作协作。

**主要功能：**
- 多司法管辖区的企业实体验证（通过 OpenCorporates，在 140 多个国家进行）
- 美国所有州的专业执照验证
- 实时状态监控（活跃、暂停、过期）
- 历史验证审计追踪
- 与去中心化工作力（deRWA）兼容的输出格式，适用于区块链认证

### OpenCorporates 集成

**企业实体验证：**
- 企业实体合法存在并已注册
- 企业状态（活跃、解散、清算）
- 注册日期（企业存续时间的指标）
- 注册董事和所有权结构
- 企业地址验证

**支持的司法管辖区：**
- 美国（所有 50 个州 + 华盛顿特区）
- 英国
- 加拿大
- 澳大利亚
- 其他 140 多个国家

### 州级许可委员会验证

**专业执照审核：**
- 承包商执照的活跃状态
- 执照号码与企业名称的匹配性
- 专业认证（电气、管道、暖通空调、屋顶等）
- 执照有效期和续期状态
- 违规行为记录

**美国各州覆盖情况：**
- 支持所有 50 个州
- 在有州级 API 的情况下提供自动验证
- 在没有 API 的州提供手动验证流程

### BMLS 框架集成

该技能实现了 **Build-Measure-Learn-Share (BMLS)** 框架：

- **构建**：承包商凭证的验证基础设施
- **测量**：验证成功率、API 响应时间、执照到期跟踪
- **学习**：识别高风险司法管辖区，优化验证流程
- **共享**：每季度通过 BIMHero DAO 公布匿名化的验证指标

详细框架文档请参阅 [BMLS-FRAMEWORK.md](../../BMLS-FRAMEWORK.md)。

## 使用方式

### 免费 tier

**限制：**
- 每月 50 次验证
- 使用 OpenCorporates 免费 tier，每月 200 次 API 调用
- 手动进行州级许可委员会审核
- 提供基本验证报告（JSON 格式）

**适用对象：**
- 需偶尔验证分包商的小型承包商
- 测试和开发人员
- 个人物业经理

### 命令行界面（CLI）使用

```bash
# Basic verification
npx tradesman-verify \
  --business-name "ABC Roofing LLC" \
  --jurisdiction "us_tx" \
  --license-number "123456" \
  --state "TX"

# Output
✅ Business Entity Verified
   Company: ABC ROOFING LLC
   Status: Active
   Incorporated: 2020-05-15
   Jurisdiction: us_tx

✅ Professional License Verified
   License: 123456
   Status: Active
   Expires: 2026-12-31
   Type: General Contractor

✅ VERIFICATION PASSED
   Recommendation: APPROVED
   Valid Until: 2027-02-13
```

### API 使用

```javascript
const { verifyContractor } = require('tradesman-verify');

const result = await verifyContractor({
  businessName: "ABC Roofing LLC",
  jurisdiction: "us_tx",
  licenseNumber: "123456",
  state: "TX"
});

// Output
{
  "contractorId": "abc_roofing_llc",
  "verificationStatus": "VERIFIED",
  "verificationDate": "2026-02-18T14:00:00Z",
  "businessVerification": {
    "isRegistered": true,
    "isActive": true,
    "incorporationDate": "2020-05-15",
    "businessAge": "5.75 years",
    "jurisdiction": "us_tx",
    "companyNumber": "0803456789"
  },
  "licenseVerification": {
    "isValid": true,
    "licenseNumber": "123456",
    "licenseType": "General Contractor",
    "expirationDate": "2026-12-31",
    "status": "Active"
  },
  "recommendation": "APPROVED"
}
```

### 批量处理

```bash
# Verify multiple contractors from CSV
npx tradesman-verify --batch --input contractors.csv --output verification-report.json

# Output
Processing 15 contractors...
✅ 12 verified successfully
⚠️  2 require manual review
❌ 1 failed verification

Details saved to: verification-report.json
```

## 输出格式

### 与去中心化工作力（deRWA）兼容的凭证格式

验证结果可以以与去中心化工作力（deRWA）兼容的格式输出，适用于区块链认证：

```json
{
  "credentialType": "ProofOfCredential",
  "credentialSubtype": "ContractorVerification",
  "subject": {
    "businessName": "ABC Roofing LLC",
    "jurisdiction": "us_tx",
    "licenseNumber": "123456"
  },
  "verification": {
    "businessEntity": {
      "verified": true,
      "source": "OpenCorporates",
      "verifiedAt": "2026-02-18T14:00:00Z",
      "status": "Active"
    },
    "professionalLicense": {
      "verified": true,
      "source": "Texas Dept. of Licensing",
      "verifiedAt": "2026-02-18T14:00:00Z",
      "status": "Active",
      "expiresAt": "2026-12-31T23:59:59Z"
    }
  },
  "attestation": {
    "attestedBy": "BIMPassport-ProofOfCredential-v1",
    "attestedAt": "2026-02-18T14:00:00Z",
    "validUntil": "2027-02-18T14:00:00Z",
    "checksumSHA256": "a3f5b8c..."
  }
}
```

该格式兼容以下系统：
- Accumulate ADI 凭证发放（通过 tradesman-validate）
- Circle ARC 认证基础设施
- Centrifuge Proof-of-X 框架
- W3C 可验证凭证（W3C Verifiable Credentials）

## 升级方案

### 高级 tier

**PPCS Pro** (ppcs.pro)
- 每月 500 次验证
- 自动化州级执照审核
- 实时状态监控 Webhook
- 优先支持
- 价格：每月 99 美元

**Enterprise** (lv8rlabs.com)
- 无限次验证
- 专用 API 端点
- 定制集成
- 风险评估功能（针对高级用户）
- 白标品牌服务
- 服务水平协议（SLA）保障
- 价格：请联系销售部门

### 高级功能

**实时监控：**
```javascript
// Webhook notification when contractor license status changes
POST https://your-app.com/webhooks/license-status
{
  "event": "license_status_changed",
  "contractorId": "abc_roofing_llc",
  "licenseNumber": "123456",
  "previousStatus": "Active",
  "newStatus": "Expired",
  "changedAt": "2026-06-30T23:59:59Z"
}
```

**风险评估：**
- 制裁和黑名单筛查
- 负面媒体监控
- 诉讼记录
- 财务稳定性指标
- 总体风险评分（0-100）

**高级分析：**
- 验证成功率趋势
- 地理风险热图
- 执照到期预测
- 合规性仪表板

## 与 BIMPassport 生态系统的集成

### tradesman-validate 集成

通过 `tradesman-verify` 完成验证后，凭证可以通过 `tradesman-validate` 在区块链上发放：

```bash
# Step 1: Verify contractor
npx tradesman-verify --business-name "ABC Roofing LLC" --jurisdiction "us_tx" --license-number "123456" --state "TX"

# Step 2: Issue blockchain credential (requires tradesman-validate)
npx tradesman-validate --contractor-id "abc_roofing_llc" --adi-url "abc.acme/contractor" --credential-type "contractor-license"
```

### 与去中心化工作力（deRWA）的兼容性

BIMPassport 的凭证与去中心化真实世界资产（deRWA）协议兼容：

- **Centrifuge**：可用作服务提供商融资的证明文件
- **Circle ARC**：适用于机构合规性的认证格式
- **Accumulate**：原生 ADI 凭证发放
- **Chainlink Functions**：链下验证预言机集成

### BIMHero DAO 治理

验证指标和标准由 BIMHero DAO 管理（详情见 BMLS-FRAMEWORK.md）：

- 每季度发布匿名化的验证指标
- 社区驱动的阈值调整（例如，针对 IP 侵权的代码相似性判断）
- 政策的透明演变
- 开源验证算法（高级风险模型为专有技术）

## 环境变量

### 必需的环境变量（免费 tier）

```bash
# OpenCorporates API (Free tier: 200/month)
OPENCORPORATES_API_KEY="your-opencorporates-api-key"
```

### 可选的环境变量（高级 tier）

```bash
# PPCS Premium API (license automation + risk assessment)
PPCS_API_KEY="your-ppcs-api-key"
```

## API 使用限制

| 级别 | 每月验证次数 | 每月 API 调用次数 | 实时监控功能 |
|------|---------------------|-----------------|---------------------|
| **免费** | 50 | 200（OpenCorporates） | 无 |
| **PPCS Pro** | 500 | 无限 | 有 |
| **Enterprise** | 无限 | 无限 | 有 + 服务水平协议（SLA） |

## 错误处理

### OpenCorporates 相关错误

**超出速率限制（429）：**
```javascript
{
  "error": "rate_limit_exceeded",
  "message": "Daily limit of 50 requests exceeded",
  "action": "Upgrade to paid plan or retry after 24 hours"
}
```

**公司未找到（404）：**
```javascript
{
  "error": "business_entity_not_found",
  "message": "No registered business found for 'ABC Roofing LLC' in us_tx",
  "action": "Verify business name spelling, check jurisdiction, request incorporation docs"
}
```

### 执照验证错误

**执照过期：**
```javascript
{
  "error": "license_expired",
  "licenseNumber": "123456",
  "expirationDate": "2025-12-31",
  "action": "Request updated license documentation from contractor"
}
```

**执照被暂停：**
```javascript
{
  "error": "license_suspended",
  "licenseNumber": "123456",
  "suspensionDate": "2026-01-15",
  "reason": "Non-payment of renewal fee",
  "action": "CRITICAL - Block contractor from new jobs, escalate to compliance team"
}
```

## 验证结果

### 验证通过
```javascript
{
  "status": "VERIFIED",
  "confidence": "HIGH",
  "checks": {
    "businessEntity": "PASSED",
    "professionalLicense": "PASSED"
  },
  "recommendation": "APPROVED",
  "validUntil": "2027-02-18T14:00:00Z"
}
```

### 验证失败
```javascript
{
  "status": "FAILED",
  "confidence": "N/A",
  "checks": {
    "businessEntity": "FAILED",
    "professionalLicense": "NOT_FOUND"
  },
  "recommendation": "REJECT",
  "reason": "Business entity dissolved, license not found"
}
```

### 需要手动审核
```javascript
{
  "status": "PENDING",
  "confidence": "MEDIUM",
  "checks": {
    "businessEntity": "PASSED",
    "professionalLicense": "MANUAL_CHECK_REQUIRED"
  },
  "recommendation": "MANUAL_REVIEW",
  "reason": "State licensing board has no API, manual verification required"
}
```

## 测试

### 使用 OpenCorporates 免费 tier 进行测试

```bash
# Set test API key
export OPENCORPORATES_API_KEY="test_key_xxxxx"

# Test company search
curl --header "X-API-TOKEN:$OPENCORPORATES_API_KEY" \
  "https://api.opencorporates.com/v0.4/companies/search?q=test&jurisdiction_code=us_tx"

# Verify API quota
curl --header "X-API-TOKEN:$OPENCORPORATES_API_KEY" \
  "https://api.opencorporates.com/v0.4/account_status"
```

### 开发用途的模拟数据

```javascript
const mockVerificationResult = {
  status: "VERIFIED",
  businessEntity: {
    isActive: true,
    incorporationDate: "2020-01-01",
    jurisdiction: "us_tx"
  },
  license: {
    isValid: true,
    expirationDate: "2026-12-31",
    status: "Active"
  },
  recommendation: "APPROVED"
};
```

## 发展路线图

### 第一阶段：核心验证（当前阶段）
- ✅ 使用 OpenCorporates 进行企业实体验证
- ✅ 手动进行州级许可委员会审核
- ✅ 与去中心化工作力（deRWA）兼容的输出格式
- ✅ 免费 tier 的实现

### 第二阶段：自动化升级（2026 年第二季度）
- 🔄 自动化执照审核功能（高级 tier）
- 🔄 所有 50 个州的自动化执照审核
- 🔄 实时状态变更 Webhook
- 🔄 高级 tier 的正式推出

### 第三阶段：区块链认证（2026 年第三季度）
- 📋 与 Accumulate ADI 的原生集成
- 📋 支持 Circle ARC 认证
- 📋 与 Centrifuge 的证明文件格式兼容
- 📋 与 Chainlink 预言机的集成

### 第四阶段：高级风险管理（2026 年第四季度）
- 📋 高级风险评估功能
- 📋 制裁筛查
- 📋 诉讼监控
- 📋 财务稳定性指标

## 支持服务

### 文档资料
- [tradesman-verify npm 库](https://gitlab.com/lv8rlabs/tradesman-verify)
- [BMLS 框架文档](../../BMLS-FRAMEWORK.md)
- [OpenCorporates API 文档](https://api.opencorporates.com/documentation/API-Reference)

### 各州许可机构信息
- [德克萨斯州 TDLR](https://www.tdlr.texas.gov/LicenseSearch/)
- [加利福尼亚州 CSLB](https://www.cslb.ca.gov/onlineservices/checklicenseII/checklicense.aspx)
- [华盛顿州 L&I](https://secure.lni.wa.gov/verify/)
- [执照查询目录](https://licenselookup.org/)

### 升级与定价
- **PPCS Pro**：https://ppcs.pro/pricing
- **Enterprise**：https://lv8rlabs.com/contact
- **社区支持**：https://gitlab.com/lv8rlabs/tradesman-verify/-/issues

## 许可证

采用 MIT 许可证协议 - 详细信息请参阅 [LICENSE](../../LICENSE) 文件。

**开源版本**：每月最多 50 次验证时免费
**商业版本**：PPCS Pro 和 Enterprise 需订阅

---

**技能版本**：2.1.0
**最后更新时间**：2026-02-28
**维护者**：TradesmanTools / BIMPassport
**状态**：已准备好投入生产
**已提交至 ClawHub**：已完成提交流程