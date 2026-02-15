---
name: memory-compression-system
description: OpenClaw 的集成内存管理和极致上下文压缩技术：将内存管理、压缩、搜索以及自动化功能整合到一个统一的系统中。
version: 3.0.0
author: tenx (@Safetbear)
tags: [memory, compression, automation, optimization, search]
---
# 内存压缩系统 v3.0

专为 OpenClaw 设计的集成内存管理和极致压缩解决方案。该系统将内存管理的最佳实践与极致压缩技术相结合，通过自动化调度实现高效的数据管理。

## 快速入门

```bash
# Install skill
openclaw skill install memory-compression-system

# Enable automatic compression (runs every 6 hours)
scripts/enable.sh

# Check status
scripts/status.sh

# Manual compression
scripts/compress.sh --format ultra

# Search memory
scripts/search.sh "keyword"
```

## 主要功能

### 1. 集成内存管理
- **自动压缩**：每 6 小时自动执行一次压缩操作（UTC 时间 00:00、06:00、12:00、18:00）
- **智能清理**：每日自动清理旧文件
- **搜索功能**：支持跨所有内存文件统一搜索
- **备份系统**：压缩前自动备份数据

### 2. 三种压缩格式
- **Base64 Compact (B64C)**：通用兼容性，压缩率约 40%
- **Custom Binary (CBIN)**：优化后的二进制格式，压缩率约 70%
- **Ultra Compact (UCMP)**：极致压缩格式，压缩率约 85%，目标文件大小约为 150 个数据单元

### 3. 自动化调度
- **单一 cron 作业**：避免任务冲突
- **可配置**：支持调整压缩频率和时间
- **可靠性**：内置错误恢复和日志记录功能
- **高效性**：资源消耗极低

### 4. 搜索与检索
- **跨格式搜索**：支持所有压缩格式的文件
- **快速索引**：实时更新搜索索引
- **压缩格式识别**：能够识别压缩后的文件格式
- **导出选项**：支持多种格式的输出结果

### 5. 兼容 ClawHub
- **标准接口**：与 ClawHub 完全兼容
- **简单安装**：通过单一命令即可完成配置
- **健康检查**：内置系统健康监测功能
- **详细文档**：提供全面的使用指南

## 安装

### 推荐通过 ClawHub 安装
```bash
openclaw skill search memory-compression-system
openclaw skill install memory-compression-system
```

### 手动安装
```bash
cd /home/node/.openclaw/workspace/skills
git clone [repository-url] memory-compression-system
cd memory-compression-system
scripts/install.sh
```

## 使用方法

### 基本操作
```bash
# Enable automatic compression
scripts/enable.sh

# Disable automatic compression  
scripts/disable.sh

# Check system status
scripts/status.sh

# Run health check
scripts/health.sh
```

### 压缩操作
```bash
# Compress with auto format selection
scripts/compress.sh

# Compress to specific format
scripts/compress.sh --format base64
scripts/compress.sh --format binary
scripts/compress.sh --format ultra

# Decompress files
scripts/decompress.sh [filename]

# List compressed files
scripts/list.sh
```

### 搜索操作
```bash
# Search across all memory
scripts/search.sh "keyword"

# Search with filters
scripts/search.sh "keyword" --format ultra --date 2026-02-15

# Export search results
scripts/search.sh "keyword" --export json

# View search history
scripts/search-history.sh
```

### 管理操作
```bash
# Cleanup old files
scripts/cleanup.sh --days 30

# Backup system
scripts/backup.sh

# Restore from backup
scripts/restore.sh [backup-file]

# View logs
scripts/logs.sh

# Performance metrics
scripts/metrics.sh
```

## 配置

### 主配置文件
编辑 `config/default.conf` 文件：
```bash
# Compression settings
COMPRESSION_ENABLED=true
DEFAULT_FORMAT=ultra
RETENTION_DAYS=30
MAX_COMPRESSED_FILES=100

# Cron schedule (UTC)
CRON_SCHEDULE="0 */6 * * *"  # Every 6 hours
CLEANUP_SCHEDULE="0 4 * * *" # Daily at 04:00

# Search settings
SEARCH_ENABLED=true
SEARCH_INDEX_AUTO_UPDATE=true
SEARCH_HISTORY_SIZE=1000

# Performance settings
MAX_MEMORY_MB=100
MAX_PROCESSING_TIME_SEC=300
```

### 环境变量
```bash
export MEMORY_COMPRESSION_DEBUG=1  # Enable debug mode
export MEMORY_COMPRESSION_QUIET=0  # Disable quiet mode
export MEMORY_COMPRESSION_TEST=0   # Enable test mode
```

## 压缩格式

### Base64 Compact (B64C)
**特点**：
- 人类可读的文件格式
- 易于调试
- 兼容性良好
- 支持 CRC32 校验

### Custom Binary (CBIN)
**特点**：
- 优化后的二进制格式
- 使用共享字符串字典
- 采用霍夫曼编码算法
- 支持 CRC16 校验

### Ultra Compact (UCMP)
**特点**：
- 极致压缩效果（压缩率约 85%）
- 使用缩写字符
- 采用位打包技术
- 支持差分编码
- 内置字符串复用机制

