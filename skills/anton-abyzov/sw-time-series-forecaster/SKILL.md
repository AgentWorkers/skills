---
name: time-series-forecaster
description: |
  Time series forecasting with ARIMA, Prophet, LSTM, and statistical methods. Activates for "time series", "forecasting", "predict future", "trend analysis", "seasonality", "ARIMA", "Prophet", "sales forecast", "demand prediction", "stock prediction". Handles trend decomposition, seasonality detection, multivariate forecasting, and confidence intervals with SpecWeave increment integration.
---

# 时间序列预测

## 概述

专为时间依赖型数据设计的预测流程。通过统计方法、机器学习和深度学习技术来处理趋势分析、季节性检测和未来预测——所有这些功能都集成在 SpecWeave 的增量工作流中。

## 时间序列数据的特殊性

**标准机器学习假设的违反**：
- ❌ 数据并非独立（存在时间相关性）
- ❌ 数据分布不均匀（存在趋势和季节性变化）
- ❌ 随机划分训练集和测试集的方法是错误的（会破坏时间顺序）

**时间序列数据的要求**：
- ✅ 保持时间顺序
- ✅ 避免使用未来的数据
- ✅ 进行平稳性检验
- ✅ 进行自相关分析
- ✅ 进行季节性分解

## 预测方法

### 1. 统计方法（基础方法）

**ARIMA（自回归积分滑动平均）**：
```python
from specweave import TimeSeriesForecaster

forecaster = TimeSeriesForecaster(
    method="arima",
    increment="0042"
)

# Automatic order selection (p, d, q)
forecaster.fit(train_data)

# Forecast next 30 periods
forecast = forecaster.predict(horizon=30)

# Generates:
# - Trend analysis
# - Seasonality decomposition
# - Autocorrelation plots (ACF, PACF)
# - Residual diagnostics
# - Forecast with confidence intervals
```

**季节性分解**：
```python
# Decompose into trend + seasonal + residual
decomposition = forecaster.decompose(
    data=sales_data,
    model='multiplicative',  # Or 'additive'
    period=12  # Monthly seasonality
)

# Creates:
# - Trend component plot
# - Seasonal component plot
# - Residual component plot
# - Strength of trend/seasonality metrics
```

### 2. Prophet（Facebook 开发的工具）

**适用场景**：商业时间序列数据（如销售数据、网站流量、用户增长等）
```python
from specweave import ProphetForecaster

forecaster = ProphetForecaster(increment="0042")

# Prophet handles:
# - Multiple seasonality (daily, weekly, yearly)
# - Holidays and events
# - Missing data
# - Outliers

forecaster.fit(
    data=sales_data,
    holidays=us_holidays,  # Built-in holiday effects
    seasonality_mode='multiplicative'
)

forecast = forecaster.predict(horizon=90)

# Generates:
# - Trend + seasonality + holiday components
# - Change point detection
# - Uncertainty intervals
# - Cross-validation results
```

**使用自定义回归器的 Prophet**：
```python
# Add external variables (marketing spend, weather, etc.)
forecaster.add_regressor("marketing_spend")
forecaster.add_regressor("temperature")

# Prophet incorporates external factors into forecast
```

### 3. 深度学习（LSTM/GRU）

**适用场景**：处理复杂模式、多变量预测以及非线性关系
```python
from specweave import LSTMForecaster

forecaster = LSTMForecaster(
    lookback_window=30,  # Use 30 past observations
    horizon=7,  # Predict 7 steps ahead
    increment="0042"
)

# Automatically handles:
# - Sequence creation
# - Train/val/test split (temporal)
# - Scaling
# - Early stopping

forecaster.fit(
    data=sensor_data,
    epochs=100,
    batch_size=32
)

forecast = forecaster.predict(horizon=7)

# Generates:
# - Training history plots
# - Validation metrics
# - Attention weights (if using attention)
# - Forecast uncertainty estimation
```

### 4. 多变量预测

**VAR（向量自回归）**：用于处理多个相关的时间序列数据
```python
from specweave import VARForecaster

# Forecast multiple related series simultaneously
forecaster = VARForecaster(increment="0042")

# Example: Forecast sales across multiple stores
# Each store's sales affects others
forecaster.fit(data={
    'store_1_sales': store1_data,
    'store_2_sales': store2_data,
    'store_3_sales': store3_data
})

forecast = forecaster.predict(horizon=30)
# Returns forecasts for all 3 stores
```

## 时间序列预测的最佳实践

### 1. 时间序列数据的训练集/测试集划分

