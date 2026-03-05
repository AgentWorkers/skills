# 报告生成器技能

## 目的
通过单次 GPT-4.1-mini 调用，将汇总的市场营销数据转换为结构化、专业的审计报告。这是整个审计流程中唯一使用 AI 的环节。

## 输入数据格式
```typescript
interface AuditData {
 input: AuditInput;
 instagram: InstagramData;
 metaAds: MetaAdsData;
 keywords: KeywordData;
 competitors: CompetitorData;
 websiteAudit: WebsiteAuditData;
 collectedAt: string;
}
```

## 输出数据格式
```typescript
interface MarketingReport {
 brand: string;
 generatedAt: string;
 sections: ReportSections;
 rawData: AuditData;
 reportMarkdown: string;
}
```

## API 依赖项
- **API:** OpenAI
- **模型:** `gpt-4.1-mini`
- **认证:** `OPENAI_API_KEY`
- **费用:** 每次调用约 0.001-0.002 美元

## 实现方式
- 系统提示定义分析师的角色以及报告的 6 个具体章节结构
- 用户输入的数据为完整的 AuditData JSON 格式
- 通过单次 API 调用（参数：`max_tokens: 1500`, `temperature: 0.4`）生成报告
- 响应内容通过 `##` 标签分割成各个章节
- 记录每个调用的令牌使用情况以用于费用追踪
- 如果 OpenAI 调用失败，会生成备用报告

## 令牌预算
- 输入数据：约 1,500-2,000 个令牌（JSON 数据）
- 输出报告：约 800-1,200 个令牌

## 错误处理
- 未提供 API 密钥：返回包含错误信息的备用报告
- API 调用失败：返回保留原始数据的备用报告
- 所有错误都会被记录并附带相关上下文信息

## 示例用法
```typescript
const report = await generateMarketingReport(auditData);
console.log(report.reportMarkdown);
```

## 注意事项
- 这是唯一需要调用 OpenAI 的文件（除非使用竞争对手提供的数据收集工具作为备用方案）；
- 请勿在其他模块中添加额外的 GPT 调用。