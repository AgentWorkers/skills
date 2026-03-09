--------------------------0aa845c205f28859
Content-Disposition: form-data; name="file"; filename="SKILL.md"
Content-Type: application/octet-stream

---
name: go-install
version: 1.0.0
description: 在 Linux 上安装 Go 编译器，用于 Go 项目的编译和测试
---

# Go 编译器安装

在 Linux 上安装 Go 编译器，以便进行 Go 项目的开发、编译和测试。

## 使用场景

- Go 项目开发
- 运行单元测试
- 编译 Go 程序

## 安装步骤

### 1. 检查系统架构

```bash
uname -m
# x86_64 = amd64
# aarch64 = arm64
```

### 2. 下载并安装

**amd64 (x86_64):**
```bash
cd /tmp
curl -LO https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
tar -xzf go1.22.0.linux-amd64.tar.gz
mv go ~/go-sdk
rm go1.22.0.linux-amd64.tar.gz
```

**arm64 (aarch64):**
```bash
cd /tmp
curl -LO https://go.dev/dl/go1.22.0.linux-arm64.tar.gz
tar -xzf go1.22.0.linux-arm64.tar.gz
mv go ~/go-sdk
rm go1.22.0.linux-arm64.tar.gz
```

### 3. 配置环境变量

```bash
export PATH=$PATH:~/go-sdk/bin
export GOPATH=~/go
export GOROOT=~/go-sdk
```

### 4. 使配置持久化

将配置添加到 `~/.bashrc` 或 `~/.profile` 文件中：

```bash
echo 'export PATH=$PATH:~/go-sdk/bin' >> ~/.bashrc
echo 'export GOPATH=~/go' >> ~/.bashrc
echo 'export GOROOT=~/go-sdk' >> ~/.bashrc
```

### 5. 验证安装

```bash
go version
go env GOPATH GOROOT
```

## 常用命令

```bash
# Run tests
go test ./...

# Run tests with verbose output
go test ./... -v

# Build project
go build -o <output> ./cmd/<entry>

# Download dependencies
go mod download

# Tidy dependencies
go mod tidy
```

## 资源要求

| 项目 | 需求 |
|------|------- |
| 下载大小 | 约 65MB |
| 解压后大小 | 约 300MB |
| 内存 | 最小 512MB |
| CPU | 单核即可满足需求 |

## 注意事项

1. Go 没有运行时依赖，是一个独立的二进制文件。
2. 编译速度极快，非常适合持续集成/持续部署（CI/CD）流程。
3. 建议使用长期支持（LTS）版本（例如 1.22.x）。
4. GOPATH 目录会自动创建。

## 版本选择

| 版本 | 说明 |
|---------|------------- |
| go1.22.x | 长期支持版本（推荐） |
| go1.21.x | 之前的稳定版本 |
| go1.23.x | 最新版本 |

下载地址：https://go.dev/dl/