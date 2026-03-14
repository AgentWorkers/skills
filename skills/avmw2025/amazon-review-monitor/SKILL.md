# Amazon Review Monitor — 跟踪、分析、回复负面评论

**再也不用错过任何负面评论了。系统提供AI生成的回复模板。**

## 产品描述
该工具可监控任意ASIN（Amazon产品代码）的评论信息，包括评分分布、情感分析、负面评论主题的识别，以及专业卖家回复的生成。用户可设置新负面评论的提醒功能。

## 使用场景
- 需要监控亚马逊产品评论的用户
- 收到负面评论并需要回复的用户
- 希望对产品评论进行情感分析的用户
- 关注评论趋势或客户反馈的用户

## 使用方法
```bash
# Analyze reviews for an ASIN
cd <skill_dir>/scripts && python3 monitor.py B0XXXXXXXXX

# Analyze 5 pages of reviews on UK marketplace
cd <skill_dir>/scripts && python3 monitor.py B0XXXXXXXXX co.uk 5
```

## 功能介绍
- 收集最新的评论数据（支持配置数据深度）
- 以可视化图表形式展示评分分布（5星到1星）
- 计算平均评分
- 进行情感分析（识别正面/负面评论）
- 确定主要的正面和负面评论主题
- 突出显示需要回复的负面评论
- 根据评论类型自动生成专业卖家回复模板

## 回复模板涵盖的内容
- 产品新鲜度/质量问题
- 运输过程中的损坏
- 发货商品与预期不符
- 一般性不满

## 无需依赖任何外部组件
完全基于Python 3开发，无需API密钥，也无需安装额外的软件包（如pip）。