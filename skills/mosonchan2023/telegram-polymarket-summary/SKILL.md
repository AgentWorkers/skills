# Telegram Polymarket 摘要

该功能会将 Polymarket 上热门且交易量较大的预测市场汇总信息直接发送到您的 Telegram 聊天窗口。

## 主要特点

- **每日/每周总结**：获取最重要的市场动态概览
- **热门市场**：识别交易最活跃的市场
- **自定义关注领域**：按类别（如政治、体育、加密货币）筛选汇总信息

## 价格

- **费用**：每次 API 调用费用为 0.001 美元
- **支付方式**：通过 SkillPay.me 进行集成支付

## 使用场景

- 及时了解选举趋势
- 监测体育博彩市场的情绪变化
- 关注加密货币市场的预测结果

## 示例输入

```json
{
  "telegram_chat_id": "123456789",
  "categories": ["Politics", "Crypto"]
}
```

## 示例输出

```json
{
  "success": true,
  "summary_sent": true,
  "message": "Polymarket summary for Politics and Crypto categories sent to Telegram."
}
```

## 集成方式

该功能已与 SkillPay.me 集成，支持自动微支付。每次 API 调用费用为 0.001 美元。