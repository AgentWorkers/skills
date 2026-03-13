# 技能：Frugal Orchestrator（节俭型任务调度器）

## 元数据
- **名称**: frugal-orchestrator
- **版本**: 0.5.0
- **作者**: Agent Zero Project
- **标签**: 任务调度、效率优化、令牌管理、任务委托、缓存、批量处理、学习算法
- **描述**: 一个高效的令牌管理任务调度平台，具备自动路由、缓存、批量处理、点对点（A2A）通信和学习算法等功能，可减少90%以上的令牌消耗。

## 问题描述
AI代理经常在那些更适合用系统工具（如Linux命令、Python脚本）完成的任务上浪费令牌，这导致了不必要的成本和执行效率低下。

**解决方案**: Frugal Orchestrator v0.5.0通过智能的任务路由机制、缓存层以及专门的任务委托功能，实现了令牌使用的显著优化。

**成果**: 在保持全部功能的同时，令牌消耗减少了90%以上。

## 核心功能

### 模块1：自动路由器（Auto-Router）
**功能**: 自动识别任务类型并选择最优的路由方式
- 系统命令 → 通过终端执行（令牌消耗减少95%）
- 脚本 → 通过Python/Node.js执行
- 复杂逻辑 → 由AI代理处理
- **类**: `TaskRouter`

### 模块2：令牌跟踪器（Token Tracker）
**功能**: 以TOON格式记录令牌使用情况
- 监控任务是通过委托执行还是直接执行
- 生成成本节省报告
- **类**: `TokenTracker`

### 模块3：缓存管理器（Cache Manager）
**功能**: 使用内容寻址方式存储结果，并设置过期时间（TTL）
- 使用CRC32哈希值作为键
- 实现LRU缓存策略，默认过期时间为7天
- **类**: `CacheManager`

### 模块4：错误恢复（Error Recovery）
**功能**: 提供重试和备用机制以确保任务可靠执行
- 采用指数级退避策略和断路器机制
- **类**: `ErrorRecovery`, `FailureType`

### 模块5：批量处理器（Batch Processor）
**功能**: 并行执行任务
- 使用并发工作线程池进行处理
- 基于任务清单（manifest）进行任务调度
- **类**: `BatchProcessor`

### 模块6：A2A适配器（A2A Adapter）
**功能**: 实现代理之间的通信
- 支持服务发现和负载均衡
- **类**: `A2AAdapter`

### 模块7：学习引擎（Learning Engine）
**功能**: 通过模式识别辅助路由决策
- 提供置信度评分和历史数据分析功能
- **类**: `LearningEngine`

### 模块8：调度器集成（Scheduler Integration）
**功能**: 支持周期性任务调度
- 支持Cron风格的调度方式
- **类**: `SchedulerClient`

## 快速入门

```bash
# Run demonstration
cd /a0/usr/projects/frugal_orchestrator/demo && bash run_demo.sh
```

### Python集成示例
```python
from scripts.auto_router import TaskRouter
from scripts.cache_manager import CacheManager
from scripts.token_tracker import TokenTracker

# Initialize
router = TaskRouter(TokenTracker())
result = router.route("file_operations", task_input)
```

## 项目统计信息
| 统计指标 | 值         |
|--------|-------------|
| Python模块数量 | 10           |
| Shell脚本数量 | 6            |
| 总文件数量 | 58            |
| Python代码行数 | 1,763         |
| 令牌消耗减少量 | 超过90%        |

## 令牌使用效率
| 功能        | 令牌消耗减少比例   |
|------------|-------------------|
| 自动路由     | 90-95%         |
| 缓存        | 重复执行时减少超过99%     |
| 批量处理     | 线性扩展         |

## GitHub仓库
https://github.com/nelohenriq/frugal_orchestrator (v0.5.0)

## 版本历史
- **0.5.0**: 完整的任务调度平台（包含10个模块和全部基础设施）
- **0.2.0**: 标准化代理接口（agentskills.io格式），代码托管在Git仓库
- **0.1.0**: 初始版本