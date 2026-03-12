# pattern-miner 技能

从多源数据中实现智能的模式识别和可操作的洞察。

## 描述

`pattern-miner` 技能利用机器学习技术，在您的工作流程数据（对话、决策、任务）中发现隐藏的模式。它能够识别出重复出现的主题、关联关系以及异常情况，并生成可操作的洞察，以提高生产力和决策质量。

## 安装

```bash
cd ~/.openclaw/workspace/skills/pattern-miner
npm install
npm run build
```

### Python 依赖项

```bash
pip install numpy scikit-learn pandas tree-sitter
```

## 使用方法

### 命令行接口 (CLI) 命令

```bash
# Run pattern mining
pattern-miner mine

# Incremental mining (only new data)
pattern-miner mine --incremental

# List discovered patterns
pattern-miner list
pattern-miner list --type cluster
pattern-miner list --verbose

# Analyze specific patterns/insights
pattern-miner analyze
pattern-miner analyze --pattern <id>
pattern-miner analyze --insight <id>
pattern-miner analyze --category optimization

# Apply insights
pattern-miner apply --confirm
pattern-miner apply --insight <id> --confirm
pattern-miner apply --category automation --dry-run

# Show statistics
pattern-miner stats

# Export patterns
pattern-miner export --format json --output patterns.json
pattern-miner export --format csv --output patterns.csv

# Configuration
pattern-miner config --show
pattern-miner config --init
```

### Node.js API

```typescript
import { PatternMiner } from '@openclaw/skill-pattern-miner';

const miner = new PatternMiner({
  minConfidence: 0.7,
  minFrequency: 5,
  analysisTypes: ['cluster', 'association', 'anomaly']
});

await miner.initialize();

// Run mining
const results = await miner.mine();
console.log(`Found ${results.summary.totalPatterns} patterns`);
console.log(`Generated ${results.summary.totalInsights} insights`);

// List patterns
const patterns = await miner.listPatterns();
const clusterPatterns = await miner.listPatterns('cluster', 10);

// List insights
const insights = await miner.listInsights(undefined, true); // pending only

// Get stats
const stats = await miner.getStats();

// Apply insight
await miner.applyInsight('insight_123');

// Export
const json = await miner.exportPatterns('json');
const csv = await miner.exportPatterns('csv');
```

## 核心功能

### 多源数据收集

自动从以下来源收集数据：
- **对话**：来自 `context-preserver` 的会话日志
- **决策**：来自 `decision-recorder` 的决策记录
- **任务**：工作区中的任务文件（JSON、Markdown 格式）
- **文件**：您配置的任何文件模式

### 智能模式识别

提供三种分析类型：

1. **聚类** (`cluster`)：
   - 使用 KMeans 算法对相似项进行分组
   - 识别重复出现的主题和话题
   - 通过 TF-IDF 对文本进行相似度量化

2. **关联规则** (`association`)：
   - 查找经常一起出现的项
   - 计算置信度和支持度指标
   - 发现隐藏的关系

3. **异常检测** (`anomaly`)：
   - 使用局部异常因子 (Local Outlier Factor, LOF) 识别异常值
   - 标记需要审查的不寻常模式
   - 帮助发现边缘情况和问题

### 模式评分系统

每个模式会根据以下指标进行评分：
- **置信度**：模式的可靠性（0-1）
- **频率**：模式出现的频率
- **重要性**：综合评分基于：
  - 模式的置信度
  - 经过归一化的频率
  - 项目的优先级元数据

### 可操作的洞察

生成的洞察包括：
- **标题**：发现的清晰描述
- **描述**：相关背景和指标
- **建议**：具体的操作建议
- **优先级**：高/中/低
- **预期影响**：估计的价值（0-1）
- **类别**：优化/自动化/风险

## 配置

默认配置存储在 `~/.pattern-miner/config.json` 中：

```json
{
  "dataDir": "~/.openclaw/workspace",
  "patternDir": "~/.pattern-miner",
  "minConfidence": 0.6,
  "minFrequency": 3,
  "analysisTypes": ["cluster", "association", "anomaly"],
  "sources": [
    {
      "type": "conversation",
      "name": "conversations",
      "path": "~/.openclaw/sessions",
      "pattern": "**/*.json"
    }
  ],
  "autoScan": false,
  "scanInterval": 60,
  "maxPatterns": 1000,
  "retentionDays": 30
}
```

## 数据存储

模式和洞察存储在 `~/.pattern-miner/` 目录下：
- `patterns.json`：发现的模式
- `insights.json`：生成的洞察
- `config.json`：配置信息

## 集成

### 与 `context-preserver` 的集成

如果安装了 `context-preserver`，该技能会自动读取对话日志：

```json
{
  "sources": [
    {
      "type": "conversation",
      "name": "sessions",
      "path": "~/.openclaw/sessions",
      "pattern": "**/*.json"
    }
  ]
}
```

### 与 `decision-recorder` 的集成

与决策日志集成：

```json
{
  "sources": [
    {
      "type": "decision",
      "name": "decisions",
      "path": "~/.openclaw/decisions",
      "pattern": "**/*.json"
    }
  ]
}
```

## 定期扫描

要实现自动周期性扫描，请将其添加到您的 crontab 中：

```bash
# Run pattern mining every hour
0 * * * * cd ~/.openclaw/workspace/skills/pattern-miner && pattern-miner mine --incremental
```

或者可以在配置中启用自动扫描：

```json
{
  "autoScan": true,
  "scanInterval": 60
}
```

## 输出示例

### 模式输出

```json
{
  "id": "cluster_0_1710234567",
  "type": "cluster",
  "items": ["...", "..."],
  "confidence": 0.85,
  "frequency": 12,
  "importance": 0.78,
  "metadata": { "centroid": [...] },
  "createdAt": "2024-03-12T09:00:00Z",
  "source": "clustering"
}
```

### 洞察输出

```json
{
  "id": "insight_cluster_0_1710234567",
  "patternId": "cluster_0_1710234567",
  "title": "Recurring Pattern: Code review feedback...",
  "description": "Found 12 similar items forming a pattern",
  "action": "Review and standardize this pattern",
  "priority": "high",
  "expectedImpact": 0.7,
  "category": "optimization"
}
```

## 故障排除

### 未找到 Python

确保已安装 Python 3.8 及更高版本，并且它被添加到 PATH 环境变量中：
```bash
python3 --version
```

### 未发现模式

- 检查数据源是否配置正确
- 确保有足够的数据（`minFrequency` 的默认值为 3）
- 尝试使用 `--verbose` 参数运行以查看收集详情

### 置信度较低

- 增加数据量
- 调整配置中的 `minConfidence` 值
- 检查数据的质量和一致性

## 技术细节

### 使用的算法

- **聚类**：基于 TF-IDF 特征的 KMeans 算法
- **关联规则**：Apriori 风格的规则挖掘
- **异常检测**：局部异常因子 (LOF) 算法

### 性能

- 对于大型数据集支持增量扫描
- 可配置的模式保留时间（默认为 30 天）
- 模式数量上限（默认为 1000 个）

## 许可证

MIT 许可证