---
name: pywayne-statistics
description: 这是一个全面的统计测试库，提供了37种以上的测试方法，用于检测数据的正态性、位置分布、相关性、时间序列特征以及模型诊断。适用于假设检验、A/B测试、数据质量检查、时间序列分析或回归模型验证等场景。所有测试方法都会返回统一的`TestResult`对象，该对象具有统一的接口，包含p值、统计量、置信区间和效应量等关键信息。
---
# Pywayne Statistics

这是一个全面的统计测试库，用于假设检验、A/B测试和数据分析。

## 快速入门

```python
from pywayne.statistics import NormalityTests, LocationTests
import numpy as np

# Test data normality
nt = NormalityTests()
data = np.random.normal(0, 1, 100)
result = nt.shapiro_wilk(data)
print(f"p-value: {result.p_value:.4f}, is_normal: {not result.reject_null}")

# Compare two groups
lt = LocationTests()
group_a = np.random.normal(100, 15, 50)
group_b = np.random.normal(105, 15, 50)
result = lt.two_sample_ttest(group_a, group_b)
print(f"Significant difference: {result.reject_null}")
```

## 测试类别

### 正态性测试（`NormalityTests`）

用于检测数据是否遵循正态分布或其他指定的分布。

| 方法 | 描述 | 使用场景 |
|---------|-------------|-----------|
| `shapiro_wilk` | Shapiro-Wilk检验 | 样本量较小至中等（n ≤ 5000） |
| `ks_test_normal` | K-S正态性检验 | 样本量较大 |
| `ks_test_two_sample` | 双样本K-S检验 | 比较两个样本的分布 |
| `anderson_darling` | Anderson-Darling检验 | 对尾部敏感的正态性检验 |
| `dagostino_pearson` | D'Agostino-Pearson K²检验 | 基于偏度和峰度 |
| `jarque_bera` | Jarque-Bera检验 | 大样本，回归残差 |
| `chi_square_goodness_of_fit` | 卡方拟合优度检验 | 分类数据 |
| `lilliefors_test` | Lilliefors检验 | 未知参数的K-S检验 |

**示例：**
```python
from pywayne.statistics import NormalityTests

nt = NormalityTests()
result = nt.shapiro_wilk(data)
if result.p_value < 0.05:
    print("Data is NOT normally distributed")
else:
    print("Data follows normal distribution")
```

### 位置性测试（`LocationTests`）

用于比较不同组间的均值或中位数（参数化和非参数化方法）。

| 方法 | 描述 | 使用场景 |
|---------|-------------|-----------|
| `one_sample_ttest` | 单样本t检验 | 比较样本均值与给定值 |
| `two_sample_ttest` | 双样本t检验 | 比较两个独立组的均值 |
| `paired_ttest` | 配对t检验 | 比较配对数据的前后差异 |
| `one_way_anova` | 单因素方差分析 | 比较3个及以上组的均值 |
| `mann_whitney_u` | Mann-Whitney U检验 | 非参数双样本检验 |
| `wilcoxon_signed_rank` | Wilcoxon符号秩检验 | 非参数配对检验 |
| `kruskal_wallis` | Kruskal-Wallis H检验 | 非参数多组检验 |

**示例（A/B测试）：**
```python
from pywayne.statistics import LocationTests, NormalityTests

lt = LocationTests()
nt = NormalityTests()

# Check normality first
if nt.shapiro_wilk(control).p_value > 0.05:
    result = lt.two_sample_ttest(control, treatment)
else:
    result = lt.mann_whitney_u(control, treatment)

print(f"Effect significant: {result.reject_null}")
```

### 相关性测试（`CorrelationTests`）

用于检测变量之间的相关性以及分类变量的独立性。

| 方法 | 描述 | 使用场景 |
|---------|-------------|-----------|
| `pearson_correlation` | Pearson相关系数 | 线性关系 |
| `spearman_correlation` | Spearman等级相关系数 | 单调关系 |
| `kendall_tau` | Kendall's tau系数 | 小样本的等级相关性 |
| `chi_square_independence` | 卡方独立性检验 | 分类变量 |
| `fisher_exact_test` | Fisher精确检验 | 2×2列联表 |
| `mcnemar_test` | McNemar检验 | 配对分类数据 |

**示例：**
```python
from pywayne.statistics import CorrelationTests

ct = CorrelationTests()
result = ct.pearson_correlation(x, y)
print(f"Correlation: {result.statistic:.3f}, p-value: {result.p_value:.4f}")
```

### 时间序列测试（`TimeSeriesTests`）

用于检测时间序列的属性：平稳性、自相关性、协整性。

| 方法 | 描述 | 使用场景 |
|---------|-------------|-----------|
| `adf_test` | Augmented Dickey-Fuller检验 | 平稳性检验 |
| `kpss_test` | KPSS检验 | 平稳性检验（补充ADF检验） |
| `ljung_box_test` | Ljung-Box Q检验 | 整体自相关性 |
| `runs_test` | 运行检验 | 随机性检验 |
| `arch_test` | ARCH效应检验 | 异方差性 |
| `granger_causality` | Granger因果关系检验 | 因果关系 |
| `engle_granger_cointegration` | Engle-Granger协整检验 | 长期均衡 |
| `breusch_godfrey_test` | Breusch-Godfrey检验 | 高阶自相关性 |

