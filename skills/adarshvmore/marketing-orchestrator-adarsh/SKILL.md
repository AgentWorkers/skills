# Marketing Orchestrator 技能

## 目的
通过依次运行以下收集器代理来协调营销审计流程：
- Instagram 收集器
- Meta Ads 收集器
- SEO / 关键词收集器
- 竞争对手查找器
- 网站审计收集器

将各个收集器的结果汇总，并调用 Report Generator 技能生成最终的全面营销审计报告。

## 输入格式
```typescript
interface MarketingInput {
  instagramHandle?: string;
  websiteDomain?: string;
}
```

## 输出格式
```typescript
interface MarketingAuditReport {
  reportMarkdown: string;
  rawData: any;
  error?: string;
}
```

## 实现模式

- 验证输入：必须提供 `instagramHandle` 或 `websiteDomain` 中的一个参数。
- 依次调用每个收集器技能，并传递相应的输入参数。
- 将收集到的结果汇总到一个复合数据对象中。
- 使用汇总后的数据调用 Report Generator 技能。
- 返回最终的报告Markdown格式文件以及原始数据。

## 示例用法
```typescript
const input = { instagramHandle: 'gymshark', websiteDomain: 'gymshark.com' };
const report = await marketingOrchestrator(input);
console.log(report.reportMarkdown);
```

## 协调逻辑（伪代码）
```typescript
async function marketingOrchestrator(input: MarketingInput): Promise<MarketingAuditReport> {
  if (!input.instagramHandle && !input.websiteDomain) {
    throw new Error("Either instagramHandle or websiteDomain is required");
  }

  const auditData: any = {
    input,
    collectedAt: new Date().toISOString(),
  };

  if (input.instagramHandle) {
    auditData.instagram = await runSkill('instagram-collector', { handle: input.instagramHandle });
  }

  if (input.websiteDomain) {
    auditData.metaAds = await runSkill('meta-ads-collector', { brandName: input.websiteDomain, domain: input.websiteDomain });
    auditData.keywords = await runSkill('seo-collector', { domain: input.websiteDomain });
    auditData.competitors = await runSkill('competitor-finder', { brandName: input.websiteDomain, domain: input.websiteDomain });
    auditData.websiteAudit = await runSkill('website-audit', { domain: input.websiteDomain });
  }

  const report = await runSkill('report-generator', auditData);

  return {
    reportMarkdown: report.reportMarkdown,
    rawData: auditData,
  };
}
```

## 注意事项：
- 每次调用 `runSkill` 都相当于启动了一个子代理或子进程。
- 调用框架应负责处理外部服务的API密钥和环境变量。
- 单个收集器出现的错误不应影响整个协调流程的进行。
- 根据需要可扩展以支持更多的收集器或数据源。