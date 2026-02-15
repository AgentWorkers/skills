---
name: github-actions-troubleshooting
description: "**GitHub Actions 工作流故障排除**  
（特别是针对 Go 项目）  

**一、诊断故障的工作流**  
当 GitHub Actions 工作流出现故障时，首先需要对其进行详细诊断。区分故障是由代码问题引起的，还是由环境配置问题导致的。  

**二、分析日志**  
通过查看工作流的日志文件（通常位于 `./logs` 目录下），可以获取有关故障的详细信息。这些日志包含了运行过程中的错误信息、警告以及执行步骤的详细记录。仔细分析日志有助于确定问题的根源。  

**三、解决常见 CI/CD 问题**  
针对常见的 CI/CD 问题，可以采取以下解决方法：  
1. **检查代码问题**：确保所有相关的 Go 代码都符合项目的编码规范和标准。使用代码审查工具（如 GoLint）来检查代码质量。  
2. **检查环境配置**：确保所有必要的环境变量都已正确设置，并且与项目的依赖项相匹配。  
3. **优化构建过程**：优化构建脚本（`Dockerfile` 或 `build.gradle` 等），以减少构建时间并避免不必要的步骤。  
4. **调整依赖管理**：使用最新的依赖包版本，并确保依赖项之间的兼容性。  
5. **优化部署过程**：检查部署脚本（`DeployScript` 或 `Pipeline.yml` 等），确保部署逻辑正确无误。  

**四、应用修复措施**  
根据诊断结果，应用相应的修复措施。这可能包括：  
- 修复代码中的错误；  
- 更新环境配置；  
- 优化构建和部署流程；  
- 调整依赖管理策略。  

**五、预防类似问题**  
为了避免类似问题的再次发生，可以采取以下措施：  
- 定期审查和维护工作流配置；  
- 监控工作流的运行状态，及时发现潜在问题；  
- 为关键步骤添加日志记录和错误处理机制；  
- 参考官方文档和社区资源，了解最佳实践。  

通过以上步骤，您可以有效地排查和解决 GitHub Actions 工作流中的故障，确保项目的持续集成和持续部署过程顺利进行。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "requires": { "bins": ["gh", "git"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (apt)",
            },
          ],
      },
  }
---

# GitHub Actions 故障排除技巧

使用 `gh` CLI 和 Git 来诊断和修复 GitHub Actions 工作流的故障，尤其是针对 Go 项目。该技巧有助于判断故障是由于代码问题还是环境/配置问题引起的。

## 工作流分析

查看最近的工作流运行状态：

```bash
gh run list --repo owner/repo --limit 10
```

查看特定失败工作流的详细信息：

```bash
gh run view <run-id> --repo owner/repo
```

仅获取失败任务的日志：

```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## 区分问题类型

1. **代码问题**：在所有环境中都一致出现的编译、测试或代码检查（linting）失败。
2. **环境问题**：与依赖项解析、工具安装或本地 CI 中的类型检查相关的问题。

## 常见的 Go CI 修复方法

### 代码检查（Linting）配置问题
- 寻找表示导入解析问题的 “undefined” 引用错误。
- 尝试使用不启用类型检查的简化配置文件。
- 使用 `golangci-lint run --disable-all --enable=gofmt` 进行基本的语法检查。

### 依赖项解析问题
- 确认 `go.mod` 和 `go.sum` 文件是否一致。
- 运行 `go mod tidy` 来解决依赖项冲突。
- 检查是否正确声明了所需的依赖项。

## 诊断命令

查看特定工作流任务的日志：

```bash
gh run view --job <job-id> --repo owner/repo
```

下载工作流生成的文件以供检查：

```bash
gh run download <run-id> --repo owner/repo
```

## 故障排除步骤

1. 确定哪些任务失败了，哪些任务成功了。
2. 查看错误信息以获取问题的线索。
3. 判断问题是否可以在本地重现。
4. 根据问题类型进行针对性的修复。
5. 监控后续的工作流运行情况，以验证问题是否已解决。