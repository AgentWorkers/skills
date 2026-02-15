# Janitor - 人工智能代理的清理与会话管理技能

## 概述

**Janitor** 是一款专为 OpenClaw 人工智能代理设计的智能清理和会话管理工具。它能够自动管理缓存、优化内存使用，并通过监控令牌使用情况来**防止上下文溢出**，同时智能地清理旧会话。

可以将 Janitor 视为你的**人工智能代理的智能维护团队**，它能够：
- 🧹 清理缓存文件以优化令牌使用
- 🗑️ 释放未使用的内存和 RAM
- 🔍 **实时监控上下文使用情况（新功能！）**
- 🤖 **自动清理旧会话（新功能！）**
- 📦 **在删除前归档会话（新功能！）**
- 🚨 **在上下文使用率达到 95% 时进行紧急恢复（新功能！）**
- 📊 将清理统计信息报告给代理
- 🔔 **提供多渠道通知（新功能！）**

## 快速入门

### 安装

```bash
cd /Users/sarthiborkar/Desktop/butler-main/janitor
npm install  # No dependencies needed!
```

### 基本使用

```javascript
const Janitor = require('./src/Janitor');

// Create janitor instance
const janitor = new Janitor();

// Run cleanup
const result = await janitor.cleanup();
console.log(result);
// {
//   filesDeleted: 42,
//   spaceSaved: "1.2 MB",
//   duration: "150ms",
//   memoryFreed: true
// }

// Get report
const report = await janitor.report();
```

## 功能

### 1. 缓存清理

自动清理占用磁盘空间并导致操作变慢的缓存文件：

**被清理的文件包括：**
- `node_modules/.cache/**` - Node 模块缓存
- `**/*.cache` - 通用缓存文件
- `.DS_Store` - macOS 元数据文件
- `dist/**/*.map` - 源代码映射文件
- `coverage/**` - 测试覆盖率报告文件
- `tmp/**` - 临时文件
- `**/*.log` - 老日志文件（超过 7 天的）

### 2. 内存优化

释放未使用的内存以优化令牌使用：

```javascript
const janitor = new Janitor();

// Free memory
janitor.freeMemory();

// Check memory usage
const memoryStats = janitor.getMemoryUsage();
console.log(memoryStats);
// {
//   rss: "45.2 MB",
//   heapTotal: "12.8 MB",
//   heapUsed: "8.4 MB",
//   external: "1.2 MB"
// }
```

**内存操作：**
- 触发垃圾回收（如果已启用）
- 清理 Node.js 的 require 缓存
- 报告内存使用统计信息

### 3. 未使用文件的清理

删除在指定时间范围内未被访问的文件：

```javascript
const janitor = new Janitor({
  unusedFileAgeDays: 7  // Delete files not accessed in 7 days
});

await janitor.cleanup();
```

**安全特性：**
- 绝不删除重要文件（如 package.json、README.md、src/、.git/ 等）
- 支持配置文件删除阈值
- 在删除前会先报告文件列表

### 4. 推送代码后的清理

在将代码推送到 GitHub 后自动进行清理：

**使用场景：**
推送代码到 GitHub 后，本地不再需要临时构建文件、缓存文件和覆盖率报告。

### 5. 统计与报告

获取详细的清理统计信息：

```javascript
const janitor = new Janitor();

// Run some cleanups
await janitor.cleanup();
await janitor.cleanup();

// Get stats
const stats = janitor.getStats();
console.log(stats);
// {
//   totalCleanups: 2,
//   totalFilesDeleted: 84,
//   totalSpaceSaved: "2.4 MB",
//   memoryUsage: { ... }
// }

// Get full report with recommendations
const report = await janitor.report();
console.log(report);
// {
//   timestamp: "2026-02-07T...",
//   status: "healthy",
//   stats: { ... },
//   recommendations: [
//     "Regular cleanup recommended."
//   ]
// }
```

## 配置

### 默认配置

```javascript
{
  enabled: true,
  autoCleanAfterPush: true,
  unusedFileAgeDays: 7,
  cachePatterns: [
    '**/*.cache',
    '**/node_modules/.cache/**',
    '**/.DS_Store',
    '**/dist/**/*.map',
    '**/tmp/**',
    '**/*.log',
    '**/coverage/**'
  ]
}
```

### 自定义配置

```javascript
const janitor = new Janitor({
  enabled: true,
  autoCleanAfterPush: false,  // Disable auto-cleanup after push
  unusedFileAgeDays: 14,       // Keep files for 2 weeks
  cachePatterns: [
    '**/*.cache',
    '**/my-custom-cache/**'
  ]
});
```

## 与 Butler 的集成

### 方法 1：直接集成

```javascript
const Butler = require('../src/Butler');
const Janitor = require('../janitor/src/Janitor');

const butler = new Butler();
const janitor = new Janitor();

// Spawn agent and cleanup after
async function runTaskWithCleanup() {
  const results = await butler.spawnAgent(
    'DataAnalysis',
    'Analyze data and generate report',
    200000
  );

  // Cleanup after task
  const cleanupResult = await janitor.cleanup();
  console.log('Cleanup:', cleanupResult);

  return results;
}

runTaskWithCleanup();
```

### 方法 2：自动清理钩子

