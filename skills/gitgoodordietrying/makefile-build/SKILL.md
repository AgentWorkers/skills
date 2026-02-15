---
name: makefile-build
description: 为任何类型的项目编写 Makefile。这些 Makefile 可用于设置构建自动化流程、定义多目标构建、管理任务之间的依赖关系、创建项目任务执行器，或者用于非 C 语言的项目（如 Go、Python、Docker、Node.js）的构建过程。同时，文档还介绍了 Just 和 Task 这两种现代的替代方案。
metadata: {"clawdbot":{"emoji":"🔨","requires":{"anyBins":["make","just","task"]},"os":["linux","darwin","win32"]}}
---

# Makefile 与构建

编写 Makefile 以实现项目的自动化构建，支持多种编程语言。内容包括目标（targets）、依赖关系（dependencies）、变量（variables）、模式规则（pattern rules）、虚拟目标（phony targets），以及如何为 Go、Python、Docker 和 Node.js 项目使用 Makefile。同时介绍了 Just 和 Task 这两种现代的替代方案。

## 适用场景

- 自动化构建、测试、代码检查（lint）和部署（deploy）命令
- 定义任务之间的依赖关系（例如：先构建再测试）
- 创建一个全项目范围内的任务执行器（确保团队成员使用一致的方法）
- 用简洁易记的目标替换冗长的命令行界面（CLI）命令
- 管理多步骤的构建流程
- 适用于需要执行 `make build && make test && make deploy` 工作流程的项目

## Makefile 基础知识

### 结构

```makefile
# target: prerequisites
#     recipe (MUST be indented with TAB, not spaces)

build: src/main.go
	go build -o bin/app src/main.go

test: build
	go test ./...

clean:
	rm -rf bin/

# First target is the default (runs with bare `make`)
```

### 变量

```makefile
# Simple assignment
CC = gcc
CFLAGS = -Wall -O2

# Deferred assignment (expanded when used)
FILES = $(wildcard src/*.go)

# Immediate assignment (expanded when defined)
VERSION := $(shell git describe --tags --always)

# Conditional assignment (only if not already set)
PORT ?= 8080

# Use variables
build:
	$(CC) $(CFLAGS) -o app main.c
	@echo "Version: $(VERSION)"
```

### 自动变量

```makefile
# $@ = target name
# $< = first prerequisite
# $^ = all prerequisites
# $* = stem (pattern match)
# $(@D) = directory of target
# $(@F) = filename of target

bin/app: src/main.go src/util.go
	go build -o $@ $^
# $@ = bin/app
# $^ = src/main.go src/util.go
# $< = src/main.go

# Pattern rule
%.o: %.c
	$(CC) -c -o $@ $<
# For foo.o: $@ = foo.o, $< = foo.c, $* = foo
```

### 虚拟目标（Phony Targets）

```makefile
# Without .PHONY, if a file named "clean" exists, `make clean` does nothing
.PHONY: build test clean lint fmt help

build:
	go build -o bin/app ./cmd/app

test:
	go test ./...

clean:
	rm -rf bin/ dist/

# List all targets
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
```

### 自文档化的 Makefile

```makefile
.DEFAULT_GOAL := help

build: ## Build the application
	go build -o bin/app ./cmd/app

test: ## Run all tests
	go test -v ./...

lint: ## Run linters
	golangci-lint run

clean: ## Remove build artifacts
	rm -rf bin/ dist/

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
```

## 针对特定语言的 Makefile

### Go

```makefile
BINARY_NAME := myapp
VERSION := $(shell git describe --tags --always --dirty)
LDFLAGS := -ldflags "-X main.version=$(VERSION)"
GOFILES := $(shell find . -name '*.go' -not -path './vendor/*')

.PHONY: all build test lint clean run

all: lint test build

build: ## Build binary
	CGO_ENABLED=0 go build $(LDFLAGS) -o bin/$(BINARY_NAME) ./cmd/$(BINARY_NAME)

test: ## Run tests
	go test -race -coverprofile=coverage.out ./...

test-coverage: test ## Show coverage report
	go tool cover -html=coverage.out

lint: ## Run linters
	golangci-lint run ./...

fmt: ## Format code
	gofmt -w $(GOFILES)

run: build ## Build and run
	./bin/$(BINARY_NAME)

clean: ## Clean build artifacts
	rm -rf bin/ coverage.out

# Cross-compilation
build-linux: ## Build for Linux
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o bin/$(BINARY_NAME)-linux-amd64 ./cmd/$(BINARY_NAME)

build-all: ## Build for all platforms
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o bin/$(BINARY_NAME)-linux-amd64 ./cmd/$(BINARY_NAME)
	GOOS=darwin GOARCH=arm64 go build $(LDFLAGS) -o bin/$(BINARY_NAME)-darwin-arm64 ./cmd/$(BINARY_NAME)
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o bin/$(BINARY_NAME)-windows-amd64.exe ./cmd/$(BINARY_NAME)
```

