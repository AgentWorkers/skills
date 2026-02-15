# 零售贸易周报生成器 - 技能文档

## 概述
该技能能够处理多个每周销售报告的 Excel 文件，生成一份综合的零售贸易周报，其中包含不同渠道（DRP、DXS、License Store）和产品类型（移动预付费/后付费、FWA 4G/5G）之间的周环比（WoW）数据。

## 目的
- 将 12 个 Excel 文件（当前周 6 个 + 上周 6 个）整合成一份全面的周报
- 按地区和渠道计算平均每日新增用户数（ADA）指标
- 计算周环比（WoW）绩效指标
- 生成包含图表和颜色编码绩效指标的格式化 Excel 输出文件

## 输入要求

### 必需文件（共 12 个）
**当前周（6 个文件）：**
1. `DRP_Channel_Sales_Report_DRP_M_DD-M_DD.xlsx`
2. `DRP_Special_SIM_Monitor_Report_Daily_TECNO_M_DD-M_DD.xlsx`
3. `License_Store_Performance_Monitor_Report_LS_M_DD-M_DD.xlsx`
4. `DXS_Acquisition_Report_Mobile_Prepaid_M_DD-M_DD.xlsx`
5. `DXS_Acquisition_Report_Mobile_Postpaid_M_DD-M_DD.xlsx`
6. `DXS_Acquisition_Report_FWA_M_DD-M_DD.xlsx`

**上周（6 个文件，日期较早）：**
文件类型相同，文件名中的日期范围较早

### 商店映射 CSV
包含商店名称到地区映射的文件，支持使用别名：
```csv
Store Name,Region,Aliases
SM Megamall,NCR,"Megamall|SM Mega|MEGAMALL"
...
```

## 数据处理逻辑

### 1. 文件识别
- 从文件名中提取日期范围（格式：`M_DD-M/DD`）
- 根据日期对比自动将文件分为当前周和上周
- 确保所有 12 个必需文件都存在

### 2. 数据提取规则

#### DRP 渠道销售报告
- **标题行：** 跳过第 0-7 行
- **数据行：** 从第 8 行开始
- **地区字段：** 第 0 列（AREA）
- **关键列：**
  - 第 1 列：MOBILE POSTPAID > TOTAL ACTIVATION
  - 第 5 列：MOBILE PREPAID > TOTAL ACTIVATION
  - 第 6 列：Double Data_Sum
  - 第 9 列：4G WiFi 980 SIM_Sum (FWA 4G)
  - 第 10 列：Unli 5G WIFI 100Mbps Starter SIM_Sum (FWA 5G)
  - 第 11 列：5G WiFi 4990 SIM_Sum (FWA 5G)

#### DRP TECNO 报告
- **标题行：** 跳过第 0-6 行
- **数据行：** 从第 7 行开始
- **地区字段：** 第 0 列（Activation Area）
- **关键列：**
  - 第 1 列：CARMON Activation (CAMON 40)
  - 第 2 列：POVA Activation (POVA 7)
  - 第 3 列：Total Activation (TECNO ADA = CAMON 40 + POVA 7)

#### License Store 报告
- **标题行：** 跳过第 0-7 行
- **数据行：** 从第 8 行开始
- **商店字段：** 第 0 列（商店名称） - **需要映射到地区**
- **关键列：**
  - 第 1 列：Mobile Prepaid
  - 第 3 列：Mobile Postpaid
  - 第 29 列（AD）：DITO Home Prepaid 4G WiFi 980 SIM (FWA 4G)
  - 需要查找：Unli 5G WIFI 100Mbps Starter SIM (FWA 5G)
  - 需要查找：5G WiFi 4990 SIM (FWA 5G)

#### DXS 移动预付费报告
- **标题行：** 跳过第 0-7 行
- **数据行：** 从第 8 行开始
- **商店字段：** 第 0 列（DXS 名称） - **需要映射到地区**
- **关键列：**
  - 第 4 列：Total

#### DXS 移动后付费报告
- **标题行：** 跳过第 0-7 行
- **数据行：** 从第 8 行开始
- **商店字段：** 第 0 列（DXS 名称） - **需要映射到地区**
- **关键列：**
  - 第 12 列：Total

#### DXS FWA 报告
- **标题行：** 跳过第 0-7 行
- **数据行：** 从第 8 行开始
- **商店字段：** 第 0 列（DXS 名称） - **需要映射到地区**
- **关键列：**
  - 第 1 列：DITO Home Prepaid 4G WiFi 980 (FWA 4G)
  - 第 18 列：Total
  - **FWA 5G 计算：** Total（第 18 列） - 4G（第 1 列）

