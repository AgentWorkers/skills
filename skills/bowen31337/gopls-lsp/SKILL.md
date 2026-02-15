---
name: gopls-lsp
description: Go语言服务器（gopls）为.go文件提供代码智能、重构和分析功能。当您需要自动完成代码、快速定位函数定义、查找代码引用、检测错误或进行代码重构时，可以使用该工具。
---

# gopls LSP

gopls 是一个用于 Go 语言的集成开发环境（IDE）服务器插件，通过官方的 Go 语言服务器（gopls）提供全面的代码智能支持。

## 功能

- **代码智能**：自动完成代码、跳转到函数定义、查找代码引用
- **错误检测**：实时诊断编译错误和问题
- **重构**：重命名变量/函数、提取代码片段、整理导入语句
- **代码分析**：静态代码分析、提供代码优化建议、检测未使用的代码
- **支持的文件扩展名**：`.go`

## 安装

使用 Go 工具链安装 gopls：

```bash
go install golang.org/x/tools/gopls@latest
```

**注意**：确保 `$GOPATH/bin`（或 `$HOME/go/bin`）已添加到系统的 PATH 环境变量中。

验证安装是否成功：
```bash
gopls version
```

## 使用方法

该语言服务器会在支持 LSP 的编辑器中自动运行。如需手动操作：

### 格式化代码
```bash
gofmt -w file.go
```

### 运行代码检查工具（linter）
```bash
go vet ./...
```

### 编译和测试代码
```bash
go build ./...
go test ./...
```

## 配置

在项目或工作区中创建 `gopls.yaml` 文件以自定义配置：

```yaml
analyses:
  unusedparams: true
  shadow: true
completeUnimported: true
staticcheck: true
```

或者通过环境变量进行配置：
```bash
export GOPLS_CONFIG='{"staticcheck": true, "analyses": {"unusedparams": true}}'
```

## 集成方式

在编辑 Go 代码时：
1. gopls 会在 LSP 编辑器中提供实时诊断功能
2. 使用 `go fmt` 或 `gofmt` 命令格式化代码
3. 使用 `go vet` 进行额外的静态代码分析
4. 在提交代码之前使用 `go test` 命令运行测试

## 常用 Go 命令

- `go mod init <module>` - 初始化 Go 模块
- `go mod tidy` - 清理依赖关系
- `go get <package>` - 添加依赖包
- `go build` - 编译代码
- `go run main.go` - 运行程序
- `go test` - 运行测试
- `go vet` - 检查代码中的潜在问题

## 更多信息

- [gopls 官方文档](https://pkg.go.dev/golang.org/x/tools/gopls)
- [GitHub 仓库](https://github.com/golang/tools/tree/master/gopls)
- [Go 官方文档](https://go.dev/doc/)