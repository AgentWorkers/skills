---
name: code-tester
description: 构建、运行并测试 Rust、Go 和 Java 语言的代码项目。自动检测项目类型；如果存在单元测试，则运行这些测试，并报告构建状态。在代码修改后使用该工具来验证项目是否能够成功构建，单元测试是否通过，以及应用程序是否能够无错误地运行。将测试结果反馈给请求方，以便进行修复和重新测试。
metadata: {"clawdbot":{"command":"test_repo"}}
---
# 代码测试工具

用于测试代码项目，以验证构建过程及测试是否通过。

## 工作流程

当收到测试变更的请求时，按照以下步骤操作：

1. **检测项目类型**：
   - Rust项目：`Cargo.toml`文件及`src/`目录
   - Go项目：`go.mod`、`go.sum`文件或`main.go`文件
   - Java项目：`pom.xml`或`build.gradle`/`build.gradle.kts`文件

2. **运行测试**（仅当存在测试脚本时）：
   - 如果未找到测试脚本，则跳过此步骤
   - 运行项目特定的测试命令
   - 记录测试结果

3. **构建项目**：
   - 执行构建命令
   - 记录构建过程中的输出和错误信息

4. **报告结果**：
   - 提供详细的测试结果总结
   - 显示测试是否通过
   - 显示项目的构建状态
   - 报告遇到的任何错误

## 通信协议

当为其他代理执行测试时，请按照以下格式生成报告：

```
Testing: <directory>
Project type: <rust|go|java>
Detected tests: <yes|no>

=== Results ===
✓ Tests: <passed/skipped/failed>
✓/✗ Build: <passed/failed>

<Relevant error messages if any>
```

**如果所有测试都通过：**
- 清晰地报告测试成功的结果
- 提供后续需要执行的步骤

**如果出现错误：**
- 详细报告出错的部分（是测试失败还是构建失败）
- 附上错误日志
- 提出相应的修复建议

## 运行测试

执行测试脚本：

```bash
/root/.openclaw/workspace/skills/code-tester/scripts/test.sh <directory>
```

该脚本将自动完成以下操作：
- 自动检测项目类型
- 运行测试（如果存在测试脚本）
- 构建项目
- 测试成功时返回退出码0，失败时返回退出码1

## 测试策略

- **Rust项目**：`cargo test` → `cargo build`
- **Go项目**：`go test ./...` → `go build`
- **Java（Maven项目）**：`mvn test` → `mvn compile`
- **Java（Gradle项目）**：`./gradlew test` → `./gradlew build -x test`

请始终从项目目录中运行该脚本。脚本会自动完成项目的类型检测及后续操作。