```python
# ❌ WRONG: Random split (data leakage!)
X_train, X_test = train_test_split(data, test_size=0.2)

# ✅ CORRECT: Temporal split
split_date = "2024-01-01"
train = data[data.index < split_date]
test = data[data.index >= split_date]

# Or use last N periods as test
train = data[:-30]  # All but last 30 observations
test = data[-30:]   # Last 30 observations
```

### 2. 平稳性检验

```python
from specweave import TimeSeriesAnalyzer

analyzer = TimeSeriesAnalyzer(increment="0042")

# Check stationarity (required for ARIMA)
stationarity = analyzer.check_stationarity(data)

if not stationarity['is_stationary']:
    # Make stationary via differencing
    data_diff = analyzer.difference(data, order=1)
    
    # Or detrend
    data_detrended = analyzer.detrend(data)
```

**平稳性检验报告**：
```markdown
# Stationarity Analysis

## ADF Test (Augmented Dickey-Fuller)
- Test Statistic: -2.15
- P-value: 0.23
- Critical Value (5%): -2.89
- Result: ❌ NON-STATIONARY (p > 0.05)

## Recommendation
Apply differencing (order=1) to remove trend.

After differencing:
- ADF Test Statistic: -5.42
- P-value: 0.0001
- Result: ✅ STATIONARY
```

### 3. 季节性检测

```python
# Automatic seasonality detection
seasonality = analyzer.detect_seasonality(data)

# Results:
# - Daily: False
# - Weekly: True (period=7)
# - Monthly: True (period=30)
# - Yearly: False
```

### 4. 时间序列数据的交叉验证

```python
# Time series cross-validation (expanding window)
cv_results = forecaster.cross_validate(
    data=data,
    horizon=30,  # Forecast 30 steps ahead
    n_splits=5,  # 5 expanding windows
    metric='mape'
)

# Visualizes:
# - MAPE across different time periods
# - Forecast vs actual for each fold
# - Model stability over time
```

### 5. 处理缺失数据

```python
# Time series-specific imputation
forecaster.handle_missing(
    method='interpolate',  # Or 'forward_fill', 'backward_fill'
    limit=3  # Max consecutive missing values to fill
)

# For seasonal data
forecaster.handle_missing(
    method='seasonal_interpolate',
    period=12  # Use seasonal pattern to impute
)
```

## 常见的时间序列数据模式

### 模式 1：销售预测

```python
from specweave import SalesForecastPipeline

pipeline = SalesForecastPipeline(increment="0042")

# Handles:
# - Weekly/monthly seasonality
# - Holiday effects
# - Marketing campaign impact
# - Trend changes

pipeline.fit(
    sales_data=daily_sales,
    holidays=us_holidays,
    regressors={
        'marketing_spend': marketing_data,
        'competitor_price': competitor_data
    }
)

forecast = pipeline.predict(horizon=90)  # 90 days ahead

# Generates:
# - Point forecast
# - Prediction intervals (80%, 95%)
# - Component analysis (trend, seasonality, regressors)
# - Anomaly flags for past data
```

### 模式 2：需求预测

```python
from specweave import DemandForecastPipeline

# Inventory optimization, supply chain planning
pipeline = DemandForecastPipeline(
    aggregation='daily',  # Or 'weekly', 'monthly'
    increment="0042"
)

# Multi-product forecasting
forecasts = pipeline.fit_predict(
    products=['product_A', 'product_B', 'product_C'],
    horizon=30
)

# Generates:
# - Demand forecast per product
# - Confidence intervals
# - Stockout risk analysis
# - Reorder point recommendations
```

### 模式 3：股票价格预测

```python
from specweave import FinancialForecastPipeline

# Stock prices, crypto, forex
pipeline = FinancialForecastPipeline(increment="0042")

# Handles:
# - Volatility clustering
# - Non-linear patterns
# - Technical indicators

pipeline.fit(
    price_data=stock_prices,
    features=['volume', 'volatility', 'RSI', 'MACD']
)

forecast = pipeline.predict(horizon=7)

# Generates:
# - Price forecast with confidence bands
# - Volatility forecast (GARCH)
# - Trading signals (optional)
# - Risk metrics
```

### 模式 4：传感器数据 / 物联网数据

```python
from specweave import SensorForecastPipeline

# Temperature, humidity, machine metrics
pipeline = SensorForecastPipeline(
    method='lstm',  # Deep learning for complex patterns
    increment="0042"
)

# Multivariate: Multiple sensor readings
pipeline.fit(
    sensors={
        'temperature': temp_data,
        'humidity': humidity_data,
        'pressure': pressure_data
    }
)

forecast = pipeline.predict(horizon=24)  # 24 hours ahead

# Generates:
# - Multi-sensor forecasts
# - Anomaly detection (unexpected values)
# - Maintenance alerts
```

