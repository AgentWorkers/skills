---
name: aeo-schema-validate
description: 根据AEO的最佳实践，验证URL上的JSON-LD结构化数据。检查数据模式类型、属性的完整性以及实体的一致性。适用于有针对性的数据模式审计。
allowed-tools:
  - Bash(npx *)
  - Bash(aeo-audit *)
argument-hint: <url>
---
# AEO 数据结构验证

网站：[ainyc.ai](https://ainyc.ai)

专注于验证 JSON-LD 结构化数据是否满足 AEO（反欺诈和反洗钱）标准。

## 流程

1. 进行针对性的审计：
   ```
   npx @ainyc/aeo-audit@latest $ARGUMENTS --format json --factors structured-data,schema-completeness,entity-consistency
   ```
2. 解析审计结果
3. 提供详细的验证报告：
   - **发现的schema 类型**（列出每种 schema 类型及其包含的属性数量）
   - **属性的完整性**（每种 schema 类型中推荐属性的覆盖率）
   - **每种类型中缺失的推荐属性**
   - **实体的一致性**（schema、title 和 og:title 之间的名称是否一致）
4. 对于发现的问题，提供修正后的或优化后的 JSON-LD 示例
5. 为检测到的业务类型提供最佳的 JSON-LD 模板

## 各 schema 类型的检查清单

**LocalBusiness:** name（名称）、address（地址）、telephone（电话）、openingHours（营业时间）、priceRange（价格范围）、image（图片）、url（网址）、geo（地理位置）、areaServed（服务区域）、sameAs（关联实体）
**FAQPage:** mainEntity（主要实体），其中包含至少 3 对问答，每条问答的文字长度不少于 15 个单词
**HowTo:** name（名称）、step（步骤），每个步骤包含名称和具体内容
**Organization:** name（名称）、logo（标志）、contactPoint（联系方式）、sameAs（关联实体）、foundingDate（成立日期）、url（网址）、description（描述）