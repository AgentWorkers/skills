---
model: fast
description: |
  WHAT: Turborepo monorepo build system - caching, task pipelines, and parallel execution for JS/TS projects.
  
  WHEN: User configures turbo.json, creates packages, sets up monorepo, shares code between apps, 
  runs --affected builds, debugs cache misses, or has apps/packages directories.
  
  KEYWORDS: turborepo, turbo.json, monorepo, dependsOn, task pipeline, caching, remote cache, 
  --filter, --affected, packages, workspace, pnpm workspace, npm workspace, build optimization
version: 2.7.6
---

# Turborepo

Turborepo 是一个专为 JavaScript/TypeScript 单仓库（monorepo）设计的构建系统。它能够缓存任务输出，并根据依赖关系图（dependency graph）并行执行任务。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install turborepo
```

## 必须遵守的规则：

- **绝对不要** 创建全局任务（root tasks）——每个包的 `package.json` 中都应创建包级别的任务。
- **绝对不要** 在代码中使用 `turbo <task>` 的简写形式——应在 `package.json` 和持续集成（CI）脚本中使用 `turbo run <task>`。
- **绝对不要** 直接运行任务，而应通过 `turbo run` 来执行任务。
- **绝对不要** 使用 `&&` 来链接多个 `turbo` 任务——应使用 `dependsOn` 来管理任务的依赖关系。
- **绝对不要** 使用 `--parallel` 标志——应正确配置 `dependsOn`。
- **绝对不要** 将 `.env` 文件放在仓库根目录下——应使用包级别的 `.env` 文件来管理环境变量。
- **绝对不要** 在任务输入中使用 `../`——应使用 `$TURBO_ROOT$/path` 来引用仓库根目录下的文件。

## 重要提示：使用包级别任务，而非全局任务

**切勿创建全局任务。始终使用包级别任务。**

在创建任务、脚本或构建流程时，必须遵循以下步骤：
1. 将相关脚本添加到每个包的 `package.json` 中。
2. 在全局的 `turbo.json` 中注册该任务。
3. `package.json` 中的任务执行应通过 `turbo run <task>` 来触发。

**切勿** 将任务逻辑放在全局 `package.json` 中，因为这会破坏 Turborepo 的并行执行机制。

```json
// DO THIS: Scripts in each package
// apps/web/package.json
{ "scripts": { "build": "next build", "lint": "eslint .", "test": "vitest" } }

// apps/api/package.json
{ "scripts": { "build": "tsc", "lint": "eslint .", "test": "vitest" } }

// packages/ui/package.json
{ "scripts": { "build": "tsc", "lint": "eslint .", "test": "vitest" } }
```

```json
// turbo.json - register tasks
{
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "lint": {},
    "test": { "dependsOn": ["build"] }
  }
}
```

```json
// Root package.json - ONLY delegates, no task logic
{
  "scripts": {
    "build": "turbo run build",
    "lint": "turbo run lint",
    "test": "turbo run test"
  }
}
```

```json
// DO NOT DO THIS - defeats parallelization
// Root package.json
{
  "scripts": {
    "build": "cd apps/web && next build && cd ../api && tsc",
    "lint": "eslint apps/ packages/",
    "test": "vitest"
  }
}
```

全局任务（以 `#taskname` 开头）仅用于那些确实无法在包内部实现的任务（这种情况较为罕见）。

## 其他规则：

- **当命令直接写在代码中时，始终使用 `turbo run`：**

```json
// package.json - ALWAYS "turbo run"
{
  "scripts": {
    "build": "turbo run build"
  }
}
```

**`turbo <tasks>` 的简写形式** 仅适用于人类或自动化工具直接在终端中执行的单次性命令。切勿在 `package.json`、CI 脚本或构建流程中使用 `turbo build`。

## 常见问题解答：

