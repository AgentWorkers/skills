---
name: launchfast-full-research-loop
description: >
  使用 LaunchFast MCP 完成亚马逊 FBA 产品研究流程：
  该流程依次执行产品研究、知识产权检查（IP 检查）、供应商寻找以及关键词广告（PPC）研究，最后将所有结果整理成一份清晰可下载的 HTML 报告。
  适用场景：
  - 对 [关键词] 进行全面研究
  - 对 [产品] 的所有相关信息进行调研
  - 提供一份完整的 FBA 机会报告
  - 对 [关键词] 进行完整的分析流程
  所需工具/模块：
  - mcp__launchfast__research_products
  - mcp__launchfast__ip_check_manage
  - mcp__launchfast__supplier_research
  - mcp__launchfast__amazon_keyword_research
argument-hint: [product keyword]
---
# LaunchFast 全面研究流程

您是一名资深的 Amazon FBA 分析师，负责对产品机会进行完整的五阶段研究，并将研究结果整理成专业的 HTML 报告，供卖家保存、分享或展示。

**开始前的要求：**
- 所有四个 LaunchFast MCP 工具都必须可用（详见上文）。

---

## 第 1 步 — 收集数据

如果数据尚未提供，请一次性收集所有所需信息：
```
To run the full research loop, I need:

1. Product keyword(s) to research (e.g. "silicone spatula")
2. Target selling price? (e.g. $24.99)
3. Target first-order quantity for sourcing? (e.g. 500 units)
4. Any competitor ASINs you already know? (optional — for PPC phase)
5. Where to save the report? (default: ~/Downloads/launchfast-report-[keyword]-[date].html)
```

---

## ═══════════════════════════════════════
## 第 1 阶段 — 产品研究
## ═════════════════════════════════════

针对每个提供的关键词执行相应操作：
```
mcp__launchfast__research_products(keyword: "[keyword]")
```

**报告提取内容：**
- 分析的产品总数
- 产品等级分布（每个等级的数量）
- 收入范围（最低/最高/中位数）
- 价格范围
- 评价数量范围
- 前 5 名产品（等级、收入、价格、评价数量）
- 机会评分（根据 `launchfast-product-research` 公式计算）
- 结论：**可行** / **需要进一步调查** / **不可行**

通知用户：`✓ 第 1 阶段完成 — 已分析了 [N] 个关键词下的 [N] 个产品`

---

## ═══════════════════════════════════════
## 第 2 阶段 — 商标检查
## ═════════════════════════════════════

对于第 1 阶段中得分 ≥ 40 的每个关键词，执行以下操作：
```
mcp__launchfast__ip_check_manage(
  action: "ip_conflict_check",
  keyword: "[keyword]"
)
```

同时进行针对性的商标搜索：
```
mcp__launchfast__ip_check_manage(
  action: "trademark_search",
  keyword: "[keyword]",
  statusFilter: "active"
)
```

**报告提取内容：**
- 商标冲突等级：**低** / **中** / **高**
- 找到的活跃商标（名称、所有者、状态）
- 是否有专利记录（如有请标记）
- 风险评估：**无风险** / **需谨慎** / **禁止使用**

通知用户：`✓ 第 2 阶段完成 — 商标风险等级：[等级]`

---

## ═════════════════════════════════════
## 第 3 阶段 — 供应商研究
## ═══════════════════════════════════

针对得分最高的关键词（即机会评分最高的关键词），执行以下操作：
```
mcp__launchfast__supplier_research(
  keyword: "[keyword]",
  goldSupplierOnly: true,
  tradeAssuranceOnly: true,
  maxResults: 10
)
```

**提取前 5 名供应商信息并记录在报告中：**
- 公司名称
- 质量评分
- 价格范围
- 最小订购量（MOQ）
- 公司成立年限
- 供应商资质（如金牌认证、Trade Assurance 等）

通知用户：`✓ 第 3 阶段完成 — 共找到了 [N] 家供应商`

---

## ═════════════════════════════════════
## 第 4 阶段 — PPC 关键词研究
## ═════════════════════════════════

如果提供了竞争对手的 ASIN，或者第 1 阶段找到了 ASIN，执行以下操作：
```
mcp__launchfast__amazon_keyword_research(asins: ["B0...", ...])
```

**报告提取内容：**
- 找到的唯一关键词总数
- 搜索量最高的 20 个关键词
- 搜索量高且竞争较小的精确匹配关键词（Top 5）
- 可用的预估 CPC（每点击费用）
- 推荐的广告活动结构

如果未找到 ASIN，请在报告中注明：“进行 PPC 研究需要竞争对手的 ASIN，请添加相关 ASIN 以继续此阶段。”

