---
name: "testrail"
description: 将测试结果与 TestRail 同步。当用户提到“TestRail”、“测试管理”、“测试用例”、“测试运行”、“同步测试用例”、“将结果推送到 TestRail”或“从 TestRail 导入”时，请使用此功能。
  Sync tests with TestRail. Use when user mentions "testrail", "test management",
  "test cases", "test run", "sync test cases", "push results to testrail",
  or "import from testrail".
---
# TestRail 集成

Playwright 测试与 TestRail 测试管理之间的双向同步功能。

## 前提条件

必须设置以下环境变量：
- `TESTRAIL_URL` — 例如：`https://your-instance.testrail.io`
- `TESTRAIL_USER` — 你的电子邮件地址
- `TESTRAIL_API_KEY` — 来自 TestRail 的 API 密钥

如果这些变量未设置，请告知用户如何配置它们，然后停止继续。

## 功能

### 1. 导入测试用例 → 生成 Playwright 测试

```
/pw:testrail import --project <id> --suite <id>
```

步骤：
1. 调用 `testrail_get_cases` MCP 工具来获取测试用例。
2. 对于每个测试用例：
   - 读取标题、前置条件、步骤和预期结果。
   - 使用相应的模板将其映射到 Playwright 测试中。
   - 将 TestRail 用例 ID 作为测试注释添加：`test.info().annotations.push({ type: 'testrail', description: 'C12345' })`
3. 按章节分组生成测试文件。
4. 报告：导入的测试用例数量为 X，生成的 Playwright 测试数量为 Y。

### 2. 将测试结果推送至 TestRail

```
/pw:testrail push --run <id>
```

步骤：
1. 使用 JSON 报告器运行 Playwright 测试：
   ```bash
   npx playwright test --reporter=json > test-results.json
   ```
2. 解析测试结果：将每个测试的结果与其对应的 TestRail 用例 ID 关联起来。
3. 对于每个测试结果，调用 `testrail_add_result` MCP 工具：
   - 如果测试通过 → 状态码：1
   - 如果测试失败 → 状态码：5，并包含错误信息
   - 如果测试被跳过 → 状态码：2
4. 报告：推送的结果数量为 X，其中 Y 个通过，Z 个失败。

### 3. 创建测试运行记录

```
/pw:testrail run --project <id> --name "Sprint 42 Regression"
```

步骤：
1. 调用 `testrail_add_run` MCP 工具。
2. 包含 Playwright 测试中所有测试用例的 ID。
3. 返回用于推送结果运行的 ID。

### 4. 同步状态

```
/pw:testrail status --project <id>
```

步骤：
1. 从 TestRail 获取测试用例信息。
2. 检查本地 Playwright 测试中是否包含 TestRail 相关的注释。
3. 报告测试覆盖率：

### 5. 更新 TestRail 中的测试用例

```
/pw:testrail update --case <id>
```

步骤：
1. 读取对应 TestRail 用例 ID 的 Playwright 测试代码。
2. 从测试代码中提取步骤和预期结果。
3. 调用 `testrail_update_case` MCP 工具来更新测试用例信息。

## 使用的 MCP 工具

| 工具 | 使用场景 |
|---|---|
| `testrail_get_projects` | 列出可用的项目 |
| `testrail_get_suites` | 列出项目中的测试套件 |
| `testrail_get_cases` | 读取测试用例信息 |
| `testrail_add_case` | 创建新的测试用例 |
| `testrail_update_case` | 更新现有测试用例 |
| `testrail_add_run` | 创建测试运行记录 |
| `testrail_add_result` | 推送单个测试结果 |
| `testrail_get_results` | 读取历史测试结果 |

## TestRail 注释格式

所有与 TestRail 关联的 Playwright 测试都包含以下注释：

```typescript
test('should login successfully', async ({ page }) => {
  test.info().annotations.push({
    type: 'testrail',
    description: 'C12345',
  });
  // ... test code
});
```

该注释起到了 Playwright 与 TestRail 之间的桥梁作用。

## 输出内容

- 操作摘要及相关统计信息
- 任何错误或未匹配的测试用例
- 链接到 TestRail 的测试运行记录页面