### 3. 商店名称到地区映射
```python
# Build mapping dictionary from CSV
store_mapping = {}
for row in mapping_csv:
    main_name = row['Store Name']
    region = row['Region']
    aliases = row['Aliases'].split('|') if row['Aliases'] else []
    
    # Add main name and all aliases to mapping
    store_mapping[main_name.upper()] = region
    for alias in aliases:
        store_mapping[alias.strip().upper()] = region

# Apply fuzzy matching for unmatched stores
def map_store_to_region(store_name):
    # Exact match (case-insensitive)
    if store_name.upper() in store_mapping:
        return store_mapping[store_name.upper()]
    
    # Fuzzy match using substring search
    for key in store_mapping:
        if key in store_name.upper() or store_name.upper() in key:
            return store_mapping[key]
    
    # Default to "Others" if no match
    return "Others"
```

### 4. 地区汇总

**标准地区：** NCR、SLZ、NLZ、CLZ、EVIS、WVIS、MIN、其他

对于每种产品类型和地区：
```python
# DRP data: Direct mapping (already by region)
DRP_ADA = drp_data[region][product_column]

# DXS data: Aggregate stores by region
DXS_ADA = sum(dxs_data[store][product_column] 
              for store in dxs_data 
              if map_store_to_region(store) == region)

# LS data: Aggregate stores by region
LS_ADA = sum(ls_data[store][product_column] 
             for store in ls_data 
             if map_store_to_region(store) == region)

# Total for region
RT_Total_ADA = DRP_ADA + DXS_ADA + LS_ADA
```

### 5. 周环比（WoW）计算
```python
WoW = (current_week_value - previous_week_value) / previous_week_value

# Formatting rules:
# - Display as percentage (e.g., "21%", "-13%")
# - Round to nearest integer
# - Handle division by zero: display "-" if previous_week_value == 0
# - Handle cases where current = 0 and previous > 0: show "-100%"
```

### 6. 特殊计算

#### FWA 5G 组件
```python
# DRP FWA 5G
DRP_FWA_5G = Column_10 + Column_11

# DXS FWA 5G
DXS_FWA_5G = Total - Column_1_4G

# LS FWA 5G
LS_FWA_5G = Unli_5G_WIFI_100Mbps + WiFi_4990_SIM
```

#### TECNO ADA
```python
TECNO_ADA = CAMON_40 + POVA_7
```

## 输出格式

### Excel 结构
**单个工作表：“周报”**

**部分：**
1. 报告标题（第 1-2 行）
   - 标题：“零售贸易周报”
   - 日期范围：“上周：[日期] | 本周：[日期]”

2. 渠道汇总（第 4-9 行）
   - 列：渠道 | 项目名称 | 本周 ADA | 周环比（WoW） | 同比环比（MoM）
   - 行：DRP BAU、DRP TECNO、License Store、DXS、RT Total

3. 按地区划分的移动预付费（第 11-21 行）
   - 列：地区 | RT Total ADA | 周环比（WoW） | DXS ADA | 同比环比（WoW） | License Store ADA | 周环比（WoW） | DRP ADA | 周环比（WoW）
   - 行：8 个地区 + 总计

4. DRP 预付费项目（第 23-33 行）
   - 列：地区 | Double Data ADA | 周环比（WoW） | TECNO ADA | 周环比（WoW） | CAMON 40 | 周环比（WoW） | POVA 7 | 周环比（WoW）
   - 行：8 个地区 + 总计

5. 按地区划分的移动后付费（第 35-45 行）
   - 结构与移动预付费相同

6. 按地区划分的 FWA 4G（第 47-57 行）
   - 结构与移动预付费相同

7. 按地区划分的 FWA 5G（第 59-69 行）
   - 结构与移动预付费相同

### 格式规则

#### 数字格式
- ADA 值：使用千位分隔符的整数格式（例如：“1,876”）
- 周环比百分比：整数百分比（例如：“21%”，“-13%”）
- 较小的 ADA 值（< 10）：显示 1 位小数（例如：“0.6”，“2.9”）

#### 颜色编码
- **周环比为正（>0%）：** 绿色文本（#008000）
- **周环比为负（<0%）：** 红色文本（#FF0000）
- **周环比为 0%：** 黑色文本
- **周环比为 N/A（"-"）：** 灰色文本（#808080）

#### 单元格样式
- **标题：** 加粗，居中，浅灰色背景（#F0F0F0）
- **地区名称：** 加粗
- **总计行：** 加粗，浅蓝色背景（#E6F2FF）
- **边框：** 所有数据单元格周围有细边框

### 图表

**图表 1：渠道绩效对比**
- 类型：分组柱状图
- 数据：按渠道划分的本周 ADA（DRP BAU、DRP TECNO、License Store、DXS）
- 位置：位于渠道汇总部分的右侧
- 大小：宽 6 列 x 高 15 行

