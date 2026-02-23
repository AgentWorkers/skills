---
name: "cost-prediction"
description: "使用机器学习预测建筑工程成本。基于历史项目数据，分别应用线性回归（Linear Regression）、K-近邻（K-Nearest Neighbors）和随机森林（Random Forest）模型进行训练、评估和部署成本预测模型。"
---
# 使用机器学习进行建筑成本预测

## 概述

基于DDC方法论（第4.5章），本技能能够利用历史数据和机器学习算法来预测建筑项目的成本。该方法将传统的专家评估方式转变为数据驱动的预测方法。

**参考书籍**：《未来：预测与机器学习》（"Будущее: Прогнозы и машинное обучение"）

> “基于历史数据的预测和预估可以帮助企业更准确地判断项目的成本和工期。”
——DDC书籍，第4.5章

## 核心概念

```plaintext
历史数据 → 特征工程 → 机器学习模型 → 成本预测
    │                    │                │              │
    ▼                    ▼                ▼              ▼
    过往项目      数据准备      模型训练    新项目
        （包含成本数据）        用于机器学习      成本预测
```

## 快速入门

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# 加载历史项目数据
df = pd.read_csv("historical_projects.csv")

# 特征和目标变量
X = df[['area_m2', 'floors', 'complexity_score']
y = df['total_cost']

# 数据分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 进行预测
predictions = model.predict(X_test)
print(f"R²得分：{r2_score(y_test, predictions):.2f}")
print(f"平均绝对误差（MAE）：{mean_absolute_error(y_test, predictions):,.0f}")
```

## 数据准备

### 准备历史数据集

```python
import pandas as pd
import numpy as np

def prepare_cost_dataset(df):
    """为机器学习准备历史项目数据"""
    # 选择相关特征
    features = [
        'area_m2',
        'floors',
        'complexity_score',
    ]

    df = df[features].copy()

    # 处理缺失值
    df = df.dropna(subset=['total_cost'])

    # 对分类变量进行编码
    df = pd.get_dummies(df, columns=['building_type', 'location'])

    # 计算衍生特征
    df['cost_per_m2'] = df['total_cost'] / df['area_m2']
    df['cost_per_floor'] = df['total_cost'] / df['floors']

    # 调整通货膨胀（至当前年份价格）
    current_year = 2024
    inflation_rate = 0.03  # 年通货膨胀率为3%
    df['years_ago'] = current_year - df['year_completed']
    df['adjusted_cost'] = df['total_cost'] * (1 + inflation_rate) ** df['years_ago']

    return df
```

### 特征工程

```python
def engineer_features(df):
    """创建额外特征以提升预测准确性"""
    # 计算交互特征
    df['area_x_floors'] = df['area_m2'] * df['floors']
    df['area_x_complexity'] = df['area_m2'] * df['complexity_score']

    # 对数值特征进行对数转换
    df['log_area'] = np.log1p(df['area_m2'])

    # 对面积进行分箱处理
    df['size_category'] = pd.cut(
        df['area_m2'],
        bins=[0, 1000, 5000, 10000, float('inf')],
        labels=['small', 'medium', 'large', 'xlarge']
    )

    return df
```

## 机器学习模型

### 线性回归

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def train_linear_model(X_train, y_train):
    """使用标准化方法训练线性回归模型"""
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ]

    pipeline.fit(X_train, y_train)

    # 输出特征重要性
    coefficients = pd.DataFrame({
        'feature': X_train.columns,
        'coefficient': pipeline.named_steps['regressor'].coef()
    }).sort_values('coefficient', key=abs, ascending=False)

    return pipeline, coefficients
```

### K近邻（KNN）

```python
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def train_knn_model(X_train, y_train):
    """使用网格搜索找到最佳的K值"""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    # 使用交叉验证找到最佳K值
    param_grid = {'n_neighbors': range(3, 20)}
    knn = KNeighborsRegressor()
    grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_absolute_error')
    grid_search.fit(X_scaled, y_train)

    return grid_search.best_estimator_, scaler
```

### 随机森林（Random Forest）

```python
from sklearn.ensemble import RandomForestRegressor

def train_random_forest(X_train, y_train):
    """训练随机森林模型"""
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    rf.fit(X_train, y_train)

    # 输出特征重要性
    importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf.feature_importances()
    }).sort_values('importance', ascending=False)

    return rf, importance
```

### 梯度提升（Gradient Boosting）

```python
from sklearn.ensemble import GradientBoostingRegressor

def train_gradient_boosting(X_train, y_train):
    """训练梯度提升模型"""
    gb = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    gb.fit(X_train, y_train)
```

## 模型评估

### 综合评估

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def evaluate_model(model, X_test, y_test, model_name="Model"):
    """对模型进行综合评估"""
    predictions = model.predict(X_test)

    metrics = {
        'MAE': mean_absolute_error(y_test, predictions),
        'RMSE': np.sqrt(mean_squared_error(y_test, predictions)),
        'R²': r2_score(y_test, predictions),
        'MAPE': np.mean(np.abs((y_test - predictions) / y_test) * 100)
    }

    print(f"{model_name} 评估结果：")
    print(
        f"  平均绝对误差（MAE）：{metrics['MAE】:,.0f}"
        f"  均方根误差（RMSE）：{metrics['RMSE】:,.0f}"
        f"  R²得分：{metrics['R²']:.3f}"
        f"  平均绝对百分比误差（MAPE）：{metrics['MAPE']:%.1f}"
    )

    return metrics, predictions
```

### 比较多个模型

```python
def compare_models(models, X_test, y_test):
    """比较多个模型"""
    results = []

    for name, model in models.items():
        metrics, _ = evaluate_model(model, X_test, y_test, name)
        metrics['Model'] = name
        results.append(metrics)

    comparison = pd.DataFrame(results)
    comparison = comparison.set_index('Model')

    print("\n模型比较结果：")
    print(comparison.round(2))

    return comparison
```

### 交叉验证

```python
from sklearn.model_selection import cross_val_score

def cross_validate_model(model, X, y, cv=5):
    """进行交叉验证"""
    scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_absolute_error')
    mae_scores = -scores

    print(f"交叉验证平均绝对误差（MAE）：{mae_scores.mean():,.0f}（±{mae_scores.std():,.0f}")
    return mae_scores
```

## 完整的预测流程

```python
import joblib

def create_prediction_pipeline(model, feature_names, scaler=None):
    """创建可重用的预测流程"""

    def predict_cost(project_data):
        """为新项目预测成本"""

        # 输入数据
        project_data = dict()

        # 数据准备
        df = pd.DataFrame(project_data)

        # 特征处理
        if scaler:
            df = scaler.transform(df)

        # 进行预测
        prediction = model.predict(df)

        # 计算置信区间
        confidence = 0.15  # 15%的置信区间
        lower = prediction * (1 - confidence)
        upper = prediction * (1 + confidence)

        return {
            'predicted_cost': prediction,
            'lower_bound': lower,
            'upper_bound': upper,
            'confidence_level': f"{(1 - confidence) * 100:.0f}%"
        }

    return predict_cost

# 使用示例
predictor = create_prediction_pipeline(rf_model, X.columns.tolist())

# 新项目数据
new_project = {
    'area_m2': 5000,
    'floors': 8,
    'complexity_score': 3,
}

# 进行预测
result = predictor(new_project)
print(f"预测成本：{result['predicted_cost】:,.0f}")
print(f"置信区间：{result['lower_bound】:,.0f} - {result['upper_bound】:,.0f}")
```

## 模型的保存与加载

```python
import joblib

# 保存模型
def save_model(model, filepath):
    """将训练好的模型保存到文件"""
    joblib.dump(model, filepath)
    print(f"模型保存至：{filepath}")

# 加载模型
def load_model(filepath):
    """从文件加载模型"""
    model = joblib.load(filepath)
    print(f"模型加载成功：{filepath}")

# 示例使用
save_model(rf_model, "cost_prediction_model.pkl")
loaded_model = load_model("cost_prediction_model.pkl")
```

## 与ChatGPT结合使用

```python
# 向ChatGPT提问：
prompt = """
我有一些历史建筑项目数据，包含以下列：
- area_m2：建筑面积（平方米）
- floors：楼层数
- building_type：住宅、商业或工业
- total_cost：项目总成本（美元）

请使用scikit-learn编写Python代码来完成以下任务：
1. 准备数据以供机器学习使用
2. 训练一个随机森林模型
3. 评估模型
4. 预测一个3000平方米、5层楼的商业建筑的 cost"""
```

## 快速参考

| 任务                | 代码示例                                      |
|------------------|-------------------------------------------|
| 数据分割            | `train_test_split(X, y, test_size=0.2)`                   |
| 线性回归            | `LinearRegression().fit(X, y)`                        |
| K近邻              | `KNeighborsRegressor(n_neighbors=5)`                        |
| 随机森林            | `RandomForestRegressor(n_estimators=100)`                    |
| 预测                | `model.predict(X_new)`                            |
| 平均绝对误差（MAE）        | `mean_absolute_error(y_true, y_pred)`                |
| R²得分            | `r2_score(y_true, y_pred)`                        |
| 交叉验证            | `cross_val_score(model, X, y, cv=5)`                    |
| 保存模型            | `joblib.dump(model, 'file.pkl')`                        |

## 最佳实践

1. **数据质量**：历史数据越丰富，预测效果越好。
2. **特征选择**：确保包含相关的项目特征。
3. **通货膨胀调整**：将成本数据调整为当前价格水平。
4. **定期重新训练**：使用新的完成项目数据更新模型。
5. **集成学习**：结合多个模型以提高预测的准确性。
6. **提供置信区间**：始终给出预测的置信范围。

## 资源推荐

- 书籍：《数据驱动的建筑》（Artem Boiko著，第4.5章）
- 网站：https://datadrivenconstruction.io
- scikit-learn官方文档：https://scikit-learn.org

## 下一步

- 可以参考`duration-prediction`模块进行项目工期预测。
- 可以使用`ml-model-builder`构建自定义的机器学习工作流程。
- 可以使用`kpi-dashboard`进行数据可视化。
- 可以学习`big-data-analysis`模块处理大型数据集。