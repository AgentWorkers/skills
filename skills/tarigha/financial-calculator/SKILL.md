---
name: financial-calculator
description: 高级财务计算器，支持未来价值表、现值计算、折现计算、加价定价以及复利计算功能。适用于计算投资增长、定价策略、贷款金额、折扣，或在不同利率和时间周期内比较财务方案。提供命令行界面（CLI）和交互式网页界面（Web UI）两种使用方式。
---

# 金融计算器

提供全面的金融计算功能，包括未来价值（Future Value, FV）、现值（Present Value, PV）、折扣/加价定价（Discount/Markup Pricing）、复利（Compound Interest）以及各种比较图表。

## 快速入门

### 命令行界面（CLI）使用方法

```bash
# Future Value
python3 scripts/calculate.py fv 10000 0.05 10 12
# PV=$10,000, Rate=5%, Years=10, Monthly compounding

# Present Value
python3 scripts/calculate.py pv 20000 0.05 10 12
# FV=$20,000, Rate=5%, Years=10, Monthly compounding

# Discount
python3 scripts/calculate.py discount 100 20
# Price=$100, Discount=20%

# Markup
python3 scripts/calculate.py markup 100 30
# Cost=$100, Markup=30%

# Future Value Table
python3 scripts/calculate.py fv_table 10000 0.03 0.05 0.07 --periods 1 5 10 20
# Principal=$10,000, Rates=3%,5%,7%, Periods=1,5,10,20 years

# Discount Table
python3 scripts/calculate.py discount_table 100 10 15 20 25 30
# Price=$100, Discounts=10%,15%,20%,25%,30%
```

### 网页用户界面（Web UI）

启动交互式计算器：

```bash
./scripts/launch_ui.sh [port]
# Default port: 5050
# Opens at: http://localhost:5050
# Auto-creates venv and installs Flask if needed
```

或者手动启动：

```bash
cd skills/financial-calculator
python3 -m venv venv  # First time only
venv/bin/pip install flask  # First time only
venv/bin/python scripts/web_ui.py [port]
```

**主要功能：**
- 7种计算器类型，通过直观的标签页进行切换
- 实时计算结果
- 交互式数据表格
- 美观的渐变用户界面（gradient UI）
- 移动设备友好设计

## 计算器类型

### 1. 未来价值（FV）计算器
计算带有复利的投资在未来时的价值。

**应用场景：**
- 投资增长预测
- 储蓄账户增长分析
- 退休规划

**输入参数：**
- 投资本金
- 年利率（%）
- 时间期限（年）
- 复利频率（每年/每季度/每月/每天）

### 2. 现值（PV）计算器
计算未来金额的当前价值（折现后的价值）。

**应用场景：**
- 贷款评估
- 债券定价
- 投资分析

**输入参数：**
- 未来价值
- 年折现率（%）
- 时间期限（年）
- 复利频率

### 3. 折扣计算器
计算应用折扣百分比后的最终价格。

**应用场景：**
- 零售定价
- 销售价格计算
- 成本节约分析

**输入参数：**
- 原价
- 折扣百分比

**输出结果：**
- 折扣金额
- 最终价格
- 节省的百分比

### 4. 加价计算器
根据成本和加价百分比计算售价。

**应用场景：**
- 产品定价
- 利润率计算
- 企业定价策略

**输入参数：**
- 成本价
- 加价百分比

**输出结果：**
- 加价金额
- 售价
- 利润率（占售价的百分比）

### 5. 复利计算器
提供复利计算的详细信息。

**应用场景：**
- 利息分析
- 实际利率比较
- 贷款利息计算

**输出结果：**
- 最终金额
- 总利息收入
- 实际年利率

### 6. 未来价值表（FV Table）
生成多个利率和时间期限下的对比表格。

**应用场景：**
- 投资方案比较
- 利率选择
- 长期规划

**特点：**
- 可添加多个利率
- 可添加多个时间期限
- 表格可排序
- 显示总收益和收益百分比

### 7. 折扣表（Discount Table）
比较相同价格下的多个折扣百分比。

**应用场景：**
- 批量定价策略
- 促销活动规划
- 价格对比

## 安装要求

需要 Python 3.7 及以上版本和 Flask 框架：

```bash
pip install flask
```

或者使用虚拟环境（venv）进行安装：

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
```

## Python API

导入计算模块：

```python
from calculate import (
    future_value,
    present_value,
    discount_amount,
    markup_price,
    compound_interest,
    generate_fv_table,
    generate_discount_table
)

# Calculate FV
fv = future_value(
    present_value=10000,
    rate=0.05,  # 5% as decimal
    periods=10,
    compound_frequency=12  # Monthly
)

# Generate table
table = generate_fv_table(
    principal=10000,
    rates=[0.03, 0.05, 0.07],  # As decimals
    periods=[1, 5, 10, 20]
)
```

## 公式说明

详细数学公式、示例及所有计算方法的用途请参阅 `references/formulas.md`。

## 使用提示

**利率格式：**
- 命令行界面：使用小数形式（例如 0.05 表示 5%）
- 网页用户界面：使用百分比形式（例如 5 表示 5%）
- Python API：使用小数形式（例如 0.05 表示 5%）

**复利频率：**
- 1 = 每年（Annual）
- 4 = 每季度（Quarterly）
- 12 = 每月（Monthly）
- 365 = 每天（Daily）

**表格生成建议：**
- 为了便于分析，建议：
  - 未来价值表：使用 3-5 个利率和 4-6 个时间期限
  - 折扣表：使用 5-10 个折扣百分比
  - 保持表格简洁明了

**性能说明：**
- 网页用户界面的计算结果即时显示
- 包含超过 100 个组合的表格可能需要几秒钟生成
- 命令行界面适用于单次计算，速度最快

## 常见工作流程

### 投资规划
1. 使用 **未来价值计算器** 预测单一投资的表现
2. 生成 **未来价值表** 以比较不同利率的影响
3. 查看 **复利计算** 以获取详细分析结果

### 定价策略
1. 使用 **加价计算器** 设定售价
2. 生成 **折扣表** 以规划促销活动
3. 比较利润率及最终价格

### 贷款分析
1. 使用 **现值计算器** 评估贷款价值
2. 查看 **复利计算** 以了解总利息成本
3. 生成 **未来价值表** 以比较不同贷款条款