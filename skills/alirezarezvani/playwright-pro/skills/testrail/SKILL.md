---
name: testrail
description: 将测试结果与 TestRail 同步。当用户提到“TestRail”、“测试管理”、“测试用例”、“测试运行”、“同步测试用例”、“将结果推送至 TestRail”或“从 TestRail 导入测试用例”时，请使用此功能。
  Sync tests with TestRail. Use when user mentions "testrail", "test management",
  "test cases", "test run", "sync test cases", "push results to testrail",
  or "import from testrail".
---
# TestRail集成

Playwright测试与TestRail测试管理之间的双向同步功能。

## 前提条件

必须设置以下环境变量：
- `TESTRAIL_URL` — 例如：`https://your-instance.testrail.io`
- `TESTRAIL_USER` — 你的电子邮件地址
- `TESTRAIL_API_KEY` — 来自TestRail的API密钥

如果这些变量未设置，请告知用户如何配置它们，然后停止继续。

## 功能

### 1. 导入测试用例 → 生成Playwright测试

```
/pw:testrail import --project <id> --suite <id>
```

步骤：
1. 调用`testrail_get_cases` MCP工具来获取测试用例。
2. 对于每个测试用例：
   - 读取标题、前置条件、步骤和预期结果。
   - 使用相应的模板将其映射到Playwright测试中。
   - 将TestRail用例ID作为测试注释添加：`test.info().annotations.push({ type: 'testrail', description: 'C12345' })`
3. 按章节分组生成测试文件。
4. 报告：导入的测试用例数量为X个，生成的Playwright测试数量为Y个。

### 2. 将测试结果推送至TestRail

```
/pw:testrail push --run <id>
```

步骤：
1. 使用JSON报告器运行Playwright测试：
   ```bash
   npx playwright test --reporter=json > test-results.json
   ```
2. 解析测试结果：将每个测试的结果与其对应的TestRail用例ID关联起来。
3. 对每个测试调用`testrail_add_result` MCP工具：
   - 如果测试通过 → 状态码：1
   - 如果测试失败 → 状态码：5，并包含错误信息
   - 如果测试被跳过 → 状态码：2
4. 报告：推送的结果数量为X个，其中Y个通过，Z个失败。

### 3. 创建测试运行

```
/pw:testrail run --project <id> --name "Sprint 42 Regression"
```

步骤：
1. 调用`testrail_add_run` MCP工具。
2. 包含Playwright测试注释中所有的测试用例ID。
3. 返回用于推送结果的运行ID。

### 4. 同步状态

```
/pw:testrail status --project <id>
```

步骤：
1. 从TestRail获取测试用例信息。
2. 扫描本地的Playwright测试以查找TestRail注释。
3. 报告测试覆盖率：

### 5. 更新TestRail中的测试用例

```
/pw:testrail update --case <id>
```

步骤：
1. 读取对应于该用例ID的Playwright测试内容。
2. 从测试代码中提取步骤和预期结果。
3. 调用`testrail_update_case` MCP工具来更新测试用例信息。

## 使用的MCP工具

| 工具 | 使用场景 |
|---|---|
| `testrail_get_projects` | 列出可用的项目 |
| `testrail_get_suites` | 列出项目中的测试套件 |
| `testrail_get_cases` | 读取测试用例信息 |
| `testrail_add_case` | 创建新的测试用例 |
| `testrail_update_case` | 更新现有测试用例 |
| `testrail_add_run` | 创建测试运行记录 |
| `testrail_add_result` | 推送单个测试结果 |
| `testrail_get_results` | 查看历史测试结果 |

## TestRail注释格式

所有与TestRail关联的Playwright测试都包含以下注释：

```typescript
test('should login successfully', async ({ page }) => {
  test.info().annotations.push({
    type: 'testrail',
    description: 'C12345',
  });
  // ... test code
});
```

此注释是Playwright与TestRail之间的桥梁。

## 输出

- 操作摘要及统计信息
- 任何错误或未匹配的测试用例
- 链接到TestRail的测试运行结果页面