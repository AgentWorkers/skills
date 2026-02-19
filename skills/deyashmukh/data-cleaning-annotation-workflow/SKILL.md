---
name: data-cleaning-annotation-workflow
description: "Kaggle 上的时间序列数据集（能源、制造业、气候领域）到 Data Annotation 平台（data.smlcrm.com）的完整工作流程：  
包括下载数据集、使用 pandas 进行数据清洗、上传包含元数据的原始数据文件、配置数据列（时间/目标变量/协变量/分组）、设置数据单位（千瓦时 kWh、千伏安时 kVarh、二氧化碳当量 tCO2、比率 ratio、秒 seconds），以及通过选择所有变量并应用相应的分组标签来完成数据分组。该流程适用于从 Kaggle 获取数据集、为机器学习模型进行数据清洗、上传带有元数据的数据文件、配置数据类型和单位、为所有变量分配分组，或使整个数据处理流程达到“CLEAN”状态。"
---
# 模拟数据标注工作流程

这是一个完整的端到端工作流程，用于在 Data Annotation 平台（data.smlcrm.com）上准备和处理时间序列数据集并进行标注。

## 该技能的作用

该技能详细说明了处理时间序列数据集（能源、制造业、气候领域）的整个工作流程，从数据查找阶段到数据被标记为“CLEAN”状态：

1. **查找数据集**：在 Kaggle 上搜索能源/制造业/气候领域的时间序列数据。
2. **下载数据**：通过浏览器或 Kaggle CLI 下载 CSV 文件。
3. **数据清洗**：运行 Python/pandas 脚本，处理缺失值、重复项和格式问题。
4. **上传原始数据**：上传包含元数据（名称、领域、来源 URL、描述）的 CSV 文件。
5. **配置列标题**：设置列的类型（时间、目标变量、协变量、分组）和单位。
6. **分配分组**：选择所有变量（目标变量和协变量），并为其分配相应的分组标签。
7. **上传清洗后的数据**：最终上传数据集，使其状态变为“CLEAN”。

## 支持的领域

- **能源**：电力消耗、公用事业、可再生能源、电网数据
- **制造业**：工业流程、钢铁生产、排放量、设备数据
- **气候**：二氧化碳排放量、环境监测、天气相关数据

## 快速入门

要从 Kaggle 下载数据集并进行标注，请参考以下代码示例：

```
1. Find dataset on Kaggle
2. Download (browser or kaggle CLI)
3. Clean with scripts/clean_dataset.py
4. Upload RAW dataset to data.smlcrm.com (with metadata)
5. Click "Clean" and upload cleaned file
6. Configure column metadata (types, units)
7. Assign groups to variables
8. Upload cleaned dataset → CLEAN status
```

## 工作流程步骤

### 第一步：查找并下载数据集

**通过浏览器在 Kaggle 上查找数据集：**
1. 访问 kaggle.com/datasets
2. 搜索相关数据集（例如：“steel industry energy consumption”、“manufacturing emissions”、“climate CO2”）
3. 查看数据描述、文件列表和数据预览
4. 点击“Download”按钮
5. 从下载的压缩文件中提取 CSV 文件

**另一种方法：使用 Kaggle CLI：**
```bash
# Install if needed: pip install kaggle
# Configure: kaggle competitions list

scripts/download_kaggle.sh <dataset-name> [output-dir]
# Example: scripts/download_kaggle.sh csafrit2/steel-industry-energy-consumption
```

### 第二步：清洗数据集

**在上传数据之前，请务必运行清洗脚本：**

```bash
python3 scripts/clean_dataset.py <input.csv> [-o <output.csv>]
```

**脚本的功能：**
- 去除列名中的空白字符
- 删除重复行
- 用中位数填充缺失的数值
- 用众数或“Unknown”填充缺失的分类值
- 将时间戳列转换为 datetime 格式
- 输出列的摘要信息以供元数据配置使用

**输出结果：**
- 清洗后的 CSV 文件，准备好上传
- 列的摘要信息打印到控制台（请保存这些信息以用于元数据配置）

### 第三步：将原始数据上传到平台

1. 访问 data.smlcrm.com/dashboard
2. 点击“Upload Dataset”按钮
3. 为原始数据集填写元数据：
   - **名称**：数据集的描述性名称
   - **领域**：能源、制造业、气候等
   - **来源 URL**：Kaggle 或数据的原始来源 URL
   - **描述**：数据集的简要概述