### Python

```makefile
PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: all install test lint fmt clean run

all: install lint test

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip

install: $(VENV)/bin/activate ## Install dependencies
	$(BIN)/pip install -r requirements.txt
	$(BIN)/pip install -r requirements-dev.txt

test: ## Run tests
	$(BIN)/pytest -v --cov=src --cov-report=term-missing

lint: ## Run linters
	$(BIN)/ruff check src/ tests/
	$(BIN)/mypy src/

fmt: ## Format code
	$(BIN)/ruff format src/ tests/

run: ## Run application
	$(BIN)/python -m src.main

clean: ## Remove venv and caches
	rm -rf $(VENV) __pycache__ .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
```

### Node.js / TypeScript

```makefile
.PHONY: all install build test lint clean dev

all: install lint test build

node_modules: package.json
	npm install
	@touch node_modules

install: node_modules ## Install dependencies

build: node_modules ## Build TypeScript
	npx tsc

test: node_modules ## Run tests
	npx vitest run

test-watch: node_modules ## Run tests in watch mode
	npx vitest

lint: node_modules ## Lint code
	npx eslint src/ --ext .ts,.tsx
	npx tsc --noEmit

fmt: node_modules ## Format code
	npx prettier --write 'src/**/*.{ts,tsx}'

dev: node_modules ## Run in development mode
	npx tsx watch src/index.ts

clean: ## Clean build artifacts
	rm -rf dist/ node_modules/.cache
```

### Docker

```makefile
IMAGE_NAME := myapp
VERSION := $(shell git describe --tags --always)
REGISTRY := ghcr.io/myorg

.PHONY: build push run stop clean

build: ## Build Docker image
	docker build -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .

push: build ## Push to registry
	docker tag $(IMAGE_NAME):$(VERSION) $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
	docker tag $(IMAGE_NAME):latest $(REGISTRY)/$(IMAGE_NAME):latest
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
	docker push $(REGISTRY)/$(IMAGE_NAME):latest

run: ## Run container
	docker run --rm -p 8080:8080 --name $(IMAGE_NAME) $(IMAGE_NAME):latest

stop: ## Stop container
	docker stop $(IMAGE_NAME) 2>/dev/null || true

clean: ## Remove images
	docker rmi $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest 2>/dev/null || true

compose-up: ## Start with docker compose
	docker compose up -d --build

compose-down: ## Stop compose
	docker compose down

compose-logs: ## Follow compose logs
	docker compose logs -f
```

## 高级技巧

### 条件逻辑

```makefile
# OS detection
UNAME := $(shell uname -s)
ifeq ($(UNAME),Darwin)
    SED := sed -i ''
else
    SED := sed -i
endif

# Environment-based config
ENV ?= development
ifeq ($(ENV),production)
    CFLAGS += -O2
    LDFLAGS += -s -w
else
    CFLAGS += -g -O0
endif

# Check if command exists
HAS_DOCKER := $(shell command -v docker 2>/dev/null)
docker-build:
ifndef HAS_DOCKER
	$(error "docker is not installed")
endif
	docker build -t myapp .
```

### 多目录构建

```makefile
SERVICES := api worker scheduler

.PHONY: build-all test-all $(SERVICES)

build-all: $(SERVICES)

$(SERVICES):
	$(MAKE) -C services/$@ build

test-all:
	@for svc in $(SERVICES); do \
		echo "Testing $$svc..."; \
		$(MAKE) -C services/$$svc test || exit 1; \
	done
```

### 包含其他 Makefile

```makefile
# Split large Makefile into modules
include mk/docker.mk
include mk/test.mk
include mk/deploy.mk

# Optional include (no error if missing)
-include .env.mk
```

### 静默执行与输出控制

```makefile
# @ suppresses command echo
install:
	@echo "Installing dependencies..."
	@npm install

# .SILENT for entire targets
.SILENT: help clean

# Make less verbose globally
MAKEFLAGS += --no-print-directory
```

## Just（现代替代方案）

### Justfile 语法