### 自动化调度

- **压缩任务**：每 6 小时执行一次压缩操作（UTC 时间 00:00、06:00、12:00、18:00）
  - 备份当前内存数据
  - 选择最优压缩格式进行压缩
  - 更新搜索索引
  - 清理旧文件
  - 记录压缩结果

### 清理任务
- **每日 04:00 UTC**执行：
  - 删除超过保留期限的文件
  - 归档日志文件
  - 优化搜索索引
  - 更新系统统计信息

### 健康检查
- **集成 OpenClaw 的健康检查机制**
  - 检查压缩状态
  - 验证文件完整性
  - 监控系统资源使用情况
  - 报告潜在问题

## 搜索系统

- **实时索引更新**：每次压缩后自动更新索引
- **跨格式搜索**：支持多种压缩格式的文件
- **快速检索**：优化搜索速度
- **压缩内容识别**：能够识别压缩后的文件内容

### 错误处理与恢复

- **自动恢复机制**：压缩前自动备份数据
- **详细日志记录**：所有操作都会被记录下来
- **故障回滚**：发生故障时可自动恢复到备份状态
- **错误通知**：对关键问题及时发送警报

### 手动恢复方法
```bash
# Check error logs
scripts/logs.sh --error

# Restore from backup
scripts/restore.sh latest

# Repair search index
scripts/repair-index.sh

# Reset system
scripts/reset.sh --safe
```

### 常见问题及解决方法

- **压缩失败**：检查磁盘空间并运行 `scripts/repair.sh` 命令
- **搜索功能失效**：使用 `scripts/rebuild-index.sh` 重建索引
- **Cron 作业未执行**：使用 `scripts/status.sh --cron` 检查作业状态
- **性能下降**：运行 `scripts/cleanup.sh --aggressive` 命令优化系统性能

## 监控与日志记录

- **日志文件**：
  - `logs/compression.log`：记录压缩操作日志
  - `logs/search.log`：记录搜索操作日志
  - `logs/error.log`：记录错误信息
  - `logs/performance.log`：记录系统性能指标
  - `logs/cron.log`：记录 Cron 作业执行情况

### 状态监控
```bash
# Basic status
scripts/status.sh

# Detailed health check
scripts/health.sh

# Performance metrics
scripts/metrics.sh

# System information
scripts/info.sh
```

### 警报系统
- **电子邮件通知**：针对严重错误
- **Telegram 联系人通知**：重要事件实时通知
- **日志分析**：自动分析系统日志
- **性能警报**：及时发现资源使用问题

## 测试

- **测试套件**：包含单元测试、集成测试、性能测试等
- **测试覆盖范围**：涵盖编码/解码、系统集成、性能测试等多个方面

### 手动测试方法
```bash
# Test compression
scripts/test-compression.sh

# Test search
scripts/test-search.sh

# Test cron job
scripts/test-cron.sh

# Test error handling
scripts/test-errors.sh
```

## 性能指标

- **压缩性能**：
  - Base64 格式：10KB 文件压缩时间 < 50 毫秒
  - Binary 格式：10KB 文件压缩时间 < 100 毫秒
  - Ultra 格式：10KB 文件压缩时间 < 200 毫秒
- **压缩效果**：平均压缩率 75-90%

- **搜索性能**：
  - 索引生成时间：< 100 毫秒
  - 文件搜索时间：< 50 毫秒（针对 1000 个文件）
- **系统资源**：
  - CPU 资源消耗极低
  - 内存使用量：< 50MB
  - 磁盘空间：支持自定义保留策略
  - 数据传输：仅限本地网络

## 更新与维护

- **更新流程**：请按照官方文档中的说明进行更新

### 备份建议
- **定期备份**：每周备份 `data/` 目录
- **索引导出**：每月导出搜索索引数据
- **日志归档**：每月备份日志文件
- **配置文件备份**：修改配置文件后及时备份

### 版本历史
- **3.0.0**：集成内存压缩功能的版本
- **2.0.0**：引入极致压缩功能的版本
- **1.0.0**：基础内存管理功能的版本

## 开发流程

- **开发环境设置**：请参考官方文档进行开发环境配置
- **代码规范**：遵循 Bash 脚本编写规范（Google Bash Style Guide）和 JavaScript 编程规范
- **文档维护**：持续更新 SKILL.md 文档
- **测试流程**：为新功能添加相应的测试用例

### 提交代码请求
- **提交流程**：请按照官方指南创建新的功能分支并提交 Pull Request

## 技术支持

- **文档参考**：请查阅相关文档（SKILL.md、README.md 等）
- **示例代码**：提供详细的操作示例
- **问题排查**：参考故障排查指南（examples/troubleshooting.md）

### 社区资源
- **ClawHub**：官方技能仓库
- **Discord 社区**：OpenClaw 用户交流平台
- **GitHub**：问题跟踪与反馈渠道
- **官方文档**：OpenClaw 官方技术文档

## 许可证
本软件采用 MIT 许可协议，详细许可信息请参阅 LICENSE 文件。

---

**注意**：本工具专为 OpenClaw 的性能优化而设计。在生产环境中使用前，请务必备份重要数据，并在安全环境中进行充分测试。