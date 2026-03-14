---
name: "report"
description: 生成测试报告。当用户请求“测试报告”、“结果摘要”、“测试状态”、“显示结果”、“测试仪表板”或“测试进展如何”时，请使用此功能。
  Generate test report. Use when user says "test report", "results summary",
  "test status", "show results", "test dashboard", or "how did tests go".
---
# 智能测试报告系统

该系统能够生成可集成到用户现有工作流程中的测试报告，无需引入任何新工具。

## 步骤

### 1. 运行测试（如果尚未运行）

检查是否有最新的测试结果：

```bash
ls -la test-results/ playwright-report/ 2>/dev/null
```

如果没有最新的测试结果，请运行测试：

```bash
npx playwright test --reporter=json,html,list 2>&1 | tee test-output.log
```

### 2. 解析测试结果

读取 JSON 格式的测试报告：

```bash
npx playwright test --reporter=json 2> /dev/null
```

提取以下信息：
- 总测试数量、通过的数量、失败的数量、跳过的数量以及“不稳定”（flaky）的测试数量
- 单个测试的运行时间以及总运行时间
- 失败的测试名称及其错误信息
- 在重试后仍失败的测试（即“不稳定”的测试）

### 3. 确定报告的发送目标

根据配置自动将报告发送到指定的位置：

| 检查项 | 是否存在 | 应采取的行动 |
|---|---|---|
| `TESTRAIL_URL` 环境变量 | TestRail 已配置 | 通过 `/pw:testrail push` 命令推送报告 |
| `SLACK_WEBHOOK_URL` 环境变量 | Slack 已配置 | 将报告摘要发布到 Slack |
| `.github/workflows/` | GitHub Actions | 将报告内容通过工件（artifacts）添加到 Pull Request 的评论中 |
| `playwright-report/` | HTML 格式的报告工具 | 打开或提供 HTML 格式的报告 |
| 以上选项均不存在 | 默认设置 | 生成 Markdown 格式的报告 |

### 4. 生成报告

#### Markdown 格式的报告（始终生成）

```markdown
# Test Results — {{date}}

## Summary
- ✅ Passed: {{passed}}
- ❌ Failed: {{failed}}
- ⏭️ Skipped: {{skipped}}
- 🔄 Flaky: {{flaky}}
- ⏱️ Duration: {{duration}}

## Failed Tests
| Test | Error | File |
|---|---|---|
| {{name}} | {{error}} | {{file}}:{{line}} |

## Flaky Tests
| Test | Retries | File |
|---|---|---|
| {{name}} | {{retries}} | {{file}} |

## By Project
| Browser | Passed | Failed | Duration |
|---|---|---|---|
| Chromium | X | Y | Zs |
| Firefox | X | Y | Zs |
| WebKit | X | Y | Zs |
```

将报告保存到 `test-reports/{{date}}-report.md` 文件中。

#### 如果配置了 Slack Webhook，则生成 Slack 总结信息

```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "🧪 Test Results: ✅ {{passed}} | ❌ {{failed}} | ⏱️ {{duration}}\n{{failed_details}}"
  }'
```

#### 如果配置了 TestRail，则将报告推送到 TestRail

使用 `/pw:testrail push` 命令发送 JSON 格式的测试结果。

#### 如果使用了 Playwright 报告工具，则生成 HTML 格式的报告

```bash
npx playwright show-report
```

#### 如果在持续集成（CI）环境中运行，则执行相应的操作

```bash
echo "HTML report available at: playwright-report/index.html"
```

### 5. 数据趋势分析（如果存在历史数据）

如果 `test-reports/` 目录中存在之前的报告：
- 分析测试通过率的变化趋势
- 识别最近出现问题的测试
- 突出显示新出现的失败测试以及反复失败的测试

## 输出内容：

- 测试结果总结（包括通过、失败、跳过和“不稳定”测试的数量）
- 失败测试的详细信息及其错误信息
- 报告的发送目标确认信息
- 测试结果的趋势分析（如果有历史数据）
- 下一步建议（修复失败的问题或庆祝测试通过）