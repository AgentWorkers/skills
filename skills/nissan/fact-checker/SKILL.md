---
name: fact-checker
version: 1.0.2
description: 在发布内容之前，通过网络搜索和引用来源资料来验证其中的事实陈述的准确性。
metadata:
  {
      "openclaw": {
            "emoji": "\u2705",
            "requires": {
                  "bins": [
                        "python3"
                  ],
                  "env": []
            },
            "primaryEnv": null,
            "network": {
                  "outbound": true,
                  "reason": "Searches the web to verify factual claims. Uses Tavily or web_search."
            }
      }
}
---

# Fact-Checker：验证Markdown中的声明与源数据的一致性

该工具能够从Markdown草稿文件中提取所有可验证的声明（包括数字、日期、模型名称、分数以及因果关系陈述），并将这些声明与现有的源数据进行比对，生成一份验证报告。

## 使用方法

```bash
python3 skills/fact-checker/scripts/fact_check.py <draft.md>
python3 skills/fact-checker/scripts/fact_check.py <draft.md> --output report.md
```

## 检查内容

### 提取的声明类型：
- **数值声明**：带有上下文的整数和浮点数
- **模型引用**：`model/task`（例如 `phi4/classify`）和 `model:tag`（例如 `phi4:latest`）
- **日期**：`YYYY-MM-DD` 格式
- **分数值**：如 `0.923`、`1.000` 等十进制分数
- **百分比**：如 `42%`、`95.3%` 等

### 查阅的源数据（按优先级排序）：
1. `projects/hybrid-control-plane/FINDINGS.md` — 主要事实来源
2. `http://localhost:8765/status` 上的控制平面 `/status` API — 实时的评分运行数据
3. `projects/hybrid-control-plane/data/scores/*.json` — 磁盘上的原始评分运行文件
4. `memory/*.md` — 包含时间戳和决策的每日日志
5. `projects/hybrid-control-plane/` 目录下的 `git log` — 提交哈希、日期和作者信息
6. `projects/hybrid-control-plane/CHANGELOG.md` — 施工日志

## 输出格式

每个声明会生成一行记录，之后会显示已确认、无法验证或与源数据矛盾的声明数量统计。

## 适用场景

当需要对博客文章、报告或文档文件进行事实核查时，运行该工具并向用户展示验证结果。如果发现任何与源数据矛盾的声明，请将其突出显示并建议进行修正。

## 对代理（Agent）的说明：
1. 使用脚本并传入草稿文件的路径。
2. 解析生成的验证报告。
3. 总结关键发现，特别是那些与源数据矛盾的声明。
4. 根据证据提供具体的修正建议。
5. 如果 `/status` API 不可用，请记录这一情况，并依赖 `FINDINGS.md` 和评分文件进行验证。