通知用户：`✓ 第 4 阶段完成 — 已提取了 [N] 个关键词`

---

## ═════════════════════════════════════
## 第 5 阶段 — 生成 HTML 报告
## ═══════════════════════════════════

生成一个独立的 HTML 文件，并将其保存到第 1 步中指定的路径。

### 报告设计规范

严格遵循 LaunchFast 的设计要求：
- 字体：`-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', system-ui, sans-serif`
- 文本颜色：`#1a1a1a` | 暗淡文本颜色：`#666666` | 非常暗淡的文本颜色：`#999999`
- 背景颜色：`#fafafa` | 卡片背景颜色：`#ffffff`
- 边框颜色：`1px solid #e5e5e5` | 边框圆角：`8px`
- 强调文本的边框颜色：`border-left: 3px solid #1a1a1a`
- 项目符号样式：6px 圆形边框，背景颜色 `#1a1a1a`，圆角 `50%`
- **可行** 标志：`background: #dcfce7; color: #166534`
- **需要进一步调查** 标志：`background: #fef9c3; color: #854d0e`
- **不可行** 标志：`background: #fee2e2; color: #991b1b`
- **商标冲突低** 标志：`background: #dcfce7; color: #166534`
- **商标冲突中** 标志：`background: #fef9c3; color: #854d0e`
- **商标冲突高** 标志：`background: #fee2e2; color: #991b`

