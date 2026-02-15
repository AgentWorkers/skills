---
name: go-linter-configuration
description: "配置并排查 Go 项目的 `golangci-lint` 工具。解决导入解析问题、类型检查错误，并针对本地开发和持续集成（CI）环境优化配置。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["go", "golangci-lint"] },
        "install":
          [
            {
              "id": "golang",
              "kind": "script",
              "script": "curl -L https://golang.org/dl/go1.21.5.linux-amd64.tar.gz | tar -C /usr/local -xzf -",
              "bins": ["go"],
              "label": "Install Go",
            },
            {
              "id": "golangci",
              "kind": "script",
              "script": "curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.59.1",
              "bins": ["golangci-lint"],
              "label": "Install golangci-lint",
            },
          ],
      },
  }
---

# Go 代码检查工具配置技巧

本技巧介绍如何配置和排查 golangci-lint 在 Go 项目中的使用问题。该工具有助于解决导入解析问题、类型检查错误，并优化本地开发及持续集成（CI）环境下的配置。

## 安装

安装 golangci-lint：

```bash
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

或者使用官方的安装脚本：

```bash
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.59.1
```

## 基本用法

1. 对整个项目运行代码检查工具：

```bash
golangci-lint run ./...
```

2. 使用特定配置运行代码检查工具：

```bash
golangci-lint run --config .golangci.yml ./...
```

## 配置文件（.golangci.yml）

### 最小配置（适用于存在导入问题的 CI 环境）
```yaml
run:
  timeout: 5m
  tests: false
  build-tags: []

linters:
  disable-all: true
  enable:
    - gofmt          # Format checking only

linters-settings:
  gofmt:
    simplify: true

issues:
  exclude-use-default: false
  max-issues-per-linter: 50
  max-same-issues: 3

output:
  format: tab
```

### 标准配置（适用于本地开发）
```yaml
run:
  timeout: 5m
  tests: true
  build-tags: []

linters:
  enable:
    - gofmt
    - govet
    - errcheck
    - staticcheck
    - unused
    - gosimple
    - ineffassign

linters-settings:
  govet:
    enable:
      - shadow
  errcheck:
    check-type-assertions: true
  staticcheck:
    checks: ["all"]

issues:
  exclude-use-default: false
  max-issues-per-linter: 50
  max-same-issues: 3

output:
  format: tab
```

## 常见问题的排查与解决

### “undefined: package” 错误
问题：代码检查工具报告对导入包的引用未定义。
解决方案：使用最小配置（`disable-all: true`），并仅启用基础的代码检查工具（如 `gofmt`）。

### 导入解析问题
问题：CI 环境无法正确解析依赖项。
解决方案：
1. 确保 `go.mod` 和 `go.sum` 文件是最新的。
2. 在运行代码检查工具之前执行 `go mod download` 命令。
3. 考虑在 CI 环境中使用更简单的代码检查工具。

### 类型检查失败
问题：代码检查工具在类型检查阶段失败。
解决方案：
1. 暂时禁用需要类型检查的复杂工具。
2. 使用 `--fast` 标志以加快检查速度并减少检查强度。
3. 确认所有导入语句都正确声明。

## 持续集成/持续部署（CI/CD）优化

针对 GitHub Actions 工作流程的配置示例：

```yaml
name: Code Quality

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'
        cache: true

    - name: Download dependencies
      run: go mod download

    - name: Install golangci-lint
      run: |
        curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.59.1

    - name: Lint
      run: golangci-lint run --config .golangci.yml ./...
```

## 代码检查工具选择指南

- **gofmt**：用于代码格式的一致性检查。
- **govet**：用于检测语义错误。
- **errcheck**：用于检测未检查的错误。
- **staticcheck**：用于静态代码分析。
- **unused**：用于检测未使用的代码。
- **gosimple**：用于提供代码简化建议。
- **ineffassign**：用于检测无效的赋值操作。

根据项目需求和 CI 环境的性能要求来选择合适的代码检查工具。