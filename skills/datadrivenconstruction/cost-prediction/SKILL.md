---
slug: "cost-prediction"
display_name: "Cost Prediction"
description: "**使用机器学习预测建筑工程成本**  
基于历史项目数据，分别使用线性回归（Linear Regression）、K-近邻（K-Nearest Neighbors）和随机森林（Random Forest）模型来预测建筑工程的成本。完成模型的训练、评估及部署工作。"
---

# 使用机器学习进行建筑成本预测

## 概述

基于DDC方法论（第4.5章），本技能能够利用历史数据和机器学习算法来预测建筑项目的成本。该方法将传统的专家评估方式转变为数据驱动的预测方式。

**参考书籍**：《未来：预测与机器学习》（"Будущее: Прогнозы и машинное обучение"）

> “基于历史数据的预测使企业能够更准确地判断项目的成本和工期。”
— DDC书籍，第4.5章

## 核心概念

```
Historical Data → Feature Engineering → ML Model → Cost Prediction
    │                    │                │              │
    ▼                    ▼                ▼              ▼
Past projects      Prepare data      Train model    New project
with costs         for ML            on history     cost forecast
```

## 快速入门

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Load historical project data
df = pd.read_csv("historical_projects.csv")

# Features and target
X = df[['area_m2', 'floors', 'complexity_score']]
y = df['total_cost']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)
print(f"R² Score: {r2_score(y_test, predictions):.2f}")
print(f"MAE: ${mean_absolute_error(y_test, predictions):,.0f}")

# Predict new project
new_project = [[5000, 10, 3]]  # area, floors, complexity
cost = model.predict(new_project)
print(f"Predicted cost: ${cost[0]:,.0f}")
```

## 数据准备

### 准备历史数据集

```python
import pandas as pd
import numpy as np

def prepare_cost_dataset(df):
    """Prepare historical project data for ML"""
    # Select relevant features
    features = [
        'area_m2',
        'floors',
        'building_type',
        'location',
        'year_completed',
        'complexity_score',
        'material_quality',
        'total_cost'
    ]

    df = df[features].copy()

    # Handle missing values
    df = df.dropna(subset=['total_cost'])
    df['complexity_score'] = df['complexity_score'].fillna(df['complexity_score'].median())

    # Encode categorical variables
    df = pd.get_dummies(df, columns=['building_type', 'location'])

    # Calculate derived features
    df['cost_per_m2'] = df['total_cost'] / df['area_m2']
    df['cost_per_floor'] = df['total_cost'] / df['floors']

    # Adjust for inflation (to current year prices)
    current_year = 2024
    inflation_rate = 0.03  # 3% annual
    df['years_ago'] = current_year - df['year_completed']
    df['adjusted_cost'] = df['total_cost'] * (1 + inflation_rate) ** df['years_ago']

    return df

# Usage
df = pd.read_csv("projects_history.csv")
df_prepared = prepare_cost_dataset(df)
```

### 特征工程

```python
def engineer_features(df):
    """Create additional features for better predictions"""
    # Interaction features
    df['area_x_floors'] = df['area_m2'] * df['floors']
    df['area_x_complexity'] = df['area_m2'] * df['complexity_score']

    # Polynomial features
    df['area_squared'] = df['area_m2'] ** 2

    # Log transforms (for skewed features)
    df['log_area'] = np.log1p(df['area_m2'])

    # Binned features
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
    """Train Linear Regression model with scaling"""
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ])

    pipeline.fit(X_train, y_train)

    # Feature importance (coefficients)
    coefficients = pd.DataFrame({
        'feature': X_train.columns,
        'coefficient': pipeline.named_steps['regressor'].coef_
    }).sort_values('coefficient', key=abs, ascending=False)

    return pipeline, coefficients

# Usage
model, importance = train_linear_model(X_train, y_train)
print("Feature Importance:")
print(importance)
```

### K近邻（KNN）

```python
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def train_knn_model(X_train, y_train):
    """Train KNN model with optimal k"""
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    # Find optimal k using cross-validation
    param_grid = {'n_neighbors': range(3, 20)}
    knn = KNeighborsRegressor()
    grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_absolute_error')
    grid_search.fit(X_scaled, y_train)

    print(f"Best k: {grid_search.best_params_['n_neighbors']}")
    print(f"Best MAE: ${-grid_search.best_score_:,.0f}")

    return grid_search.best_estimator_, scaler

# Usage
knn_model, scaler = train_knn_model(X_train, y_train)
```

### 随机森林

```python
from sklearn.ensemble import RandomForestRegressor

def train_random_forest(X_train, y_train):
    """Train Random Forest model"""
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )

    rf.fit(X_train, y_train)

    # Feature importance
    importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)

    return rf, importance

# Usage
rf_model, importance = train_random_forest(X_train, y_train)
print("Feature Importance:")
print(importance.head(10))
```

### 梯度提升

```python
from sklearn.ensemble import GradientBoostingRegressor

def train_gradient_boosting(X_train, y_train):
    """Train Gradient Boosting model"""
    gb = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    gb.fit(X_train, y_train)
    return gb

