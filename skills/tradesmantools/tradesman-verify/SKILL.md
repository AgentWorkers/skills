---
name: tradesman-verify
version: 2.2.0
description: 通过 OpenCorporates 的企业实体查询服务（覆盖 140 多个司法管辖区）来验证承包商的资质，并收集相关的区块链身份验证信息。使用 W3C 可验证凭证（Verifiable Credentials）来验证承包商的许可证、保险信息以及企业实体的合法性。
homepage: https://gitlab.com/lv8rlabs/tradesman-verify
metadata:
  openclaw:
    emoji: "🔐"
    install:
      - kind: node
        package: tradesman-verify
        bins:
          - tradesman-verify
---
# Tradesman Verify Skill

**Tradesman Verify Skill** 是一套用于验证承包商和技工资质的工具，它结合了 OpenCorporates 的商业实体验证服务、各州许可机构的审核机制，以及基于区块链的可验证身份认证技术，专为建筑和贸易行业设计。

## 概述

该系统为承包商、技工和服务提供商提供多层次的资质验证：

- **第一层**：商业实体验证（通过 OpenCorporates，在 140 多个司法管辖区进行）
- **第二层**：专业执照验证（由各州许可机构负责）
- **第三层**：合规性验证（可选）
- **第四层**：基于区块链的可验证身份认证（W3C Verifiable Credentials）

## 特点

### 商业实体验证（OpenCorporates）

- 确认该商业实体合法存在并已完成注册
- 公司状态（活跃、已解散、已清算）
- 公司成立日期（反映公司运营时间）
- 注册的管理人员和所有权结构
- 公司地址的真实性验证

**支持司法管辖区**：美国（所有 50 个州及华盛顿特区）、英国、加拿大、澳大利亚，以及另外 140 多个国家。

### 各州许可机构验证

- 承包商执照的当前状态
- 执照号码与公司名称的匹配性
- 专业认证（如电气、管道、暖通空调、屋顶维修等）
- 执照的有效期限和续期状态

**覆盖范围**：美国所有 50 个州。在有州级 API 的地区实现自动化验证；其他地区则采用手动验证流程。

## 使用方式

### 命令行界面 (CLI)

```bash
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

✅ Professional License Verified
   License: 123456
   Status: Active
   Expires: 2026-12-31
   Type: General Contractor

✅ VERIFICATION PASSED
   Recommendation: APPROVED
```

### 应用程序编程接口 (API)

```javascript
const { verifyContractor } = require('tradesman-verify');

const result = await verifyContractor({
  businessName: "ABC Roofing LLC",
  jurisdiction: "us_tx",
  licenseNumber: "123456",
  state: "TX"
});

console.log(result.verificationStatus); // "VERIFIED"
console.log(result.recommendation);     // "APPROVED"
```

### 批量处理

```bash
npx tradesman-verify --batch --input contractors.csv --output report.json

# Processing 15 contractors...
# ✅ 12 verified successfully
# ⚠️  2 require manual review
# ❌ 1 failed verification
```

## 输出格式

验证结果遵循 W3C Verifiable Credentials 数据模型：

```json
{
  "credentialType": "ContractorVerification",
  "subject": {
    "businessName": "ABC Roofing LLC",
    "jurisdiction": "us_tx",
    "licenseNumber": "123456"
  },
  "verification": {
    "businessEntity": {
      "verified": true,
      "source": "OpenCorporates",
      "status": "Active"
    },
    "professionalLicense": {
      "verified": true,
      "source": "Texas Dept. of Licensing",
      "status": "Active",
      "expiresAt": "2026-12-31T23:59:59Z"
    }
  }
}
```

该系统可与 Accumulate ADI 身份认证服务、Centrifuge 证明文件以及 W3C Verifiable Credentials 兼容。

## 配置要求

需要使用 OpenCorporates 的 API 密钥。免费版本每月允许 200 次 API 调用——请在 [opencorporates.com](https://opencorporates.com) 注册。使用前请将 API 密钥设置为环境变量。

高级版本（包含自动化的州级执照验证和实时监控功能）需要使用 PPCS 的 API 密钥——详情请访问 [ppcs.pro](https://ppcs.pro)。

## 使用限制

| 版本 | 每月可进行的验证次数 | 是否支持实时监控 |
|------|---------------------|---------------------|
| **免费版** | 50 次 | 不支持 |
| **专业版** | 500 次 | 支持 |
| **企业版** | 无限制 | 支持，并提供 SLA 服务 |

## 开发计划

### 第一阶段：核心功能（当前阶段）
- ✅ 通过 OpenCorporates 进行商业实体验证
- ✅ 手动进行各州许可机构的审核
- ✅ 输出格式符合 W3C 可验证身份认证标准
- ✅ 免费版本的正式上线

### 第二阶段：自动化升级（2026 年第二季度）
- 🔄 实现执照验证的自动化（仅限专业版）
- 🔄 所有 50 个州的执照验证自动化
- 🔄 实时更新执照状态通知
- 🔄 专业版的正式推出

### 第三阶段：区块链认证（2026 年第三季度）
- 📋 与 Accumulate ADI 的集成
- 📋 Centrifuge 证明文件的格式化支持
- 📋 与 Chainlink 预言机的集成

### 第四阶段：增强合规性（2026 年第四季度）
- 📋 提升合规性验证能力
- 📋 加强对监管要求的合规性检查
- 📋 监控企业的持续运营状态

## 技术支持

- [源代码和问题跟踪](https://gitlab.com/lv8rlabs/tradesman-verify)
- [OpenCorporates API 文档](https://api.opencorporates.com/documentation/API-Reference)
- [各州许可机构查询目录](https://licenselookup.org/)

## 许可证信息

采用 MIT 许可协议，完全免费且开源。详细信息请参阅 LICENSE 文件。

---

**技能版本**：2.2.0  
**最后更新时间**：2026-03-11  
**维护者**：TradesmanTools