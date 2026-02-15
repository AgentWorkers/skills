---
name: xlsx-pro
description: "**Excel文件处理能力**  
能够熟练操作Excel格式的文件（包括.xlsx、.xlsm、.csv、.tsv等扩展名）。用户可以根据需要执行以下操作：  
- 打开文件  
- 读取文件内容  
- 编辑文件  
- 创建新的Excel文件  
- 添加新的列  
- 计算公式  
- 格式化表格  
- 绘制图表  
- 清理数据  
- 在不同的表格格式之间进行转换  

**使用场景**：  
该技能适用于需要处理Excel文件的用户，例如数据分析师、财务人员或日常使用Excel进行工作的办公人员。  

**注意事项**：  
- 仅当最终交付成果为Excel文件时，才应使用此技能。  
- 不得将Excel文件转换为Word文档、HTML页面、独立的Python脚本，或集成到Google Sheets系统中使用。"
version: "1.0.1"
author: "Eric Barotte"
---

# OpenClawd 的 Excel 技能

## 简而言之
- 生成/编辑包含 **公式** 的 Excel 文件（而非硬编码的值）。
- 可选功能：通过无头版 LibreOffice 重新计算公式，并检测 Excel 中的错误。
- 预期输出格式：规范的电子表格文件（XLSX/XLSM/CSV/TSV）。

## 先决条件

### Python 依赖项
```bash
pip install openpyxl pandas xlrd xlwt
```

### LibreOffice（用于重新计算公式）
```bash
# Ubuntu/Debian
sudo apt-get install libreoffice-calc libreoffice-common
```

## 质量标准

### 专业字体规范
- 除非另有说明，否则使用一致的字体（Arial 或 Times New Roman）。

### 公式零错误
- 所有 Excel 文件必须 **无错误**（无 #REF!、#DIV/0!、#VALUE!、#N/A、#NAME! 等错误）。

### 模板维护
- 修改时必须 **严格遵循** 现有模板的格式和样式。
- 现有模板的约定始终具有最高优先级。

## 财务报表模板标准

### 颜色编码规范（行业标准）
- **蓝色文本（RGB: 0,0,255）**：硬编码的输入值
- **黑色文本（RGB: 0,0,0）**：所有公式和计算结果
- **绿色文本（RGB: 0,128,0）**：指向同一工作表内其他单元格的链接
- **红色文本（RGB: 255,0,0）**：指向外部文件的链接
- **黄色背景（RGB: 255,255,0）**：需要更新的关键假设或单元格

### 数字格式规范
- **年份**：采用文本格式（例如 "2024" 而非 "2,024"）
- **货币**：使用 "$#,##0" 格式；在标题中注明单位（例如 "Revenue ($mm)"）
- **零值**：显示为 "-"（格式："$#,##0;($#,##0);-"）
- **百分比**：默认使用 0.0% 格式
- **倍数**：使用 0.0x 格式（例如 EV/EBITDA、P/E）
- **负数**：使用括号表示（例如 123 而非 -123）

## 强制要求：使用公式，切勿硬编码数值
**务必使用 Excel 公式进行计算，而非直接在 Python 中进行硬编码。**

### ❌ 错误做法：硬编码数值
```python
# Mauvais: Calcul Python puis hardcode
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcode 5000

# Mauvais: Taux de croissance calculé en Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcode 0.15
```

### ✅ 正确做法：使用 Excel 公式
```python
# Bon: Laisser Excel calculer
sheet['B10'] = '=SUM(B2:B9)'

# Bon: Taux de croissance en formule Excel
sheet['C5'] = '=(C4-C2)/C2'

# Bon: Moyenne en fonction Excel
sheet['D20'] = '=AVERAGE(D2:D19)'
```

## 工作流程