```just
# justfile — simpler than Make, no TAB requirement

# Set shell
set shell := ["bash", "-euo", "pipefail", "-c"]

# Variables
version := `git describe --tags --always`
default_port := "8080"

# Default recipe (first one)
default: lint test build

# Recipes
build: ## Build the application
    go build -ldflags "-X main.version={{version}}" -o bin/app ./cmd/app

test: ## Run tests
    go test -race ./...

lint: ## Run linters
    golangci-lint run

run port=default_port: build ## Run with optional port
    ./bin/app --port {{port}}

clean: ## Clean artifacts
    rm -rf bin/ dist/

# Recipes with dependencies
deploy: build test
    ./scripts/deploy.sh

# OS-specific
[linux]
install-deps:
    sudo apt install -y build-essential

[macos]
install-deps:
    brew install go golangci-lint

# List recipes
help:
    @just --list
```

### Task（Go 任务执行器）

### Taskfile.yml

```yaml
# Taskfile.yml
version: '3'

vars:
  VERSION:
    sh: git describe --tags --always
  BINARY: myapp

tasks:
  default:
    deps: [lint, test, build]

  build:
    desc: Build the application
    cmds:
      - go build -ldflags "-X main.version={{.VERSION}}" -o bin/{{.BINARY}} ./cmd/{{.BINARY}}
    sources:
      - ./**/*.go
    generates:
      - bin/{{.BINARY}}

  test:
    desc: Run tests
    cmds:
      - go test -race ./...

  lint:
    desc: Run linters
    cmds:
      - golangci-lint run

  run:
    desc: Build and run
    deps: [build]
    cmds:
      - ./bin/{{.BINARY}} {{.CLI_ARGS}}

  clean:
    desc: Clean artifacts
    cmds:
      - rm -rf bin/ dist/

  docker:build:
    desc: Build Docker image
    cmds:
      - docker build -t {{.BINARY}}:{{.VERSION}} .

  # Task with preconditions
  deploy:
    desc: Deploy to production
    preconditions:
      - sh: test -f bin/{{.BINARY}}
        msg: "Build first: task build"
      - sh: git diff --quiet
        msg: "Uncommitted changes detected"
    cmds:
      - ./scripts/deploy.sh
```

```bash
# Install: https://taskfile.dev/installation/
# Run:
task          # Default task
task build    # Specific task
task --list   # List all tasks
```

## Make、Just 与 Task 的比较

| 特性 | Make | Just | Task |
|---|---|---|---|
| 配置格式 | Makefile（对制表符（TAB）敏感） | Justfile | Taskfile.yml |
| 依赖关系管理 | 基于文件 + 虚拟目标 | 基于任务定义 | 基于任务定义 |
| 文件变更检测 | 内置功能 | 不支持 | 需要手动更新源文件或生成新的任务文件 |
| 变量支持 | 支持（但配置复杂） | 支持（配置简单） | 支持（使用 YAML 格式） |
| 跨平台兼容性 | 需要安装 Make 工具 | 无需额外安装 | 无需额外安装 |
| 学习难度 | 相对较高 | 相对较低 | 相对较低 |
| 适用场景 | 适合 C/C++ 构建、依赖关系复杂的项目 | 适用于替代传统的任务执行器 | 适用于原生使用 YAML 的项目 |

## 使用技巧

- Makefile 的常见错误：使用空格而非制表符进行缩进。Makefile 中的依赖关系定义必须严格使用制表符（TAB）。
- 为所有非实际存在的文件添加 `.PHONY` 标签。否则，如果存在名为 `clean` 的文件，`make clean` 命令将不会执行。
- 使用 `@` 前缀来抑制命令的输出，以获得更清晰的输出：`@echo "Building..."` 只会输出 “Building...”，而不会显示 `echo` 命令本身。
- 在每个 Makefile 中添加自文档化的 `help` 目标（使用 `##` 注释），方便用户快速了解如何使用该文件。执行 `make help` 可以获取项目的使用说明。
- 对于简单的任务执行，Just 或 Task 更为简洁易用，且不需要关注制表符的使用规则。
- 使用 `?=` 来允许用户覆盖某些变量：例如 `PORT ?= 8080` 可以让 `PORT=9090 make run` 命令正常执行。
- 对于混合使用多种编程语言的项目（如 Go、Python 和 Docker），在项目根目录下编写一个 Makefile，并将其链接到对应语言的构建脚本是一个常见的做法。
- Makefile 的基于文件的依赖关系管理功能非常强大，能有效避免不必要的重新构建。