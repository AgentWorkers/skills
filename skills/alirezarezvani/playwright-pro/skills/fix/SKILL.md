---
name: fix
description: 修复那些失败或运行不稳定的 Playwright 测试。当用户反馈“修复测试”、“测试运行不稳定”、“测试失败”、“调试测试”、“测试出错”或“测试有时能通过”时，请使用此方法。
  Fix failing or flaky Playwright tests. Use when user says "fix test",
  "flaky test", "test failing", "debug test", "test broken", "test passes
  sometimes", or "intermittent failure".
---
# 修复失败或不稳定运行的测试

使用系统的分类方法来诊断并修复那些时有时无地失败或正常运行的 Playwright 测试。

## 输入

`$ARGUMENTS` 包含以下内容：
- 测试文件路径：`e2e/login.spec.ts`
- 测试名称：`"登录后应重定向"`
- 描述：`“结账测试在持续集成（CI）环境中失败，但在本地环境中通过”`

## 步骤

### 1. 重现故障

运行测试以捕获错误：

```bash
npx playwright test <file> --reporter=list
```

如果测试正常通过，那么很可能是由于测试结果不稳定（即“flaky”）。接下来执行“burn-in”测试：

```bash
npx playwright test <file> --repeat-each=10 --reporter=list
```

如果测试仍然正常通过，尝试使用并行执行机制：

```bash
npx playwright test --fully-parallel --workers=4 --repeat-each=5
```

### 2. 捕获日志痕迹

以全日志模式运行测试：

```bash
npx playwright test <file> --trace=on --retries=0
```

阅读日志输出。如果可用，请使用 `/debug` 命令分析日志文件。

### 3. 对故障进行分类

从 `flaky-taxonomy.md` 文件中查找对应的故障分类。

所有失败的测试都属于以下四个类别之一：

| 类别 | 症状 | 诊断方法 |
|---|---|---|
| **时间/异步问题** | 在所有环境中都时有时无地失败 | 使用 `--repeat-each=20` 在本地环境中重现故障 |
| **测试隔离问题** | 在测试套件中失败，单独运行时通过 | 使用 `--workers=1 --grep "测试名称"` 重新运行测试 |
| **环境问题** | 在持续集成环境中失败，在本地环境中通过 | 比较持续集成环境和本地环境的截图/日志 |
| **基础设施问题** | 失败具有随机性，没有规律 | 错误信息中可能包含浏览器内部的详细信息 |

### 4. 实施针对性的修复措施

**时间/异步问题：**
- 将 `waitForTimeout()` 替换为基于网络响应的断言方法
- 为缺失的 Playwright 调用添加 `await` 语句
- 在进行断言之前等待特定的网络响应
- 在与元素交互之前使用 `toBeVisible()` 方法确认元素已可见

**测试隔离问题：**
- 移除测试之间的共享可变状态
- 通过 API 或测试 fixture 为每次测试生成唯一的测试数据
- 使用唯一的标识符（如时间戳、随机字符串）作为测试数据
- 检查数据库状态是否泄漏

**环境问题：**
- 确保本地环境和持续集成环境中的视口大小一致
- 考虑截图中的字体渲染差异
- 在本地环境中使用 `docker` 来模拟持续集成环境
- 检查与时区相关的断言是否正确

**基础设施问题：**
- 增加持续集成环境的超时时间
- 在持续集成配置中添加重试机制（例如 `retries: 2`）
- 检查浏览器是否出现内存溢出（OOM）现象（适当减少并行执行的测试数量）
- 确保所有必要的浏览器依赖项都已安装

### 5. 验证修复效果

运行测试 10 次以确保修复后的稳定性：

```bash
npx playwright test <file> --repeat-each=10 --reporter=list
```

所有 10 次测试都必须通过。如果有任何测试失败，请返回步骤 3。

### 6. 防止问题再次发生

建议采取以下措施：
- 如果尚未设置，将重试机制添加到持续集成配置中（例如 `retries: 2`）
- 在配置中启用 `trace: 'on-first-retry'` 选项
- 将修复方法添加到项目的测试规范文档中

## 输出结果
- 故障的根本原因及具体问题
- 所采取的修复措施（包括代码差异）
- 测试验证结果（10 次全部通过）
- 防止问题再次发生的建议