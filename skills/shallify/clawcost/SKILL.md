---
name: clawcost
description: 跟踪 OpenClaw 代理的成本，每日/每周检查支出情况，并对支出进行详细分析（即进行成本建模）。
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins:
        - python3
---

# ClawCost

运行以下命令：
```bash
python3 {baseDir}/scripts/clawcost.py --budget 10
```

## 输出结果
输出为 JSON 格式的数据，包含以下内容：
- `balance`: 总余额（初始余额、已花费金额、剩余余额）或 `null`
- `today`: 当天的费用、预算占比、实际花费百分比
- `week`: 本周的总费用
- `total`: 终身费用（累计花费的代币数量）
- `models`: 费用明细（按模型分类）
- `models_today`: 仅显示当天的费用明细
- `daily`: 过去 7 天内的每日费用

## 设置初始余额
用户可以通过以下命令设置初始余额：
```bash
python3 {baseDir}/scripts/clawcost.py --set-balance 50.00
```
剩余余额会自动计算：初始余额 - 已花费总额

## 呈现方式
**语气：** 友好的，像是一位帮助用户查看开支的助手。请适量使用表情符号。

**格式：** 使用树状结构（`├ └`）来清晰地展示信息：
```
💰 clawleaks
├ Balance $42.98 / $50 remaining
├ Today   $1.36 / $10 (14%) ✅
├ Week    $7.02
└ Total   $7.02 (15.5M tok)

📈 Sonnet $3.99 (57%) • Haiku $2.06 (29%) • Opus $0.97 (14%)
```

**规则：**
- 如果某个模型的费用为 0 美元，则不显示该模型。

**提示信息：**
- 如果 `today.pct` 大于 80%：显示警告信息：**“警告：当日预算已使用 {pct}%！”**
- 如果 `today.pct` 大于 100%：显示严重警告：**“超出预算！已花费 ${cost} 美元！”**
- 如果 `balance_remaining` 小于 5 美元：显示提示信息：“余额过低：剩余 ${remaining} 美元”
- 如果 `balance` 为 `null`：建议用户使用 `--set-balance` 命令设置初始余额
- 如果预算使用正常：以 `✅` 标志表示预算已使用完毕

**使用场景：**
- 如有简单疑问：提供简短回答
- 如需详细信息：展示完整的费用明细及每日费用情况
- 如果超出预算：首先显示警告信息，并建议用户切换到 Haiku 服务

---

（注：由于文件中包含一些特定命令（如 `__CODE_BLOCK_0__`、`__CODE_BLOCK_1__` 等），这些部分在翻译时保持原样，因为它们是代码示例或特定功能的标识。在实际应用中，这些命令需要根据实际情况进行替换。）