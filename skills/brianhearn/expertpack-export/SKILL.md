---
name: expertpack-export
description: 将 OpenClaw 实例中积累的知识导出为结构化的 ExpertPack 综合文件。该功能可用于备份代理的身份信息、进行迁移操作或创建可移植的知识快照。它支持自动发现（扫描工作区状态以识别所需的组件包）、数据压缩（将原始数据格式转换为符合 EP 标准的结构化文件）以及打包过程（生成符合 EP 标准的文件包及相应的元数据文件）。**请注意：**该功能不适用于从现有的 ExpertPack 文件中导入或恢复数据。
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
---
# ExpertPack 导出

[ExpertPack](https://expertpack.ai) 框架的一部分——一种用于 AI 代理的结构化、可移植的知识格式。

将 OpenClaw 实例导出为一个复合的 ExpertPack——该包包含代理（agent）以及作为知识组成部分的人员/产品/流程（person/product/process）包。

**了解更多信息：** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack) · [架构文档](https://expertpack.ai/#schemas)

## 先决条件

- 阅读 `references/schemas-summary.md`，了解此导出必须遵循的 EP 架构规则。
- 导出操作会将数据写入目标目录（默认为：`{workspace}/export/`）。该操作不会修改代理的实时工作区文件。

## 导出流程

### 1. 扫描

运行 `scripts/scan.py` 以列出工作区中的文件。该脚本会输出一个 JSON 清单，其中包含发现的文件、它们的类别以及建议的打包方式。

```bash
python3 {skill_dir}/scripts/scan.py --workspace /root/.openclaw/workspace --output /tmp/ep-scan.json
```

查看扫描结果。结果会显示：
- 哪些文件对应于哪种类型的包（代理、人员、产品、流程）
- 检测到了哪些知识领域
- 对于模糊分类的文件，会给出置信度评分

### 2. 提出建议

向用户展示建议的打包方案：
- 列出每个建议的包，包括其类型、名称以及主要的知识来源
- 标出需要用户决定的模糊分类情况
- 注意任何缺失的部分（例如：“未检测到流程包——是跳过这些包还是创建空包？”

在继续之前，请等待用户的确认。

### 3. 提取知识

对每个建议的包运行 `scripts/distill.py` 脚本。该脚本会读取源文件，提取知识内容，消除重复项，并生成符合 EP 标准的输出文件。

```bash
python3 {skill_dir}/scripts/distill.py \
  --scan /tmp/ep-scan.json \
  --pack agent:easybot \
  --output /root/.openclaw/workspace/export/packs/easybot/
```

对每个包重复此步骤。脚本会：
- 读取扫描清单中列出的源文件
- 提取并分类知识内容
- 消除重复项（优先保留最新的数据）
- 生成带有正确头部和前言的结构化 `.md` 文件
- 为每个包生成 `manifest.yaml` 文件
- 自动删除敏感信息（如 API 密钥、令牌、密码）

### 4. 组合打包

运行 `scripts/compose.py` 以生成最终的打包清单和概览。

```bash
python3 {skill_dir}/scripts/compose.py \
  --scan /tmp/ep-scan.json \
  --export-dir /root/.openclaw/workspace/export/
```

### 5. 验证

运行 `scripts/validate.py` 以检查导出内容是否符合架构规则。

```bash
python3 {skill_dir}/scripts/validate.py --export-dir /root/.openclaw/workspace/export/
```

验证内容包括：
- 是否所有必需的文件都存在
- `manifest.yaml` 文件中的字段是否有效
- 是否没有敏感信息被泄露（会扫描 API 密钥等敏感信息）
- 文件大小是否在规定的范围内
- 引用关系是否正确

### 6. 审查与发布

向用户展示验证报告以及导出内容的概要。用户可以决定是否提交/推送导出结果或进行必要的调整。

## 重要规则

- **切勿包含敏感信息。** 扫描和提取知识的脚本会自动删除敏感信息，但仍需手动检查 `operational/tools.md` 和 `operational/infrastructure.md` 文件。
- **提取知识，而非简单复制。** 原始的日志记录和会话状态应被压缩成结构化的知识数据。导出后的文件体积应仅为原始数据的 10-20%。
- **尊重用户隐私。** 对涉及用户个人信息的部分需进行特别处理，确保其访问权限得到控制。默认情况下，用户特定的内容应设置为 `private` 访问权限。
- **保留信息来源。** 每个提取的知识文件都应在前言中注明其来源文件。
- **不要修改实时工作区。** 所有导出文件都应保存在导出目录中。