---
name: expertpack-export
description: 将 OpenClaw 实例中积累的知识导出为结构化的 ExpertPack 综合文件。该功能可用于备份代理的身份信息、进行迁移操作或创建可移植的知识快照。它支持自动发现（扫描工作区状态以识别所需的组件包）、数据压缩（将原始数据格式转换为结构化的 EP 文件）以及文件打包（生成符合 EP 标准的包及相应的元数据文件）。**请注意：** 该功能不适用于从现有的 ExpertPack 文件中导入或恢复数据。
---
# ExpertPack 导出

将 OpenClaw 实例导出为一个复合的 ExpertPack——该包包含一个代理（agent）以及用于表示知识的“人员/产品/流程”（person/product/process）包。

## 先决条件

- 请阅读 `references/schemas-summary.md`，以了解此导出操作必须遵循的 EP 架构规则。
- 导出操作会将文件写入目标目录（默认为 `{workspace}/export/`），但不会修改代理的实时工作区文件。

## 导出流程

### 1. 扫描

运行 `scripts/scan.py` 以统计工作区中的文件。该脚本会输出一个 JSON 列表，其中包含发现的文件、它们的类别以及建议的打包方式。

```bash
python3 {skill_dir}/scripts/scan.py --workspace /root/.openclaw/workspace --output /tmp/ep-scan.json
```

查看扫描结果：
- 哪些文件应归类为哪种类型的包（代理、人员、产品、流程）
- 检测到了哪些知识领域
- 对于存在歧义的分类，会显示相应的置信度分数

### 2. 提出打包方案

向用户展示建议的打包方案：
- 列出每个建议的包的类型、名称以及主要的内容来源
- 标出存在歧义的分类，供用户决定如何处理
- 注意任何缺失的部分（例如：“未检测到流程包——是跳过这些包还是创建空包？”）

在用户确认之前，请勿继续下一步操作。

### 3. 提取知识内容

针对每个建议的包，运行 `scripts/distill.py`。该脚本会读取源文件，提取其中的知识内容，去除重复项，并生成符合 EP 标准的输出文件。

```bash
python3 {skill_dir}/scripts/distill.py \
  --scan /tmp/ep-scan.json \
  --pack agent:easybot \
  --output /root/.openclaw/workspace/export/packs/easybot/
```

对每个包重复此步骤。脚本会：
- 读取扫描结果中列出的源文件
- 提取并分类文件中的知识内容
- 去除重复项（优先保留最新的数据）
- 生成结构化的 `.md` 文件，并添加适当的头部和前言部分
- 为每个包生成 `manifest.yaml` 文件
- 自动删除文件中的敏感信息（如 API 密钥、令牌、密码）

### 4. 组合所有包

运行 `scripts/compose.py` 以生成最终的复合包清单和概览。

```bash
python3 {skill_dir}/scripts/compose.py \
  --scan /tmp/ep-scan.json \
  --export-dir /root/.openclaw/workspace/export/
```

### 5. 验证

运行 `scripts/validate.py` 以检查导出结果是否符合 EP 架构规则。

```bash
python3 {skill_dir}/scripts/validate.py --export-dir /root/.openclaw/workspace/export/
```

验证内容包括：
- 是否所有必需的文件都存在
- `manifest.yaml` 文件中的字段是否有效
- 是否没有敏感信息被泄露（会扫描文件中是否包含 API 密钥等敏感内容）
- 文件大小是否在规定的范围内
- 文件之间的引用关系是否正确

### 6. 审查并发布

向用户展示验证报告以及导出内容的概要。用户可以决定是提交导出结果、推送文件，还是对结果进行修改。

## 重要规则

- **严禁包含敏感信息。** 扫描和提取知识的脚本会自动删除文件中的敏感信息，但仍需手动检查 `operational/tools.md` 和 `operational/infrastructure.md` 文件。
- **仅提取知识内容，不要直接复制原始文件。** 原始的日志记录和会话状态应被压缩成结构化的知识数据。导出文件的体积应为原始文件体积的 10%–20%。
- **尊重用户隐私。** 对涉及用户个人信息的文件，需设置访问权限为“私有”。
- **保留文件的来源信息。** 每个提取出的知识文件都应在前言部分注明其来源文件。
- **不要修改实时工作区文件。** 所有导出的文件都应保存在导出目录中。