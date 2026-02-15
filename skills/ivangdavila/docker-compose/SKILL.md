---
name: Docker Compose
description: 定义具有适当依赖管理、网络配置和卷管理功能的多容器应用程序。
metadata: {"clawdbot":{"emoji":"🐳","requires":{"anyBins":["docker-compose","docker"]},"os":["linux","darwin","win32"]}}
---

## `depends_on` 的准备条件

- 单独使用 `depends_on` 时，系统仅会等待容器的启动——此时服务可能尚未准备好。
- 需要添加健康检查（healthcheck）和判断服务是否真正准备就绪的条件：
```yaml
depends_on:
  db:
    condition: service_healthy
```
- 如果目标服务未定义健康检查（healthcheck），`service_healthy` 指令将返回错误。

## `healthcheck` 的 `start_period`

```yaml
healthcheck:
  test: ["CMD", "pg_isready"]
  start_period: 30s
```
- `start_period`：初始的宽限期——在此期间，健康检查失败不会被记录为问题。
- 需要较长时间启动的服务（如数据库、Java 应用程序）需要设置合适的 `start_period`。
- 如果没有设置 `start_period`，容器可能在初始化完成之前就被标记为“不健康”。

## 卷（Volume）的销毁

- 使用 `docker compose down` 命令时，卷（volume）会被保留。
- 使用 `docker compose down -v` 命令会删除所有卷，导致数据丢失。
- 有些人习惯性地添加 `-v` 参数，但在生产环境中这可能会导致严重问题。
- 带名称的卷（named volumes）在容器停止时仍会保留；匿名卷（anonymous volumes）则会被删除。

## 开发环境中的资源限制

```yaml
deploy:
  resources:
    limits:
      memory: 512M
```
- 在开发阶段设置资源限制，可以及时发现内存等问题。
- 如果容器没有资源限制，它可能会消耗掉所有主机内存，从而影响其他进程的正常运行。
- 将开发阶段的资源限制配置复制到生产环境中，以避免在生产环境中出现资源不足的问题。

## `.dockerignore` 文件

- 如果不使用 `.dockerignore` 文件，`node_modules`、`.git` 目录以及配置文件中的敏感信息（如 secrets）会被复制到容器镜像中。
- `.dockerignore` 文件的语法应该与 Dockerfile 处于同一层级。
- 如果构建环境过于复杂，会导致构建速度变慢、镜像体积增大，并可能带来安全风险。
- 至少应排除 `.git`、`node_modules`、`.env`、`.log` 文件以及构建生成的临时文件。

## 文件覆盖规则

- `docker-compose.yml` 是通用的基础配置文件。
- `docker-compose.override.yml` 是自动加载的、针对开发环境的配置文件（用于指定挂载目录、端口等设置）。
- 在生产环境中，使用 `docker compose -f docker-compose.yml -f docker-compose.prod.yml up` 命令来启动容器。
- 敏感信息和环境特定的配置应保存在 `docker-compose.override.yml` 文件中，而不是基础配置文件中。

## 可选服务的配置文件（Profiles）

```yaml
services:
  mailhog:
    profiles: [dev]
```
- 具有配置文件（profiles）的服务默认不会启动，使用 `docker compose up` 命令时这些服务会被忽略，从而保持系统的整洁性。
- 可以通过 `--profile dev` 参数来启用这些服务。
- 这些配置文件适用于测试数据库、调试工具、模拟服务以及管理界面等场景。

## 环境变量的优先级

- Shell 环境变量具有最高的优先级。
- `docker-compose` 目录下的 `.env` 文件中的环境变量优先级次之。
- 使用 `env_file:` 指令指定的环境变量优先级再次降低。
- `compose` 文件中的 `environment:` 指令指定的环境变量优先级最低。
- 注意：`.env` 文件必须命名为 `.env`，否则不会被自动加载。
- 可以使用 `docker compose config` 命令查看环境变量的实际值。