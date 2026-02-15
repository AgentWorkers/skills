# 🐾 AI成本追踪器 — 了解您的支出情况  
> 由Odin's Eye Enterprises开发 — 古老的智慧，现代的智能。  

追踪每一次AI API调用，生成支出报告，并提供优化路由的建议以降低成本。  

## 功能介绍  
1. **记录** 每次API调用，包括使用的模型、令牌以及产生的费用（以JSONL格式保存）  
2. **生成报告**，按模型、时间范围和使用场景展示支出情况  
3. **根据任务复杂性**，推荐更经济的模型使用方案  

## 常用指令  
- “我在AI上花了多少钱？”  
- “AI成本报告”  
- “追踪这次API调用”  
- “显示AI支出明细”  
- “成本分解”  

## 使用方法  
### 日志记录（在您的代码中）  
```python
from tracker import log_usage
log_usage(model="claude-3-haiku", input_tokens=500, output_tokens=200, task="humanize")
```  

### 报告生成  
```bash
# Full spend report
python report.py

# Last 7 days
python report.py --days 7

# By model
python report.py --by-model
```  

## 相关文件  
- `tracker.py` — 日志记录库，可导入到您的工具中  
- `report.py` — 用于支出分析的命令行界面（CLI）  
- `pricing.json` — 模型定价数据（根据需要更新）  

## 系统要求  
- Python 3.10及以上版本（仅需要标准库）  
- 无需API密钥（系统会自动记录您的使用情况）  

## 对于开发人员/运维人员  
- 查看支出情况：`python report.py`  
- 从其他工具中记录使用情况：`from tracker import log_usage`  

<!-- 🐾 Odin的乌鸦会精确统计每一枚硬币……（象征系统对数据的高效管理）