4. 上传未清洗的原始 CSV 文件
5. 点击“Upload”

**结果：**数据集会以“RAW”状态显示在列表中

### 第四步：上传清洗后的数据并配置元数据

1. 在列表中找到原始数据集
2. 点击“Clean”按钮
3. 上传第二步中清洗后的 CSV 文件
4. 为每一列配置标题：

| 设置 | 描述 |
|---------|-------------|
| **名称** | 列的名称（可编辑） |
| **单位** | 测量单位（kWh、°C、%、比率、tCO2 等） |
| **类型** | 时间/目标变量/协变量/分组 |

**列类型指南：**
- **时间**：时间戳/日期时间列（通常必需）
- **目标变量**：需要预测的变量（至少需要一个）
- **协变量**：输入特征/自变量
- **分组**：分类变量（如 WeekStatus、Day_of_week、Load_Type 等）

**批量配置：**
- 通过复选框选择多行
- 使用“Apply”下拉菜单为选中的列设置类型
- 单个或批量设置单位

**常见的单位示例：**
- 能源：kWh、MWh、MW
- 功率：kVarh、kW
- 排放量：tCO2、kgCO2
- 比率：比率、%
- 时间：秒、分钟、小时

### 第五步：为变量分配分组

**目的：**分组变量用于定义数据的分割方式，以便进行分析。

**具体步骤：**
1. 通过勾选复选框选择所有变量：
   - 目标变量
   - 所有协变量

2. 为选中的变量分配所有分组标签：
   - 点击第一个分组标签（例如 WeekStatus）→ 所有选中的变量都会被归入该组
   - 点击第二个分组标签（例如 Day_of_week）→ 所有选中的变量都会被归入该组
   - 依此类推，为所有可用的分组标签进行操作

**注意：**目标变量和所有协变量都必须分配分组。

### 第六步：最终上传

1. 点击“Upload Cleaned Dataset”按钮
2. 等待数据处理完成
3. 数据集的状态会从“RAW”变为“CLEAN”
4. 核对数据点数量是否正确

## 示例：钢铁行业能源数据集

**来源：** https://www.kaggle.com/datasets/csafrit2/steel-industry-energy-consumption

**元数据：**
- **名称：** 钢铁行业能源消耗（韩国）
- **领域：** 能源
- **数据点数量：** 350,400

**列配置：**
| 列 | 类型 | 单位 |
|--------|------|-------|
| Timestamps | 时间 | - |
| Usage_kWh | 目标变量 | kWh |
| Lagging_Current_Reactive.Power_kVarh | 协变量 | kVarh |
| Leading_Current_Reactive_Power_kVarh | 协变量 | kVarh |
| CO2(tCO2) | 协变量 | tCO2 |
| Lagging_Current_Power_Factor | 协变量 | 比率 |
| Leading_Current_Power_Factor | 协变量 | 比率 |
| NSM | 协变量 | 秒 |
| WeekStatus | 分组 | - |
| Day_of_week | 分组 | - |
| Load_Type | 分组 | - |

**分组分配：**
1. 选择：Usage_kWh、Lagging_Current_Reactive.Power_kVarh、Leading_Current_Reactive_Power_kVarh、CO2(tCO2)、Lagging_Current_Power_Factor、Leading_Current_Power_Factor、NSM
2. 点击：WeekStatus → 所有选中的变量都会被归入 WeekStatus 组
3. 点击：Day_of_week → 所有选中的变量都会被归入 Day_of_week 组
4. 点击：Load_Type → 所有选中的变量都会被归入 Load_Type 组
5. 最终结果：所有变量都会显示为 “WeekStatus × Day_of_week × Load_Type” 的组合

## 参考资料

有关平台配置的详细指南，请参阅 [references/platform_guide.md](references/platform_guide.md)。

## 故障排除

- 如果“Next”按钮不可用，请检查是否至少设置了一个时间列和一个目标列。
- 确保所有列都已分配了正确的类型。
- 如果分组没有显示，请确保列已被标记为“Group”类型，然后再进行下一步操作。
- 如果上传失败，请重新运行清洗脚本，检查 CSV 文件的格式（是否为逗号分隔），并确认没有空的列名。

## 脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/clean_dataset.py` | 清洗数据并准备上传 |
| `scripts/download_kaggle.sh` | 通过 Kaggle CLI 下载数据集 |

## 平台网址

Data Annotation 平台：https://data.smlcrm.com