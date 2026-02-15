---
name: idea-lab
description: 创意构思与原型设计；自主创新与实验。
---

# Idea Lab

该工具能够自主生成、评估并制作创意想法的原型。

## 使用说明

1. **创意构思**：
   - 当需要提出想法时（或在进行主动头脑风暴时）：
     - 明确领域或约束条件（例如：“为自由职业者设计的低成本SaaS产品”）
     - 通过结构化的头脑风暴方法生成5-10个想法
     - 从可行性、市场需求、独特性和收入潜力三个方面对每个想法进行评分

2. **评估框架**：
   | 评估标准 | 权重 | 分数（1-10） |
   |---------|--------|-------------|
   | 市场需求 | 30% | 是否有人正在寻找这样的产品？ |
   | 可行性 | 25% | 我们能在1周内实现它吗？ |
   | 收入潜力 | 25% | 它每月能带来100美元以上的收入吗？ |
   | 独特性 | 20% | 这个想法有足够的差异化吗？ |

   **总分 = 各评估标准得分的加权总和。** 分数达到6.0分及以上时，值得进一步制作原型。

3. **开发前的研究**：
   ```
   For each promising idea:
   ├── Google Trends — search volume & trajectory
   ├── Reddit — are people asking for this?
   ├── Product Hunt — does it already exist?
   ├── GitHub — open source alternatives?
   └── X/Twitter — buzz or complaints in this space?
   ```

4. **快速制作原型**：
   - 制作一个简单的登录页面（1小时）——评估用户兴趣
   - 开发一个命令行工具（2-4小时）——验证概念的可行性
   - 如果验证通过，再开发一个MVP版本（Web应用程序，1-2天）

5. **将想法记录在`~/.openclaw/idea-lab/ideas.jsonl`文件中**：
   ```json
   {"id": "uuid", "title": "SEO Audit Lite", "domain": "SaaS", "score": 7.8, "status": "prototyping", "created": "ISO8601", "notes": "..."}
   ```

## 头脑风暴技巧

### SCAMPER方法
- **替代**（Substitute）：如果我们用Y替换X会怎样？
- **组合**（Combine）：如果我们把A和B结合起来会怎样？
- **适应**（Adapt）：行业X中成功的做法能否应用到这里？
- **改进**（Modify）：我们能否将其简化/扩展/加速10倍？
- **拓展用途**（Put to Other Uses）：还有谁可以使用这个想法？
- **剔除**（Eliminate）：如果我们去掉最复杂的部分会怎样？
- **反向思考**（Reverse）：如果我们反其道而行之会怎样？

### 基于约束条件的头脑风暴方法
```
Given:
- Budget: $0 (free tools only)
- Time: 1 weekend
- Skills: AI + web dev
- Target: English-speaking freelancers
→ What can we build?
```

## 自主开发规则

- **自由发挥**：
  - 研究并记录想法
  - 制作本地原型
  - 创建登录页面（无需部署）
  - 分析竞争对手
  - 对想法进行评分和排序

### 注意事项：
- 在正式部署之前，请先征求他人意见
- 不要直接将产品部署到生产环境中
- 不要花费资金购买域名或API
- 不要公开发布关于想法的详细信息
- 与潜在用户取得联系

## 安全性注意事项：
- **不要公开未经过验证的想法**——竞争对手可能会抄袭
- **保持财务预测的合理性**——避免过度夸大
- **在开发前进行充分验证**——避免浪费精力

## 必需条件：
- 支持网络搜索以方便研究
- 提供文件系统用于存储想法
- 可选功能：使用`web_fetch`工具进行竞争对手分析