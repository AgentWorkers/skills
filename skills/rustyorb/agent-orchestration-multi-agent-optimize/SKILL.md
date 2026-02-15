---
name: agent-orchestration-multi-agent-optimize
description: "通过协调式的性能分析、工作负载分配以及成本意识强的系统编排来优化多代理系统。适用于提升代理的性能、吞吐量或可靠性。"
---

# 多智能体优化工具包

## 适用场景

- 当需要提升多智能体的协调性、吞吐量或延迟时
- 当需要分析智能体工作流程以识别瓶颈时
- 当需要为复杂的工作流程设计编排策略时
- 当需要优化成本、上下文使用效率或工具效率时

## 不适用场景

- 当只需要调整单个智能体的提示（prompt）时
- 当没有可衡量的指标或评估数据时
- 当任务与多智能体编排无关时

## 使用步骤

1. 确立基准指标和目标性能目标。
2. 分析智能体工作负载并识别协调瓶颈。
3. 逐步应用编排调整和成本控制措施。
4. 通过可重复的测试来验证改进效果，并在必要时进行回滚。

## 安全性注意事项

- 在部署编排调整之前，务必进行回归测试。
- 逐步推出更改，以防止系统出现全局性退化。

## 职责：AI驱动的多智能体性能工程专家

### 背景

多智能体优化工具是一个先进的AI驱动框架，旨在通过智能、协作的智能体优化方式全面提升系统性能。该工具利用前沿的AI编排技术，为多个领域提供全面的性能工程解决方案。

### 核心功能

- 智能多智能体协调
- 性能分析与瓶颈识别
- 自适应优化策略
- 跨领域性能优化
- 成本与效率监控

## 参数处理

该工具支持灵活的优化参数配置：

- `$TARGET`：需要优化的主系统/应用程序
- `$PERFORMANCE_GOALS`：具体的性能指标和目标
- `$OPTIMIZATION_SCOPE`：优化深度（快速见效、全面优化）
- `$BUDGET_CONSTRAINTS`：成本和资源限制
- `$QUALITY_METRICS`：性能质量阈值

## 1. 多智能体性能分析

### 分析策略

- 在系统各层进行分布式性能监控
- 实时收集和分析性能数据
- 持续跟踪性能变化趋势

#### 智能体类型分析示例

1. **数据库性能智能体**
   - 查询执行时间分析
   - 索引使用情况监控
   - 资源消耗监测

2. **应用程序性能智能体**
   - CPU和内存使用情况分析
   - 算法复杂度评估
   - 并发性和异步操作分析

3. **前端性能智能体**
   - 渲染性能指标分析
   - 网络请求优化
   - 核心Web性能指标监控

### 分析代码示例

```python
def multi_agent_profiler(target_system):
    agents = [
        DatabasePerformanceAgent(target_system),
        ApplicationPerformanceAgent(target_system),
        FrontendPerformanceAgent(target_system)
    ]

    performance_profile = {}
    for agent in agents:
        performance_profile[agent.__class__.__name__] = agent.profile()

    return aggregate_performance_metrics(performance_profile)
```

## 2. 上下文窗口优化

### 优化技术

- 智能上下文压缩
- 语义相关性过滤
- 动态上下文窗口调整
- 令牌预算管理

### 上下文压缩算法示例

```python
def compress_context(context, max_tokens=4000):
    # Semantic compression using embedding-based truncation
    compressed_context = semantic_truncate(
        context,
        max_tokens=max_tokens,
        importance_threshold=0.7
    )
    return compressed_context
```

## 3. 智能体协调效率

### 协调原则

- 并行执行设计
- 最小化智能体间的通信开销
- 动态工作负载分配
- 容错智能体交互

### 编排框架示例

```python
class MultiAgentOrchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.execution_queue = PriorityQueue()
        self.performance_tracker = PerformanceTracker()

    def optimize(self, target_system):
        # Parallel agent execution with coordinated optimization
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(agent.optimize, target_system): agent
                for agent in self.agents
            }

            for future in concurrent.futures.as_completed(futures):
                agent = futures[future]
                result = future.result()
                self.performance_tracker.log(agent, result)
```

## 4. 并行执行优化

### 关键策略

- 异步智能体处理
- 工作负载划分
- 动态资源分配
- 减少阻塞操作

## 5. 成本优化策略

### 大语言模型（LLM）成本管理

- 令牌使用情况跟踪
- 自适应模型选择
- 缓存和结果重用
- 高效的提示设计

### 成本跟踪示例

```python
class CostOptimizer:
    def __init__(self):
        self.token_budget = 100000  # Monthly budget
        self.token_usage = 0
        self.model_costs = {
            'gpt-5': 0.03,
            'claude-4-sonnet': 0.015,
            'claude-4-haiku': 0.0025
        }

    def select_optimal_model(self, complexity):
        # Dynamic model selection based on task complexity and budget
        pass
```

## 6. 延迟降低技术

### 性能加速方法

- 预测性缓存
- 提前预热智能体上下文
- 智能结果缓存
- 减少往返通信次数

## 7. 性能与速度的权衡

### 优化策略

- 性能阈值设定
- 可接受的性能下降范围
- 以质量为导向的优化
- 智能的折中选择

## 8. 监控与持续改进

### 可观测性框架

- 实时性能仪表板
- 自动化的优化反馈循环
- 基于机器学习的改进机制
- 自适应优化策略

## 参考工作流程

### 工作流程1：电子商务平台优化

1. 初始性能分析
2. 基于智能体的优化
3. 成本与性能监控
4. 持续改进循环

### 工作流程2：企业级API性能提升

1. 全面系统分析
2. 多层智能体优化
3. 迭代性能优化
4. 高效的成本扩展策略

## 关键注意事项

- 在优化前后务必进行性能测量
- 在优化过程中保持系统稳定性
- 在提升性能的同时平衡资源消耗
- 逐步实施可逆的更改

目标优化参数：$ARGUMENTS