```javascript
const Butler = require('../src/Butler');
const Janitor = require('../janitor/src/Janitor');

class ButlerWithJanitor extends Butler {
  constructor() {
    super();
    this.janitor = new Janitor({ autoCleanAfterPush: true });
  }

  async spawnAgent(...args) {
    const result = await super.spawnAgent(...args);

    // Auto-cleanup after agent completes
    await this.janitor.cleanup();

    return result;
  }
}

const butler = new ButlerWithJanitor();
```

## 示例

### 示例 1：基本清理

```javascript
const Janitor = require('./src/Janitor');

async function basicCleanup() {
  const janitor = new Janitor();

  console.log('Starting cleanup...');
  const result = await janitor.cleanup();

  console.log(`✅ Deleted ${result.filesDeleted} files`);
  console.log(`✅ Saved ${result.spaceSaved}`);
}

basicCleanup();
```

### 示例 2：定时清理

```javascript
const Janitor = require('./src/Janitor');

const janitor = new Janitor();

// Run cleanup every hour
setInterval(async () => {
  console.log('🧹 Running scheduled cleanup...');
  const result = await janitor.cleanup();
  console.log(`Cleaned: ${result.spaceSaved}`);
}, 60 * 60 * 1000); // 1 hour
```

### 示例 3：Git 钩子集成

创建 `.git/hooks/post-commit` 文件：

```bash
#!/bin/sh
node janitor/src/index.js cleanup --after-push
```

### 示例 4：监控与警报

```javascript
const Janitor = require('./src/Janitor');

const janitor = new Janitor();

async function monitor() {
  const report = await janitor.report();

  if (report.recommendations.length > 0) {
    console.log('⚠️  Recommendations:');
    report.recommendations.forEach(r => console.log(`   - ${r}`));
  }

  // Send to monitoring system
  sendToMonitoring(report);
}

setInterval(monitor, 5 * 60 * 1000); // Every 5 minutes
```

## 命令行接口（CLI）使用

创建 `src/index.js` 文件：

```javascript
#!/usr/bin/env node
const Janitor = require('./Janitor');

const janitor = new Janitor();

const args = process.argv.slice(2);
const command = args[0];

(async () => {
  switch (command) {
    case 'cleanup':
      const result = await janitor.cleanup();
      console.log('Result:', result);
      break;

    case 'report':
      const report = await janitor.report();
      console.log(JSON.stringify(report, null, 2));
      break;

    case 'stats':
      const stats = janitor.getStats();
      console.log(stats);
      break;

    default:
      console.log('Usage: node index.js [cleanup|report|stats]');
  }
})();
```

然后使用以下命令：

```bash
node janitor/src/index.js cleanup
node janitor/src/index.js report
node janitor/src/index.js stats
```

## API 参考

### 构造函数

```javascript
new Janitor(config?: object)
```

### 方法

#### `cleanup(workingDir?: string): Promise<CleanupResult>`

执行完整的清理操作。

**返回值：**
```javascript
{
  filesDeleted: number,
  spaceSaved: string,
  duration: string,
  memoryFreed: boolean
}
```

#### `cleanupAfterPush(): Promise<CleanupResult | null>`

在推送代码后自动执行清理（如果已启用）。

#### `freeMemory(): void`

通过触发垃圾回收和清理缓存来释放内存。

#### `getStats(): object`

获取清理统计信息。

#### `report(): Promise<Report>`

生成包含建议的详细报告。

#### `getMemoryUsage(): object`

获取当前的内存使用情况。

## 最佳实践

### 1. 定期清理

定期执行清理操作以防止缓存堆积：

```javascript
// Every hour
setInterval(() => janitor.cleanup(), 60 * 60 * 1000);
```

### 2. 任务完成后清理

任务完成后务必进行清理：

```javascript
async function runTask() {
  // Do work
  await butler.spawnAgent(...);

  // Cleanup
  await janitor.cleanup();
}
```

### 3. 监控内存使用情况

跟踪内存使用情况以检测内存泄漏：

```javascript
const memUsage = janitor.getMemoryUsage();
console.log('Heap used:', memUsage.heapUsed);
```

### 4. 安全删除

Janitor 会自动保护重要文件，但你也可以添加自定义的保护机制：

```javascript
// Override isImportant method if needed
janitor.isImportant = (filePath) => {
  const important = ['my-important-file.txt'];
  return important.some(name => filePath.includes(name));
};
```

## 性能

- 清理时间：50-500 毫秒（取决于文件数量）
- 内存开销：<5MB
- 无外部依赖
- 支持并发操作

## 故障排除

### 问题：内存使用过高

**解决方案：** 运行 `janitor.freeMemory()` 来触发垃圾回收。

### 问题：文件未被删除

**解决方案：** 检查文件是否位于受保护的目录中（如 node_modules、.git、src）。

### 问题：清理过于激进

**解决方案：** 增加配置文件中的 `unusedFileAgeDays` 值：

```javascript
const janitor = new Janitor({ unusedFileAgeDays: 30 });
```

## 待开发功能

- [ ] 通过配置文件自定义清理规则
- [ ] 与 Butler 仪表板集成
- [ ] 实时清理监控
- [ ] 云存储清理（S3、GCS）
- [ ] Docker 容器清理
- [ ] 数据库缓存清理

## 许可证

MIT

## 支持

- 问题反馈：[GitHub 问题](https://github.com/zoro-jiro-san/butler/issues)
- 文档：本文件

---

**Janitor v1.0.0** - 保持你的人工智能代理的整洁和高效运行！