**示例：**
```python
from pywayne.statistics import TimeSeriesTests

tst = TimeSeriesTests()
adf_result = tst.adf_test(time_series_data)
kpss_result = tst.kpss_test(time_series_data)

if adf_result.reject_null:
    print("Series is stationary")
else:
    print("Series has unit root (non-stationary)")
```

### 模型诊断（`ModelDiagnostics`）

用于回归模型的诊断：异方差性、自相关性、多重共线性。

| 方法 | 描述 | 使用场景 |
|---------|-------------|-----------|
| `breusch_pagan_test` | Breusch-Pagan检验 | 异方差性检验 |
| `white_test` | White检验 | 一般异方差性 |
| `goldfeld_quandt_test` | Goldfeld-Quandt检验 | 结构性突变引起的异方差性 |
| `durbin_watson_test` | Durbin-Watson检验 | 一阶自相关性 |
| `variance_inflation_factor` | VIF（方差膨胀因子） | 多重共线性诊断 |
| `levene_test` | Levene检验 | 方差齐性检验 |
| `bartlett_test` | Bartlett检验 | 正态性假设检验 |
| `residual_normality_test` | 残差正态性检验 | 回归假设检验 |

**示例：**
```python
from pywayne.statistics import ModelDiagnostics

md = ModelDiagnostics()
residuals = y - model.predict(X)

# Check assumptions
bp_result = md.breusch_pagan_test(residuals, X)
dw_result = md.durbin_watson_test(residuals)

if bp_result.reject_null:
    print("Warning: Heteroscedasticity detected")
```

## `TestResult` 对象

所有测试方法都会返回一个统一的`TestResult`对象：

```python
result = nt.shapiro_wilk(data)

# Access results
result.test_name        # Test method name
result.statistic        # Test statistic value
result.p_value          # P-value
result.reject_null      # True if null hypothesis is rejected
result.critical_value   # Critical value (if applicable)
result.confidence_interval # Tuple (lower, upper) if applicable
result.effect_size      # Effect size if applicable
result.additional_info  # Dict with additional information
```

## 实用函数

### `list_all_tests()`

列出所有模块中可用的测试方法。

```python
from pywayne.statistics import list_all_tests
print(list_all_tests())
```

### `show_test_usage(method_name)`

显示特定测试的用法和文档。

```python
from pywayne.statistics import show_test_usage
show_test_usage('shapiro_wilk')
```

## 方法选择指南

### 正态性测试

| 样本量 | 推荐方法 |
|-------------|-------------------|
| n < 30 | Shapiro-Wilk |
| 30 ≤ n ≤ 300 | Shapiro-Wilk, D'Agostino-Pearson |
| n > 300 | Jarque-Bera, Kolmogorov-Smirnov |

### 位置性测试

| 条件 | 参数化方法 | 非参数方法 |
|-----------|-------------|----------------|
| 正态数据 | t检验、方差分析 | - |
| 非正态数据 | Mann-Whitney U检验、Kruskal-Wallis检验 |
| 配对数据 | 配对t检验 | Wilcoxon符号秩检验 |

## 多重检验校正

在进行多次检验时，需要应用p值校正：

```python
from statsmodels.stats.multitest import multipletests

p_values = [r.p_value for r in results]
rejected, p_corrected, _, _ = multipletests(
    p_values, alpha=0.05, method='fdr_bh'
)
```

## 常见应用

### 数据质量检查

```python
def data_quality_check(data):
    nt = NormalityTests()
    lt = LocationTests()

    normality = nt.shapiro_wilk(data)

    # Outlier detection (IQR)
    Q1, Q3 = np.percentile(data, [25, 75])
    IQR = Q3 - Q1
    outliers = data[(data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)]

    return {
        'size': len(data),
        'is_normal': not normality.reject_null,
        'p_value': normality.p_value,
        'outliers': len(outliers)
    }
```

### A/B测试工作流程

```python
def ab_test_analysis(control, treatment):
    nt = NormalityTests()
    lt = LocationTests()

    # Check normality
    norm_c = nt.shapiro_wilk(control[:100])
    norm_t = nt.shapiro_wilk(treatment[:100])

    # Choose appropriate test
    if norm_c.p_value > 0.05 and norm_t.p_value > 0.05:
        result = lt.two_sample_ttest(control, treatment)
    else:
        result = lt.mann_whitney_u(control, treatment)

    return {
        'test_used': result.test_name,
        'p_value': result.p_value,
        'significant': result.reject_null,
        'effect_size': result.effect_size
    }
```

### 回归模型诊断

```python
def diagnose_model(y, X, model):
    md = ModelDiagnostics()
    residuals = y - model.predict(X)

    return {
        'heteroscedasticity_bp': md.breusch_pagan_test(residuals, X).reject_null,
        'autocorrelation_dw': md.durbin_watson_test(residuals).statistic,
        'residuals_normal': md.residual_normality_test(residuals).p_value,
        'vif_max': max(md.variance_inflation_factor(X))
    }
```

## 注意事项

- 所有方法都接受`np.ndarray`或列表作为输入。
- 所有方法返回具有统一接口的`TestResult`对象。
- 在应用参数化检验之前，务必验证检验假设。
- 进行多次检验时，需要应用多重检验校正。
- 为了全面解释结果，应同时报告效应大小和p值。