---
name: vnstock-free-expert
description: 运行一个端到端的 vnstock 工作流程，用于免费 tier 下的越南股票估值、排名以及 API 操作，并具备严格的速率限制控制功能；当用户在免费 tier 的限制下请求越南股票分析时，会使用该流程。
compatibility: Requires Python 3.x, vnstock package, pandas, internet access, and optional VNSTOCK_API_KEY in .env.
---
# VNStock 免费专家技能

当用户需要使用 `vnstock` 进行高级越南股票分析，同时确保在免费 tier 的使用限制范围内时，可以使用此技能。

## 重要说明
此技能是自包含的，无需单独传输 `vnstock/` 文档文件夹。  
代理所需的所有操作知识都存储在以下路径：
- `references/`

## 阅读顺序
1. 阅读 `references/capabilities.md`。
2. 阅读 `references/method_matrix.md` 以获取类/方法的详细映射关系。
3. 在进行大规模数据分析之前，先阅读 `references/free_tier_playbook.md`。

## 使用范围和限制
- 仅支持 `vnstock` 库。
- 首选数据源为 `kbs`，备用数据源为 `vci`；严禁使用 `tcbs`。
- 除非用户确认其安装的 `vnstock` 版本中已恢复 `Screener API` 的功能，否则将其视为不可用。

## 免费 tier 的使用规则
- 无 API 密钥时：每分钟请求次数不超过 20 次。
- 使用免费 API 密钥时：每分钟请求次数不超过 60 次。
- 脚本中的默认执行速率为每请求 3.2 秒。
- 可以在步骤之间重用缓存的数据结果。

## 共享的信心评估标准（必填）
使用以下标准来评估分析结果的可靠性：
- **高**：覆盖范围 >= 95%，关键指标覆盖率 >= 80%，且错误率（针对所有股票） <= 5%。
- **中**：覆盖范围 >= 80%，关键指标覆盖率 >= 60%，且错误率 <= 15%。
- **低**：低于上述标准，或存在可能导致排名结果变化的缺失字段。

## 必须输出的内容
1. 信心等级。
2. 覆盖情况统计（请求的股票数量、评分的股票数量、按关键指标缺失的数据数量）。
3. 可能影响分析结果的缺失字段列表。

## API 密钥配置（已实现）
- 技能相关的密钥文件：`.env`
- 变量：`VNSTOCK_API_KEY`
- 所有调用 API 的脚本都会自动加载此密钥，并在请求前执行 `vnstock` 的身份验证设置。
- 可以通过 `--api-key "..."` 参数在每次运行时覆盖该密钥的值。

## 执行流程（按顺序）
1. 验证环境（`python`、`vnstock`、`pandas`）并从 `.env` 文件中加载 API 密钥（如需）。
2. 使用 `scripts/build_universe.py`（`group`、`exchange` 或 `symbols` 模式）构建股票数据集。
3. 使用 `scripts/collect_market_data.py` 以安全的执行速率收集市场数据。
4. 使用 `scripts/collect_fundamentals.py` 收集财务数据。
5. 使用 `scripts/score_stocks.py` 对股票进行评分和排名。
6. 使用 `scripts/generate_report.py` 生成分析师风格的报告。
7. 应用信心评估标准，列出缺失的字段，并总结潜在风险。

## 脚本映射

### A) 发现和通用功能调用（适用于广泛的功能覆盖）
- `catalog_vnstock.py`
  路径：`scripts/catalog_vnstock.py`
  用途：
  - 检查已安装的 `vnstock` 版本中可用的类和方法。
  - 在运行特定方法之前确认兼容性。

- `invoke_vnstock.py`
  路径：`scripts/invoke_vnstock.py`
  用途：
  - 调用 `vnstock` 中提供的任何类或方法（不包括预构建的估值流程）。
  - 作为 `Listing`、`Quote`、`Company`、`Finance`、`Trading`、`Fund` 等类的通用入口点。
  - 该脚本支持通过类名和方法名以及 JSON 参数进行动态调用。

### B) 估值流程脚本
- `build_universe.py`
  用途：根据指数、交易所或自定义股票列表构建股票数据集。
  输入：数据来源、模式以及分组/交易所/股票列表。
  输出：`outputs/universe_*.csv` 文件及最新的数据引用。

- `collect_market_data.py`
  用途：收集股票的 OHLCV（开高收低）和动量指标数据（3 个月、6 个月、12 个月的回报数据）。
  输入：股票数据集的 CSV 文件路径。
  输出：`outputs/market_data_*.csv` 文件及每只股票的错误信息（以 JSON 格式）。

- `collect_fundamentals.py`
  用途：从财务/公司 API 中收集估值和基础数据。
  输入：股票数据集的 CSV 文件路径。
  输出：`outputs/fundamentals_*.csv` 文件及每只股票的错误信息（以 JSON 格式）。

- `score_stocks.py`
  用途：对股票进行综合评分和排名。
  输入：包含市场数据和财务数据的 CSV 文件。
  输出：`outputs/ranking_*.csv` 文件。

- `generate_report.py`
  用途：将排名结果转换为分析师风格的 Markdown 报告。
  输入：排名结果的 CSV 文件。
  输出：`outputs/investment_memo_*.md` 文件。

- `run_pipeline.py`
  用途：一次性执行整个估值流程。
  输入：数据来源和数据集构建模式。
  输出：上述所有处理结果。

## 错误处理规则
1. 记录失败股票的详细信息，并继续处理剩余的股票。
2. 对于缺失的指标，不要将其视为零值，而是标记为“缺失”。
3. 如果某个关键步骤失败，停止当前操作并报告失败的原因及建议的重试方案。

## 推荐的决策逻辑
1. 如果请求是“标准估值/排名”操作，直接运行流程脚本。
2. 如果请求需要 `vnstock` 的特定功能但该功能不在流程中，先使用 `catalog_vnstock.py`，再使用 `invoke_vnstock.py`。
3. 如果请求量较大，应遵循 `free_tier_playbook.md` 中规定的限流和分批处理策略。

## 信心评估（必填）
当输出包含排名结果和估值分析时，需进行以下评估：
1. 根据覆盖率和错误率计算数据的可靠性。
2. 根据方法的稳健性（单指标与多因素一致性）评估模型的可靠性。
3. 最终的信心等级为数据可靠性和模型可靠性的较低值。
4. 在信心等级较低的情况下，仅提供方向性分析结果，并列出缺失的输入信息。

## 必需的输出模板
1. **执行内容**：使用的脚本、数据来源、数据集范围及执行速率。
2. **覆盖情况**：请求的股票数量、评分结果以及按关键字段划分的缺失数据情况。
3. **排名结果**：包含评分信息的排名列表。
4. **主要风险**：数据集中存在的问题（如数据过时、关键指标缺失或服务提供商的限制）。
5. **信心评估与问题分析**：最终的信心等级及具体问题所在。

## 快速命令示例
```bash
python scripts/catalog_vnstock.py --outdir ./outputs
python scripts/invoke_vnstock.py --class-name Quote --init-kwargs '{"source":"kbs","symbol":"VCB"}' --method history --method-kwargs '{"start":"2024-01-01","end":"2024-12-31","interval":"1D"}' --outdir ./outputs
python scripts/run_pipeline.py --source kbs --mode group --group VN30 --outdir ./outputs
```

## 使用示例
- “使用 `vnstock` 分析 VN30 指数，同时确保在免费 tier 的使用范围内。”
- “利用 KBS 数据，按价值/质量/动量对越南股票进行排名。”
- “运行完整的 `vnstock` 流程，并返回带有风险提示的排名结果。”