# Usage
gb_model = train_gradient_boosting(X_train, y_train)
```

## 模型评估

### 综合评估

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def evaluate_model(model, X_test, y_test, model_name="Model"):
    """Comprehensive model evaluation"""
    predictions = model.predict(X_test)

    metrics = {
        'MAE': mean_absolute_error(y_test, predictions),
        'RMSE': np.sqrt(mean_squared_error(y_test, predictions)),
        'R²': r2_score(y_test, predictions),
        'MAPE': np.mean(np.abs((y_test - predictions) / y_test)) * 100
    }

    print(f"\n{model_name} Evaluation:")
    print(f"  MAE:  ${metrics['MAE']:,.0f}")
    print(f"  RMSE: ${metrics['RMSE']:,.0f}")
    print(f"  R²:   {metrics['R²']:.3f}")
    print(f"  MAPE: {metrics['MAPE']:.1f}%")

    return metrics, predictions

# Usage
metrics, predictions = evaluate_model(model, X_test, y_test, "Linear Regression")
```

### 比较多个模型

```python
def compare_models(models, X_test, y_test):
    """Compare multiple models"""
    results = []

    for name, model in models.items():
        metrics, _ = evaluate_model(model, X_test, y_test, name)
        metrics['Model'] = name
        results.append(metrics)

    comparison = pd.DataFrame(results)
    comparison = comparison.set_index('Model')

    print("\nModel Comparison:")
    print(comparison.round(2))

    return comparison

# Usage
models = {
    'Linear Regression': linear_model,
    'KNN': knn_model,
    'Random Forest': rf_model,
    'Gradient Boosting': gb_model
}
comparison = compare_models(models, X_test, y_test)
```

### 交叉验证

```python
from sklearn.model_selection import cross_val_score

def cross_validate_model(model, X, y, cv=5):
    """Perform cross-validation"""
    scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_absolute_error')
    mae_scores = -scores

    print(f"Cross-Validation MAE: ${mae_scores.mean():,.0f} (+/- ${mae_scores.std():,.0f})")
    return mae_scores

# Usage
cv_scores = cross_validate_model(rf_model, X, y)
```

## 预测流程

### 完整的预测函数

```python
import joblib

def create_prediction_pipeline(model, feature_names, scaler=None):
    """Create a reusable prediction pipeline"""

    def predict_cost(project_data):
        """
        Predict cost for new project

        Args:
            project_data: dict with project features

        Returns:
            Predicted cost and confidence interval
        """
        # Create DataFrame from input
        df = pd.DataFrame([project_data])

        # Ensure all required features
        for col in feature_names:
            if col not in df.columns:
                df[col] = 0

        df = df[feature_names]

        # Scale if necessary
        if scaler:
            df = scaler.transform(df)

        # Predict
        prediction = model.predict(df)[0]

        # Confidence interval (simple estimation)
        confidence = 0.15  # 15% margin
        lower = prediction * (1 - confidence)
        upper = prediction * (1 + confidence)

        return {
            'predicted_cost': prediction,
            'lower_bound': lower,
            'upper_bound': upper,
            'confidence_level': f"{(1-confidence)*100:.0f}%"
        }

    return predict_cost

# Usage
predictor = create_prediction_pipeline(rf_model, X.columns.tolist())

# Predict new project
new_project = {
    'area_m2': 5000,
    'floors': 8,
    'complexity_score': 3,
    'material_quality': 2
}

result = predictor(new_project)
print(f"Predicted Cost: ${result['predicted_cost']:,.0f}")
print(f"Range: ${result['lower_bound']:,.0f} - ${result['upper_bound']:,.0f}")
```

### 保存和加载模型

```python
import joblib

# Save model
def save_model(model, filepath):
    """Save trained model to file"""
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")

# Load model
def load_model(filepath):
    """Load model from file"""
    model = joblib.load(filepath)
    print(f"Model loaded from {filepath}")
    return model

# Usage
save_model(rf_model, "cost_prediction_model.pkl")
loaded_model = load_model("cost_prediction_model.pkl")
```

## 与ChatGPT结合使用

```python
# Prompt for ChatGPT to help with cost prediction

prompt = """
I have historical construction project data with these columns:
- area_m2: Building area in square meters
- floors: Number of floors
- building_type: residential, commercial, industrial
- total_cost: Total project cost in USD

Write Python code using scikit-learn to:
1. Prepare the data for machine learning
2. Train a Random Forest model
3. Evaluate the model
4. Predict cost for a new 3000 m² commercial building with 5 floors
"""
```

## 快速参考

| 任务 | 代码 |
|------|------|
| 分割数据 | `train_test_split(X, y, test_size=0.2)` |
| 线性回归 | `LinearRegression().fit(X, y)` |
| KNN | `KNeighborsRegressor(n_neighbors=5)` |
| 随机森林 | `RandomForestRegressor(n_estimators=100)` |
| 预测 | `model.predict(X_new)` |
| 均方绝对误差（MAE） | `mean_absolute_error(y_true, y_pred)` |
| R²分数 | `r2_score(y_true, y_pred)` |
| 交叉验证 | `cross_val_score(model, X, y, cv=5)` |
| 保存模型 | `joblib.dump(model, 'file.pkl')` |

## 最佳实践

1. **数据质量**：历史数据越多，预测越准确。
2. **特征选择**：包含相关的项目特征。
3. **通货膨胀调整**：将成本转换为当前价格。
4. **定期重新训练**：用新的已完成项目更新模型。
5. **集成方法**：结合多个模型以提高模型的稳健性。
6. **置信区间**：始终提供预测范围。

## 资源

- **书籍**：Artem Boiko所著的《数据驱动的建筑》（"Data-Driven Construction"），第4.5章
- **网站**：https://datadrivenconstruction.io
- **scikit-learn**：https://scikit-learn.org

## 下一步

- 查看`duration-prediction`以进行项目工期预测。
- 查看`ml-model-builder`以构建自定义的机器学习工作流程。
- 查看`kpi-dashboard`以进行数据可视化。
- 查看`big-data-analysis`以处理大型数据集。