**图表 2：地区移动预付费分布**
- 类型：堆叠柱状图
- 数据：按地区划分的 DRP ADA、DXS ADA、License Store ADA
- 位置：位于移动预付费部分的右侧
- 大小：宽 6 列 x 高 15 行

**图表 3：周环比趋势 - 前 3 个地区**
- 类型：带标记的折线图
- 数据：按 RT Total ADA 排名的前 3 个地区的周环比百分比
- 位置：位于主表格下方
- 大小：宽 12 列 x 高 12 行

## 错误处理

### 文件缺失
```python
if len(current_week_files) != 6:
    raise ValueError(f"Expected 6 current week files, found {len(current_week_files)}")

if len(previous_week_files) != 6:
    raise ValueError(f"Expected 6 previous week files, found {len(previous_week_files)}")
```

### 商店未映射
```python
unmapped_stores = []
for store in all_stores:
    if map_store_to_region(store) == "Others":
        # Log warning but continue processing
        unmapped_stores.append(store)

if unmapped_stores:
    print(f"Warning: {len(unmapped_stores)} stores mapped to 'Others' region")
```

### 数据质量检查
```python
# Check for negative values
if any_value < 0:
    print(f"Warning: Negative value found in {file}:{column}")

# Check for missing regions
expected_regions = {"NCR", "SLZ", "NLZ", "CLZ", "EVIS", "WVIS", "MIN", "Others"}
missing_regions = expected_regions - set(actual_regions)
if missing_regions:
    print(f"Warning: Missing regions: {missing_regions}")
```

## 实施说明

### Python 库
```python
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
import re
from datetime import datetime
```

### 关键函数

#### 1. 文件解析器
```python
def extract_date_from_filename(filename):
    """Extract date range from filename like 'Report_1_11-1_17.xlsx'"""
    pattern = r'_(\d+)_(\d+)-(\d+)_(\d+)\.xlsx'
    match = re.search(pattern, filename)
    if match:
        start_month, start_day, end_month, end_day = match.groups()
        return (int(start_month), int(start_day), int(end_month), int(end_day))
    return None

def identify_file_type(filename):
    """Identify file type from filename"""
    if 'DRP_Channel_Sales' in filename:
        return 'DRP'
    elif 'TECNO' in filename:
        return 'TECNO'
    elif 'License_Store' in filename:
        return 'LS'
    elif 'Mobile_Prepaid' in filename:
        return 'DXS_Prepaid'
    elif 'Mobile_Postpaid' in filename:
        return 'DXS_Postpaid'
    elif 'FWA' in filename:
        return 'DXS_FWA'
    return 'Unknown'
```

#### 2. 数据提取器
```python
def extract_drp_data(filepath):
    """Extract DRP channel sales data"""
    df = pd.read_excel(filepath, sheet_name='Sheet0', header=None)
    
    # Find data start row (usually row 8)
    data_start = 8
    
    # Extract by region
    regions_data = {}
    for idx in range(data_start, len(df)):
        region = df.iloc[idx, 0]
        if pd.isna(region) or region == 'Total':
            continue
            
        regions_data[region] = {
            'mobile_postpaid': df.iloc[idx, 1],
            'mobile_prepaid': df.iloc[idx, 5],
            'double_data': df.iloc[idx, 6],
            'fwa_4g': df.iloc[idx, 9],
            'fwa_5g': df.iloc[idx, 10] + df.iloc[idx, 11]
        }
    
    return regions_data

def extract_dxs_data(filepath, product_type):
    """Extract DXS acquisition data"""
    df = pd.read_excel(filepath, sheet_name='Sheet1', header=None)
    
    # Determine column based on product type
    if product_type == 'prepaid':
        value_col = 4
    elif product_type == 'postpaid':
        value_col = 12
    elif product_type == 'fwa':
        return extract_dxs_fwa_data(df)
    
    stores_data = {}
    for idx in range(8, len(df)):
        store = df.iloc[idx, 0]
        if pd.isna(store) or store in ['Grand Total', '-']:
            continue
        
        value = df.iloc[idx, value_col]
        if pd.notna(value):
            stores_data[store] = value
    
    return stores_data

def extract_dxs_fwa_data(df):
    """Extract FWA data with 4G/5G split"""
    stores_data = {}
    for idx in range(8, len(df)):
        store = df.iloc[idx, 0]
        if pd.isna(store) or store in ['Grand Total', '-']:
            continue
        
        fwa_4g = df.iloc[idx, 1] if pd.notna(df.iloc[idx, 1]) else 0
        total = df.iloc[idx, 18] if pd.notna(df.iloc[idx, 18]) else 0
        fwa_5g = total - fwa_4g
        
        stores_data[store] = {
            'fwa_4g': fwa_4g,
            'fwa_5g': fwa_5g
        }
    
    return stores_data
```

