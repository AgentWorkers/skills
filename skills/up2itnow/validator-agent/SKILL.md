# 验证器代理（Validator Agent）

这是一个针对 TypeScript/Solidity 项目的多轮自动化验证流程。在项目发布或部署之前，会执行 8 轮验证：编译检查、代码风格检查（lint）、测试套件测试、安全审计、类型覆盖率检查、文档验证、变更日志检查以及最终审核。

**这堪称黄金标准**——能够发现人工审核可能遗漏的问题。该工具最初是为在每次通过 npm 发布之前验证 `agent-wallet-sdk` 而开发的，现在可作为通用工具用于任何项目。

## 使用场景

- 在执行 `npm publish` 之前：运行完整的 8 轮验证流程。
- 在合并 Pull Request（PR）之前：作为质量检查环节。
- 在依赖项更新之后：确保没有出现功能退化。
- 适用于工作区中的任何 TypeScript 或 Solidity 项目。

## 快速入门

```
Run the Validator Agent on skills/agent-nexus-2/agent-wallet-sdk
```

或者，您可以单独触发特定的验证轮次：

```
Run Validator Agent round 0 (compile gate) on projects/mastra-plugin
```

## 8 轮验证流程

### 第 0 轮 — 编译检查（此轮失败将阻止后续所有轮次）
```bash
cd <project> && npx tsc --noEmit 2>&1
```
**如果编译失败，所有后续轮次都将被阻止。**只有在编译成功后，流程才会继续进行。这一环节是在 2 月份发生错误（错误的类型被发布到 npm）之后新增的。

### 第 1 轮 — 代码风格检查（Lint）
```bash
cd <project> && npm run lint 2>&1 | tail -20
```
检查代码风格是否存在问题。警告会被记录下来，但不会阻止流程继续；只有错误才会导致流程中断。

### 第 2 轮 — 测试套件测试
```bash
cd <project> && npm test 2>&1
```
记录测试的总数、通过的数量、失败的数量以及被跳过的测试。如果存在 `ops/test-baselines.md` 文件，会与基准数据进行比较。**任何测试数量的减少都可能表示功能退化，此时流程将被阻止。**

### 第 3 轮 — 安全审计
```bash
cd <project> && npm audit 2>&1 | tail -15
```
- 无安全漏洞 → ✅ 通过
- 仅有中等风险的安全问题（传递性风险）→ ⚠️ 警告（需要关注，但不会阻止流程继续）
- 高风险或严重风险 → 🚨 阻止发布

### 第 4 轮 — 类型覆盖率检查
```bash
cd <project> && npx type-coverage 2>&1 || echo "type-coverage not installed — skip"
```
如果支持类型覆盖率检测，会报告覆盖率。目标覆盖率应大于 95%；低于 90% 时将发出警告。

### 第 5 轮 — 文档验证
- `README.md` 是否存在，并且引用了当前版本的信息？
- `CHANGELOG.md` 中是否记录了当前版本的相关变更？
- 所有导出的函数是否都有相应的文档？

### 第 6 轮 — 变更日志验证
- 查看 `package.json` 中的版本信息。
- 查看 `CHANGELOG.md`，确认其中是否记录了当前版本的变更信息。
- 如果当前版本没有对应的变更日志记录，则阻止发布。

### 第 7 轮 — 最终审核总结
将所有轮次的检查结果汇总成一个综合判断：

```
# Validator Agent Report — [project] — [timestamp]

## Verdict: [✅ PASS / ⚠️ WARN / 🚨 BLOCK]

| Round | Check | Result |
|-------|-------|--------|
| 0 | Compile | ✅/❌ |
| 1 | Lint | ✅/⚠️/❌ |
| 2 | Tests | ✅ X/X passing / ❌ regression |
| 3 | Security | ✅/⚠️/🚨 |
| 4 | Type Coverage | ✅ X% / ⚠️ / skipped |
| 5 | Docs | ✅/⚠️ |
| 6 | Changelog | ✅/❌ |
| 7 | Summary | [verdict] |

## Blocking Issues
[list or "None"]

## Warnings
[list or "None"]

## Recommendation
[PUBLISH / FIX FIRST / DO NOT PUBLISH]
```

将验证报告保存到：`ops/reports/validator-YYYY-MM-DD-HH-[project].md`

## 配置

该工具会根据以下文件自动识别项目类型：
- `package.json`：判断项目类型为 TypeScript/Node 项目
- `foundry.toml`：判断项目类型为 Solidity/Forge 项目

对于 Solidity 项目，第 0 轮会使用 `forge build` 而不是 `tsc` 进行编译；第 2 轮会使用 `forge test` 进行测试；第 3 轮会使用 `forge audit`（如果 `slither` 工具可用的话）进行安全审计。

## 权限说明
- 该工具仅具有 **读取权限**——它仅负责检查并生成报告，不会修改代码。
- 它会给出建议，但不会自动执行发布操作。
- 在查看报告后，必须由 Max 或 Bill 批准才能继续发布项目。