### 标准工作流程
1. **选择工具**：使用 pandas 处理数据，使用 openpyxl 处理公式和格式。
2. **创建/加载**：新建工作表或加载现有文件。
3. **修改**：数据、公式和格式。
4. **保存**：保存文件。
5. **重新计算公式（必须执行）**：运行 `python scripts/recalc.py output.xlsx` 脚本。
6. **检查并修正** 检测到的错误。

### 使用 pandas 进行数据读取与分析
```python
import pandas as pd

# Lire Excel
df = pd.read_excel('file.xlsx')  # Première feuille par défaut
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # Dict de toutes les feuilles

# Analyser
df.head()      # Aperçu
df.info()      # Info colonnes
df.describe()  # Statistiques

# Écrire
df.to_excel('output.xlsx', index=False)
```

### 创建 Excel 文件
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Données
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Formule
sheet['B2'] = '=SUM(A1:A10)'

# Formatage
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Largeur colonne
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 编辑现有 Excel 文件
```python
from openpyxl import load_workbook

# Charger fichier existant
wb = load_workbook('existing.xlsx')
sheet = wb.active  # ou wb['NomFeuille']

# Parcourir les feuilles
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Feuille: {sheet_name}")

# Modifier
sheet['A1'] = 'Nouvelle Valeur'
sheet.insert_rows(2)  # Insérer ligne
sheet.delete_cols(3)  # Supprimer colonne

# Ajouter feuille
new_sheet = wb.create_sheet('NouvelleFeuille')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 公式重新计算

openpyxl 创建的文件中仅包含公式字符串，不包含计算结果。请使用 `recalc.py` 脚本进行重新计算：

```bash
python scripts/recalc.py <fichier_excel> [timeout_secondes]
```

该脚本的功能包括：
- 在首次运行时自动配置 LibreOffice 宏。
- 重新计算所有公式。
- 检查所有单元格中的 Excel 错误。
- 以 JSON 格式返回错误详情及位置。

### 输出结果的解释
```json
{
  "status": "success",           // ou "errors_found"
  "total_errors": 0,             // Nombre total d'erreurs
  "total_formulas": 42,          // Nombre de formules
  "error_summary": {             // Présent si erreurs
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 验证检查清单

### 必须执行的验证项
- [ ] **测试 2-3 个引用**：确保它们引用的值正确。
- [ ] **列对应关系**：确认列号正确（例如第 64 列对应 BL 而非 BK）。
- [ ] **行索引**：Excel 的行索引从 1 开始（例如 DataFrame 的第 5 行对应 Excel 的第 6 行）。

### 常见问题
- [ ] **处理 NaN 值**：使用 `pd.notna()` 检查空值。
- **数据位置**：财务数据通常位于第 50 列以后。
- **多重引用**：确保所有引用都有效。
- **除以零**：检查是否存在除以零的情况（#DIV/0!）。
- **引用有效性**：确保所有引用都指向有效的单元格（#REF!）。
- **跨工作表引用**：确保引用格式正确（例如 Sheet1!A1）。

## 良好实践

### 库的选择
- **pandas**：用于数据分析和批量操作，以及简单的导出功能。
- **openpyxl**：用于复杂的格式处理、公式应用以及 Excel 特有的功能。

### 使用 openpyxl 时：
- 单元格索引从 1 开始（例如 row=1, column=1 表示 A1 单元格）。
- 使用 `data_only=True` 仅读取计算结果。
- **注意**：启用 `data_only=True` 会永久替换公式为实际数值。
- 对于大型文件，可以使用 `read_only=True` 或 `write_only=True`。

### 使用 pandas 时：
- 明确指定数据类型：`pd.read_excel('file.xlsx', dtype={'id': str})`。
- 对于大型文件，可以选择需要读取的列：`usecols=['A', 'C', 'E']`。
- 处理日期时使用 `parse_dates=['date_column']`。

## 代码风格规范
**重要提示**：代码应简洁明了，避免不必要的注释。

**对于 Excel 文件**：
- 对包含复杂公式的单元格添加注释。
- 明确记录硬编码数据的来源。
- 为关键计算步骤添加说明性注释。