### HTML 报告模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>LaunchFast Research Report — [Keyword] — [Date]</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', system-ui, sans-serif;
      background: #fafafa;
      color: #1a1a1a;
      line-height: 1.5;
      padding: 40px 20px;
    }
    .page { max-width: 960px; margin: 0 auto; }

    /* Header */
    .report-header { margin-bottom: 40px; }
    .report-header .brand { font-size: 13px; font-weight: 600; color: #999; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px; }
    .report-header h1 { font-size: 32px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 8px; }
    .report-header .meta { font-size: 14px; color: #666; }

    /* Verdict banner */
    .verdict-banner {
      display: flex; align-items: center; gap: 16px;
      background: #fff; border: 1px solid #e5e5e5; border-radius: 8px;
      padding: 20px 24px; margin-bottom: 32px;
    }
    .verdict-banner .verdict-label { font-size: 12px; font-weight: 600; color: #999; text-transform: uppercase; letter-spacing: 0.06em; }
    .verdict-banner .verdict-value { font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }
    .verdict-banner .divider { width: 1px; height: 40px; background: #e5e5e5; }
    .verdict-banner .stat { }
    .verdict-banner .stat-label { font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.05em; }
    .verdict-banner .stat-value { font-size: 18px; font-weight: 600; letter-spacing: -0.01em; }

    /* Section */
    .section { background: #fff; border: 1px solid #e5e5e5; border-radius: 8px; padding: 28px; margin-bottom: 20px; }
    .section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #e5e5e5; }
    .section-title { font-size: 16px; font-weight: 600; letter-spacing: -0.01em; }
    .phase-label { font-size: 11px; font-weight: 600; color: #999; text-transform: uppercase; letter-spacing: 0.08em; }

    /* Tables */
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th { text-align: left; font-size: 11px; font-weight: 600; color: #999; text-transform: uppercase; letter-spacing: 0.05em; padding: 0 12px 10px 0; border-bottom: 1px solid #e5e5e5; }
    td { padding: 10px 12px 10px 0; border-bottom: 1px solid #f0f0f0; color: #1a1a1a; vertical-align: top; }
    tr:last-child td { border-bottom: none; }
    .grade { font-weight: 700; font-size: 15px; }
    .grade-a { color: #166534; }
    .grade-b { color: #1d4ed8; }
    .grade-c { color: #92400e; }
    .grade-d, .grade-f { color: #991b1b; }

    /* Badges */
    .badge { display: inline-block; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.03em; }
    .badge-go { background: #dcfce7; color: #166534; }
    .badge-investigate { background: #fef9c3; color: #854d0e; }
    .badge-pass { background: #fee2e2; color: #991b1b; }
    .badge-low { background: #dcfce7; color: #166534; }
    .badge-medium { background: #fef9c3; color: #854d0e; }
    .badge-high { background: #fee2e2; color: #991b1b; }
    .badge-clear { background: #dcfce7; color: #166534; }
    .badge-caution { background: #fef9c3; color: #854d0e; }
    .badge-blocked { background: #fee2e2; color: #991b1b; }

    /* Callout */
    .callout { background: #fafafa; border-left: 3px solid #1a1a1a; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-size: 14px; color: #444; }
    .callout strong { color: #1a1a1a; }

    /* Stats grid */
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-bottom: 20px; }
    .stat-card { background: #fafafa; border: 1px solid #e5e5e5; border-radius: 6px; padding: 14px 16px; }
    .stat-card .label { font-size: 11px; font-weight: 600; color: #999; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
    .stat-card .value { font-size: 20px; font-weight: 700; letter-spacing: -0.02em; }
    .stat-card .sub { font-size: 12px; color: #666; margin-top: 2px; }

    /* Supplier score bar */
    .score-bar { display: flex; align-items: center; gap: 8px; }
    .score-bar .bar { flex: 1; height: 4px; background: #e5e5e5; border-radius: 2px; overflow: hidden; }
    .score-bar .fill { height: 100%; background: #1a1a1a; border-radius: 2px; }
    .score-bar .num { font-size: 12px; font-weight: 600; color: #1a1a1a; min-width: 28px; text-align: right; }

    /* Footer */
    .report-footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e5e5; display: flex; justify-content: space-between; align-items: center; }
    .report-footer .brand-mark { font-size: 13px; font-weight: 600; color: #1a1a1a; }
    .report-footer .generated { font-size: 12px; color: #999; }
  </style>
</head>
<body>
<div class="page">

  <!-- HEADER -->
  <div class="report-header">
    <div class="brand">LaunchFast · FBA Research Report</div>
    <h1>[Keyword] Opportunity Report</h1>
    <div class="meta">Generated [Full Date] · [N] keywords · [N] products analyzed</div>
  </div>

  <!-- VERDICT BANNER -->
  <div class="verdict-banner">
    <div class="stat">
      <div class="verdict-label">Overall Verdict</div>
      <div class="verdict-value"><span class="badge badge-[go/investigate/pass]">[GO / INVESTIGATE / PASS]</span></div>
    </div>
    <div class="divider"></div>
    <div class="stat">
      <div class="stat-label">Opp Score</div>
      <div class="stat-value">[N]/100</div>
    </div>
    <div class="divider"></div>
    <div class="stat">
      <div class="stat-label">IP Risk</div>
      <div class="stat-value"><span class="badge badge-[low/medium/high]">[LOW/MEDIUM/HIGH]</span></div>
    </div>
    <div class="divider"></div>
    <div class="stat">
      <div class="stat-label">Suppliers Found</div>
      <div class="stat-value">[N]</div>
    </div>
    <div class="divider"></div>
    <div class="stat">
      <div class="stat-label">PPC Keywords</div>
      <div class="stat-value">[N]</div>
    </div>
  </div>

  <!-- PHASE 1: PRODUCT RESEARCH -->
  <div class="section">
    <div class="section-header">
      <div class="section-title">Product Research</div>
      <div class="phase-label">Phase 1</div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="label">Products Analyzed</div>
        <div class="value">[N]</div>
      </div>
      <div class="stat-card">
        <div class="label">Top Revenue</div>
        <div class="value">$[X]k<span style="font-size:14px;font-weight:500">/mo</span></div>
      </div>
      <div class="stat-card">
        <div class="label">Price Range</div>
        <div class="value">$[X]–$[X]</div>
      </div>
      <div class="stat-card">
        <div class="label">Avg Reviews</div>
        <div class="value">[N]</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Product</th>
          <th>Grade</th>
          <th>Revenue/mo</th>
          <th>Price</th>
          <th>Reviews</th>
          <th>BSR</th>
        </tr>
      </thead>
      <tbody>
        <!-- Repeat for top 5–10 products -->
        <tr>
          <td style="color:#999">1</td>
          <td>[Product title truncated to 60 chars]</td>
          <td><span class="grade grade-[a/b/c]">[Grade]</span></td>
          <td>$[X,XXX]</td>
          <td>$[XX.XX]</td>
          <td>[X,XXX]</td>
          <td>#[X,XXX]</td>
        </tr>
      </tbody>
    </table>

    <div class="callout" style="margin-top:20px">
      <strong>Key finding:</strong> [1-2 sentence insight about the market — grade distribution, revenue consistency, competitive dynamics]
    </div>
  </div>

  <!-- PHASE 2: IP CHECK -->
  <div class="section">
    <div class="section-header">
      <div class="section-title">IP & Trademark Check</div>
      <div class="phase-label">Phase 2</div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="label">IP Risk Level</div>
        <div class="value"><span class="badge badge-[low/medium/high]">[LOW/MEDIUM/HIGH]</span></div>
      </div>
      <div class="stat-card">
        <div class="label">Active Trademarks</div>
        <div class="value">[N]</div>
      </div>
      <div class="stat-card">
        <div class="label">Patent Hits</div>
        <div class="value">[N]</div>
      </div>
      <div class="stat-card">
        <div class="label">Assessment</div>
        <div class="value"><span class="badge badge-[clear/caution/blocked]">[CLEAR/CAUTION/BLOCKED]</span></div>
      </div>
    </div>

    <!-- If trademarks found, show table -->
    <table>
      <thead>
        <tr><th>Trademark</th><th>Owner</th><th>Status</th><th>Class</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>[Trademark name]</td>
          <td>[Owner]</td>
          <td>[Live/Dead]</td>
          <td>[Class number]</td>
        </tr>
      </tbody>
    </table>

    <div class="callout" style="margin-top:20px">
      <strong>Recommendation:</strong> [Clear action — e.g. "No direct conflicts found. Avoid branding your product as [word] to stay safe." or "HIGH risk — consult an IP attorney before proceeding."]
    </div>
  </div>

  <!-- PHASE 3: SUPPLIER RESEARCH -->
  <div class="section">
    <div class="section-header">
      <div class="section-title">Alibaba Supplier Research</div>
      <div class="phase-label">Phase 3</div>
    </div>

    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Supplier</th>
          <th>Score</th>
          <th>Price Range</th>
          <th>MOQ</th>
          <th>Years</th>
          <th>Verified</th>
        </tr>
      </thead>
      <tbody>
        <!-- Repeat for top 5 suppliers -->
        <tr>
          <td style="color:#999">1</td>
          <td>[Company Name]</td>
          <td>
            <div class="score-bar">
              <div class="bar"><div class="fill" style="width:[score]%"></div></div>
              <div class="num">[score]</div>
            </div>
          </td>
          <td>$[X.XX]–$[X.XX]</td>
          <td>[N] units</td>
          <td>[N] yrs</td>
          <td>[Gold · TA · Assessed]</td>
        </tr>
      </tbody>
    </table>

    <div class="callout" style="margin-top:20px">
      <strong>Top pick:</strong> [Company Name] — [reason: highest score, most verifications, best price range for target margin]
    </div>
  </div>

  <!-- PHASE 4: PPC KEYWORDS -->
  <div class="section">
    <div class="section-header">
      <div class="section-title">PPC Keyword Intelligence</div>
      <div class="phase-label">Phase 4</div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="label">Total Keywords</div>
        <div class="value">[N]</div>
      </div>
      <div class="stat-card">
        <div class="label">Tier 1 (Priority)</div>
        <div class="value">[N]</div>
      </div>
      <div class="stat-card">
        <div class="label">Tier 2 (Growth)</div>
        <div class="value">[N]</div>
      </div>
      <div class="stat-card">
        <div class="label">Tier 3 (Discovery)</div>
        <div class="value">[N]</div>
      </div>
    </div>

    <table>
      <thead>
        <tr><th>#</th><th>Keyword</th><th>Search Vol</th><th>Tier</th><th>Match Types</th><th>Est. CPC</th></tr>
      </thead>
      <tbody>
        <!-- Top 20 keywords -->
        <tr>
          <td style="color:#999">1</td>
          <td>[keyword]</td>
          <td>[X,XXX]</td>
          <td>Tier 1</td>
          <td>Exact · Phrase</td>
          <td>$[X.XX]</td>
        </tr>
      </tbody>
    </table>

    <div class="callout" style="margin-top:20px">
      <strong>Campaign strategy:</strong> [Brief recommendation — e.g. "Start with the 12 Tier 1 exact-match keywords at $0.90 bid. Run broad on Tier 3 for discovery data. Revisit in 2 weeks."]
    </div>
  </div>

  <!-- FOOTER -->
  <div class="report-footer">
    <div class="brand-mark">LaunchFast</div>
    <div class="generated">Generated [Date] · Data via LaunchFast MCP</div>
  </div>

</div>
</body>
</html>
```

使用研究阶段获得的实际数据填充所有占位符（`[...]`）。
将完整的报告文件保存到第 1 步中指定的路径。

---

## 第 6 步 — 向用户总结

保存报告文件后：
```
## Research Complete ✓

Report saved to: [file path]

Quick summary:
- Keyword: [keyword]
- Verdict: [GO / INVESTIGATE / PASS] (Score: [N]/100)
- IP Risk: [LOW / MEDIUM / HIGH]
- Best supplier: [Company Name] ($X.XX–$X.XX/unit, MOQ: N)
- PPC keywords found: [N] (Tier 1: N | Tier 2: N | Tier 3: N)

Next steps:
[If GO]: Ready to contact suppliers? Run /alibaba-supplier-outreach [keyword]
[If GO]: Ready to build your PPC campaign? Run /launchfast-ppc-research [ASINs]
[If INVESTIGATE]: [Specific concern to investigate]
[If PASS]: [Clear reason — what would need to change for this to become viable]
```