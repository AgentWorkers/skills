---
name: openclaw-interchange
description: 这是一个用于 OpenClaw 技能的共享 `.md` 交换库，提供了原子写操作、确定性序列化、YAML 前言（frontmatter）功能、建议性锁定（advisory locking）以及模式验证（schema validation）等基础功能。所有其他 OpenClaw 技能都是建立在这个库之上的。
---
# @openclaw/interchange

这是一个共享库，用于实现代理之间的通信，通信通过 `.md` 文件进行。

## 使用方法

```javascript
import { writeMd, readMd, acquireLock } from '@openclaw/interchange';

// Write an interchange file atomically
await writeMd('ops/status.md', { skill: 'crm', status: 'healthy' }, '## Status\nAll systems go.');

// Read it back
const { meta, content } = readMd('ops/status.md');
```

## 主要特性：
- 原子性写入操作（临时文件 + `fsync` + 重命名）
- 确定性序列化（按键排序、稳定的 YAML 格式）
- 建议性文件锁定机制（包含过时锁的检测功能）
- YAML 文件头部内容的解析
- 数据模式验证
- 电路断路器（Circuit Breaker）模式
- 生成内容的跟踪与哈希处理