#### 3. 地区汇总器
```python
def aggregate_by_region(stores_data, mapping_dict, regions):
    """Aggregate store data by region"""
    regional_totals = {region: 0 for region in regions}
    
    for store, value in stores_data.items():
        region = map_store_to_region(store, mapping_dict)
        if isinstance(value, dict):
            # Handle nested data (e.g., FWA with 4G/5G)
            for key in value:
                if key not in regional_totals:
                    regional_totals[key] = {region: 0 for region in regions}
                regional_totals[key][region] += value[key]
        else:
            regional_totals[region] += value
    
    return regional_totals
```

#### 4. 周环比计算器
```python
def calculate_wow(current, previous):
    """Calculate week-over-week percentage change"""
    if previous == 0 or pd.isna(previous):
        return "-"
    
    if current == 0 or pd.isna(current):
        return "-100%"
    
    wow = ((current - previous) / previous) * 100
    return f"{int(round(wow))}%"
```

#### 5. Excel 格式化
```python
def apply_formatting(ws, start_row, start_col, end_row, end_col):
    """Apply formatting to Excel worksheet"""
    # Define styles
    header_fill = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")
    total_fill = PatternFill(start_color="E6F2FF", end_color="E6F2FF", fill_type="solid")
    
    green_font = Font(color="008000")
    red_font = Font(color="FF0000")
    gray_font = Font(color="808080")
    bold_font = Font(bold=True)
    
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Apply to cells
    for row in ws.iter_rows(min_row=start_row, max_row=end_row, 
                            min_col=start_col, max_col=end_col):
        for cell in row:
            cell.border = thin_border
            
            # Color code WoW values
            if isinstance(cell.value, str) and '%' in cell.value:
                try:
                    pct_value = int(cell.value.replace('%', ''))
                    if pct_value > 0:
                        cell.font = green_font
                    elif pct_value < 0:
                        cell.font = red_font
                except:
                    if cell.value == '-':
                        cell.font = gray_font

def add_chart(ws, chart_type, data_range, position, title):
    """Add chart to worksheet"""
    if chart_type == 'column':
        chart = BarChart()
    elif chart_type == 'line':
        chart = LineChart()
    
    chart.title = title
    chart.style = 10
    chart.height = 10
    chart.width = 15
    
    data = Reference(ws, min_col=data_range[0], min_row=data_range[1],
                     max_col=data_range[2], max_row=data_range[3])
    chart.add_data(data, titles_from_data=True)
    
    ws.add_chart(chart, position)
```

## 使用示例

```python
from retail_trade_report_skill import generate_weekly_report

# Input files directory
input_dir = "/mnt/user-data/uploads/"

# Store mapping CSV
mapping_file = "/mnt/user-data/uploads/store_mapping.csv"

# Generate report
output_file = generate_weekly_report(
    input_dir=input_dir,
    mapping_csv=mapping_file,
    output_path="/mnt/user-data/outputs/Retail_Trade_Weekly_Report.xlsx"
)

print(f"Report generated: {output_file}")
```

## 验证清单

在最终输出之前：
- [ ] 所有 12 个输入文件均已识别并处理
- [ ] 日期范围正确提取并显示
- [ ] 所有商店均已映射到地区（未映射的记录标记为“其他”）
- [ ] 所有周环比计算已完成
- [ ] 无负 ADA 值（错误日志除外）
- [ ] 所有公式均经过样本数据验证
- [ ] 图表正确渲染
- [ ] 所有周环比单元格均应用了颜色编码
- [ ] 总计行正确求和
- [ ] 输出文件无错误

## 性能考虑

- 预计处理时间：12 个文件需 10-30 秒
- 内存使用：约 50-100 MB
- 处理大文件：支持每个文件大小不超过 10MB
- 并行处理：尽可能并行处理文件

## 故障排除

### 常见问题

**问题：“文件未找到”错误**
- **解决方案：** 确认所有 12 个文件均已上传且文件名符合预期格式

**问题：** 商店名称未映射到地区
- **解决方案：** 检查映射 CSV 中的拼写错误，为常见变体添加别名

**问题：** 所有周环比值为“N/A”
- **解决方案：** 确认上周文件已正确识别（日期正确）

**问题：** 图表未显示
- **解决方案：** 检查 openpyxl 版本是否大于或等于 3.0，并验证图表数据范围

**问题：** ADA 值为负数
- **解决方案：** 检查源数据中的错误，并验证列索引

## 版本历史

- **v1.0**（2026-02-02）：初始技能创建
  - 支持生成 12 个文件的周报
  - 周环比计算并应用颜色编码
  - 支持使用别名进行商店到地区的映射
  - 提供三种图表类型进行可视化