- **“我需要配置一个任务”**：请参考 [configuration/README.md](./references/configuration/README.md)。
- **“我的缓存不起作用”**：请检查任务是否正确设置了缓存策略。
- **“我只想运行已更改的包”**：可以使用 `--affected` 标志来仅运行已更改的包。
- **“我想过滤包”**：请参考 [configuration/package-configurations](./references/configuration/package-configurations)。
- **“环境变量没有生效”**：请确保环境变量被正确配置。
- **“我需要设置持续集成（CI）”**：请参考相关文档进行配置。
- **“我想在开发过程中监控文件变化”**：请参考相关文档了解如何实现实时监控。
- **“我需要创建/组织仓库结构”**：请参考相关文档来构建合适的仓库结构。
- **“如何组织我的单仓库？”**：请参考相关文档来设计合理的仓库结构。
- **“我想强制执行特定的架构规则”**：请参考相关文档来确保架构的一致性。

## 需避免的错误用法：

- **在代码中使用 `turbo` 的简写形式**：建议在 `package.json` 脚本和 CI 流程中使用 `turbo run`，而 `turbo <task>` 仅用于终端交互。
- **全局脚本直接执行任务**：全局 `package.json` 脚本必须通过 `turbo run` 来触发任务。
- **使用 `&&` 来链接多个 `turbo` 任务**：应让 Turborepo 自动管理任务的依赖关系。

```json
// WRONG - bypasses turbo entirely
{
  "scripts": {
    "build": "bun build",
    "dev": "bun dev"
  }
}

// CORRECT - delegates to turbo
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev"
  }
}
```

**注意：`prebuild` 脚本会手动构建依赖关系**  
如果 `package.json` 中声明了依赖关系（例如 `@repo/types: "workspace:*"`），则无需使用 `prebuild` 脚本，因为 Turborepo 会自动处理这些依赖关系。如果未声明依赖关系，需要手动将依赖关系添加到 `package.json` 中（例如 `@repo/types: "workspace:*"`），然后再移除 `prebuild` 脚本。

**关键提示：** `^build` 标志仅会在包含该依赖关系的包中触发构建。如果没有依赖关系声明，Turborepo 不会自动执行构建。

### 注意事项：

- **`globalDependencies` 的使用**：`globalDependencies` 会影响所有包中的任务，因此请确保其配置是具体的。
- **重复的配置**：如果多个任务有相同的配置，可以将其提取出来并共享，以减少重复代码。
- **`globalEnv` 和 `globalDependencies` 的使用**：`globalEnv` 用于影响所有任务，适用于全局配置；`env` 和 `inputs` 用于特定任务的配置。

### 注意：大型 `env` 数组**  
即使包含 50 多个环境变量，也不属于问题——这通常表示用户已经仔细声明了构建所需的环境依赖关系。

### 使用 `--parallel` 标志**  
`--parallel` 标志会绕过 Turborepo 的依赖关系管理机制。如果需要并行执行任务，应正确配置 `dependsOn`。

### 包级别的配置**  
当多个包需要不同的任务配置时，应在每个包的 `turbo.json` 中设置相应的配置，而不是在全局 `turbo.json` 中进行覆盖。

### 使用 `../` 的注意事项**  
不要使用相对路径（如 `../`）来引用仓库根目录外的文件，应使用 `$TURBO_ROOT$/path`。

### 关于缓存输出的问题**  
在报告缓存输出缺失的问题之前，请先确认任务实际是否产生了输出文件。例如，某些构建工具（如 tsc）即使不生成 JavaScript 文件，也可能产生缓存文件（请参考相关文档）。

## 其他相关文档：  
- [configuration/README.md](./references/configuration/README.md)：Turborepo 的基本配置和包级别配置。
- [caching/README.md](./references/caching/README.md)：缓存机制的详细信息。
- [environment/README.md](./references/environment/README.md)：环境变量的使用和配置。
- [filtering/README.md](./references/filtering/README.md)：过滤规则的介绍。

## 参考链接：  
- [ci/README.md](./references/ci/README.md)：持续集成（CI）的相关文档。
- [cli/README.md](./references/cli/README.md)：Turborepo 的命令行接口（CLI）使用指南。
- [best-practices/README.md](./references/best-practices/README.md)：单仓库的最佳实践。

## 注意：Turborepo 的文档基于官方文档：  
所有详细信息和最佳实践均来自 Turborepo 的官方文档仓库。