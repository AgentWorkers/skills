# 亚马逊FBA费用计算器 — 清楚了解您的实际利润

**别再猜测了。在销售任何一件商品之前，就能准确知道您的收益。**

## 产品描述
这是一个全面的亚马逊FBA（Fulfillment by Amazon）盈利能力计算器，支持2026年的费用标准。它可以计算推荐费用、FBA配送费用、存储成本以及净利润。同时支持所有产品尺寸等级和20多个产品类别。

## 使用场景
- 用户需要计算亚马逊FBA的盈利能力
- 用户询问亚马逊的费用、利润率或投资回报率（ROI）
- 用户正在考虑是否在亚马逊上销售产品
- 用户希望比较FBA和FBM（Fulfillment by Merchant）的成本
- 用户提及商品成本（COGS）、利润率或盈亏平衡价格

## 使用方法
```bash
# Basic: selling price + product cost
cd <skill_dir>/scripts && python3 calculator.py 24.99 5.00

# Full options
cd <skill_dir>/scripts && python3 calculator.py 9.95 2.00 --ship 0.50 --weight 8 --category grocery --units 200 --ppc 1.50
```

## 参数选项
- `--ship COST` — 每件商品的FBA运输费用
- `--weight OZ` — 产品的重量（以盎司为单位）
- `--dims L W H` — 产品的尺寸（以英寸为单位）
- `--category CAT` — 产品类别（食品杂货、美容用品、电子产品等）
- `--units N` — 每月的销售数量（用于预测）
- `--ppc COST` — 每件商品的PPC/广告费用

## 计算内容
- 推荐费用（根据产品类别及费用阈值计算）
- FBA配送费用（根据产品重量和尺寸等级计算）
- 每月的存储费用（按单位计算，包含季节性调整）
- 每件商品的总成本
- 每件商品的利润、利润率及投资回报率（ROI）
- 每月和每年的利润预测
- 盈亏平衡销售价格

## 无依赖项
完全使用Python 3编写，无需安装任何第三方库（如pip），也不需要API密钥。适用于任何环境。