## 评估指标

**针对时间序列数据的特定评估指标**：
```python
from specweave import TimeSeriesEvaluator

evaluator = TimeSeriesEvaluator(increment="0042")

metrics = evaluator.evaluate(
    y_true=test_data,
    y_pred=forecast
)

# Metrics:
# - MAPE (Mean Absolute Percentage Error) - business-friendly
# - RMSE (Root Mean Squared Error) - penalizes large errors
# - MAE (Mean Absolute Error) - robust to outliers
# - MASE (Mean Absolute Scaled Error) - scale-independent
# - Directional Accuracy - did we predict up/down correctly?
```

**评估报告**：
```markdown
# Time Series Forecast Evaluation

## Point Metrics
- MAPE: 8.2% (target: <10%) ✅
- RMSE: 124.5
- MAE: 98.3
- MASE: 0.85 (< 1 = better than naive forecast) ✅

## Directional Accuracy
- Correct direction: 73% (up/down predictions)

## Forecast Bias
- Mean Error: -5.2 (slight under-forecasting)
- Bias: -2.1%

## Confidence Intervals
- 80% interval coverage: 79.2% ✅
- 95% interval coverage: 94.1% ✅

## Recommendation
✅ DEPLOY: Model meets accuracy targets and is well-calibrated.
```

## 与 SpecWeave 的集成

### SpecWeave 的增量工作流结构

```
.specweave/increments/0042-sales-forecast/
├── spec.md (forecasting requirements, accuracy targets)
├── plan.md (forecasting strategy, method selection)
├── tasks.md
├── data/
│   ├── train_data.csv
│   ├── test_data.csv
│   └── schema.yaml
├── experiments/
│   ├── arima-baseline/
│   ├── prophet-holidays/
│   └── lstm-multivariate/
├── models/
│   ├── prophet_model.pkl
│   └── lstm_model.h5
├── forecasts/
│   ├── forecast_2024-01.csv
│   ├── forecast_2024-02.csv
│   └── forecast_with_intervals.csv
└── analysis/
    ├── stationarity_test.md
    ├── seasonality_decomposition.png
    └── forecast_evaluation.md
```

### 文档的实时更新机制

```bash
/sw:sync-docs update
```

## 命令操作

```bash
# Create time series forecast
/ml:forecast --horizon 30 --method prophet

# Evaluate forecast
/ml:evaluate-forecast 0042

# Decompose time series
/ml:decompose-timeseries 0042
```

## 高级功能

### 1. 集成预测（Ensemble Forecasting）

```python
# Combine multiple methods for robustness
ensemble = EnsembleForecast(increment="0042")

ensemble.add_forecaster("arima", weight=0.3)
ensemble.add_forecaster("prophet", weight=0.5)
ensemble.add_forecaster("lstm", weight=0.2)

# Weighted average of all forecasts
forecast = ensemble.predict(horizon=30)

# Ensemble typically 10-20% more accurate than single model
```

### 2. 预测结果的一致性校验

```python
# For hierarchical time series (e.g., total sales = store1 + store2 + store3)
reconciler = ForecastReconciler(increment="0042")

# Ensures forecasts sum correctly
reconciled = reconciler.reconcile(
    forecasts={
        'total': total_forecast,
        'store1': store1_forecast,
        'store2': store2_forecast,
        'store3': store3_forecast
    },
    method='bottom_up'  # Or 'top_down', 'middle_out'
)
```

### 3. 预测结果的监控

```python
# Track forecast accuracy over time
monitor = ForecastMonitor(increment="0042")

# Compare forecasts vs actuals
monitor.track_performance(
    forecasts=past_forecasts,
    actuals=actual_values
)

# Alerts when accuracy degrades
if monitor.accuracy_degraded():
    print("⚠️ Forecast accuracy dropped 15% - retrain model!")
```

## 总结

时间序列预测需要采用专门的技术：
- ✅ 保持时间顺序（避免随机划分数据）
- ✅ 进行平稳性检验
- ✅ 检测数据中的季节性变化
- ✅ 进行趋势分解
- ✅ 使用交叉验证方法
- ✅ 计算预测的置信区间
- ✅ 监控预测结果

该技能能够在 SpecWeave 的增量工作流中处理所有时间序列数据的复杂性，确保预测结果的可重复性、可记录性以及适用于生产环境。