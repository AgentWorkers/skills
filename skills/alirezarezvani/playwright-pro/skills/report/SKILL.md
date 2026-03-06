---
name: report
description: 生成测试报告。当用户请求“测试报告”、“结果摘要”、“测试状态”、“显示结果”、“测试仪表盘”或“测试进展如何”时，请使用该报告。
  Generate test report. Use when user says "test report", "results summary",
  "test status", "show results", "test dashboard", or "how did tests go".
---
# 智能测试报告生成

生成能够集成到用户现有工作流程中的测试报告，无需使用任何新工具。

## 步骤

### 1. 运行测试（如果尚未运行）

检查是否存在最近的测试结果：

```bash
ls -la test-results/ playwright-report/ 2>/dev/null
```

如果没有最近的测试结果，请运行测试：

```bash
npx playwright test --reporter=json,html,list 2>&1 | tee test-output.log
```

### 2. 解析测试结果

读取 JSON 格式的测试报告：

```bash
npx playwright test --reporter=json 2> /dev/null
```

提取以下信息：
- 总测试数量、通过的数量、失败的数量、跳过的数量以及出现不稳定行为的测试数量
- 每个测试的耗时及总耗时
- 失败的测试名称及其错误信息
- 出现不稳定行为的测试（在重试后仍失败）

### 3. 确定报告的发送目的地

检查系统配置，并自动将报告发送到指定位置：

| 检查项 | 是否存在 | 执行操作 |
|---|---|---|
| `TESTRAIL_URL` 环境变量 | 配置了 TestRail | 通过 `/pw:testrail push` 命令推送报告 |
| `SLACK_WEBHOOK_URL` 环境变量 | 配置了 Slack | 将报告摘要发送到 Slack |
| `.github/workflows/` | 配置了 GitHub Actions | 将报告通过工件（artifacts）添加到 Pull Request 的评论中 |
| `playwright-report/` | 配置了 HTML 报告工具 | 打开或提供 HTML 格式的报告 |
| 以上选项均不存在 | 使用默认方式 | 生成 Markdown 格式的报告 |

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

#### 如果配置了 Slack Webhook，则生成 Slack 总结：

```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "🧪 Test Results: ✅ {{passed}} | ❌ {{failed}} | ⏱️ {{duration}}\n{{failed_details}}"
  }'
```

#### 如果配置了 TestRail，则推送报告：

使用 `/pw:testrail push` 命令发送 JSON 格式的报告。

#### HTML 格式的报告：

```bash
npx playwright show-report
```

或者在持续集成（CI）环境中：

```bash
echo "HTML report available at: playwright-report/index.html"
```

### 5. 数据趋势分析（如果存在历史数据）

如果 `test-reports/` 目录下有之前的报告：
- 分析测试通过率的变化趋势
- 识别近期出现不稳定行为的测试
- 突出显示新出现的失败测试和反复失败的测试

## 输出内容

- 测试结果总结（包括通过、失败、跳过和出现不稳定行为的测试数量）
- 失败测试的详细信息及其错误信息
- 报告的发送目的地确认信息
- 测试结果的趋势分析（如果存在历史数据）
- 下一步建议（修复失败的问题或庆祝测试通过）