# 经济失业监测工具

该工具用于监测失业率、劳动力参与率以及就业数据，以评估劳动力市场的健康状况。

## 主要功能

- **失业率**：当前及历史数据
- **劳动力参与率**：劳动力人口所占的百分比
- **非农就业报告（NFP）**：跟踪每月的就业增减情况

## 价格

- **费用**：每次API调用0.001美元
- **支付方式**：通过SkillPay.me进行集成支付

## 使用场景

- 评估劳动力市场状况
- 预测经济周期
- 为政策制定和招聘策略提供参考

## 示例输入

```json
{
  "country": "Germany"
}
```

## 示例输出

```json
{
  "success": true,
  "country": "Germany",
  "unemployment_rate": "3.2%",
  "labor_participation": "60.5%",
  "message": "Unemployment data fetched for Germany."
}
```

## 集成方式

该工具与SkillPay.me集成，支持自动微支付。每次API调用的费用为0.001美元。