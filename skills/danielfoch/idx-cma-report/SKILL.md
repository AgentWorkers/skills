---
name: idx-cma-report
description: 根据IDX房源列表数据以及选定的可比房源，生成市场对比分析报告（CMA，Comparative Market Analysis）和房屋估值报告。这些报告可用于用户挑选可比房源、估算房屋的市场价值范围、为卖家提供房屋评估报告，或通过Google Gemini Canvas或Google AI Studio平台发布交互式的市场对比分析内容。
---
# IDX CMA 报告

使用此技能将主题房产数据及 IDX 对比房源转化为一份规范的 CMA 报告，内容包括：

- 结构化的估值计算结果
- 供代理人/客户查阅的书面报告
- 适用于 Google Gemini Canvas 或 Google AI Studio 的交互式使用提示

## 工作流程

### 1. 通过 IDX MCP/CLI 收集数据
使用环境中已有的 IDX MCP/CLI 工具收集以下数据：
- 主题房产的详细信息
- 根据用户需求筛选出的候选对比房源（已售出/待售/在售状态）

如果用户对房源选择不明确，可询问具体需要包含哪些对比房源。默认保留 3 至 8 个对比房源，除非用户另有要求。

使用 `references/cma-input-schema.md` 中定义的格式将数据转换为 JSON 格式。

### 2. 生成 CMA 报告输出
运行以下脚本：
```bash
python3 scripts/build_cma.py \
  --subject subject.json \
  --comps comps.json \
  --output-dir cma-output
```

该脚本会生成以下文件：
- `cma-output/cma_report.md`（总结报告）
- `cma-output/cma_data.json`（估值计算数据）
- `cma-output/interactive_local.html`（本地交互式查看页面）
- `cma-output/gemini_canvas.prompt.md`（适用于 Google 工具的交互式提示文件）

### 3. 审查并解释调整内容
在最终交付之前，请执行以下操作：
- 展示所使用的对比房源列表
- 显示预估的房价范围及中心估价
- 用通俗易懂的语言解释各项估值假设及主要调整因素
- 标记缺失或质量较低的字段（这些字段可能会影响估值的准确性）

请参考 `references/valuation-guidelines.md` 以获取调整规则和信心评估的指导。

### 4. 在 Gemini 中发布交互式版本
使用 `cma-output/gemini.canvas.prompt.md` 作为基础提示文件，然后按照以下步骤操作：
1. 打开 [Google AI Studio](https://aistudio.google.com/) 或 Gemini Canvas。
2. 粘贴生成的提示文件，并提供 `cma_data.json` 数据文件。
3. 请求生成一个交互式的 CMA 网页应用，该应用应具备以下功能：
   - 可排序/筛选的对比房源列表
   - 包含经坐标（纬度/经度）处理后的数据字段
   - 价格范围可视化功能
   - 用于解释各项调整的备注面板
4. 如所选 Google 工具支持，可申请托管或分享最终报告结果。

详细操作步骤请参阅 `references/gemini-canvas-publish.md`。

## 安全注意事项
- 将生成的报告视为经纪人的辅助工具，而非正式的评估报告。
- 在展示估值结果前，务必指出数据中的空白、异常值或过时的房源信息。
- 绝不要虚构房源属性；对于缺失的数据，应标记为“未知”。
- 清晰区分房源的实际数据与模型中的假设参数。

## 参考资料
- `references/cma-input-schema.md`
- `references/valuation-guidelines.md`
- `references/gemini-canvas-publish.md`