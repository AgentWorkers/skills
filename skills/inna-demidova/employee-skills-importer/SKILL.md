---
name: employee-skills-importer
description: 解析员工技能的 CSV 文件，识别技能类别和具体技能；从员工表中查找员工 ID；并为技能类别、技能以及员工技能表生成幂等的 SQL INSERT 语句。
---
# 员工技能导入器

该工具可自动化将员工技能信息从CSV文件导入Supabase数据库的过程。它首先解析CSV文件，检查数据库中已有的数据，然后生成幂等的SQL脚本以插入缺失的数据。

## 概述

该工具执行以下三个步骤：
1. **识别并插入缺失的技能类别**：从CSV文件头部提取类别信息，检查数据库中是否存在这些类别，并生成相应的INSERT脚本。
2. **识别并插入缺失的技能**：提取技能名称及其所属类别，检查数据库中是否存在这些技能，并生成相应的INSERT脚本。
3. **生成员工技能INSERT脚本**：根据员工姓名将技能信息与员工关联起来，最终生成完整的INSERT语句。

## CSV文件格式要求

CSV文件必须满足以下格式：
- **第1行**：为空或包含元数据（将被忽略）。
- **第2行**：包含多个列的技能类别名称。
- **第3行及以后**：包含各个技能名称（列标题可能因换行符而分布在多行中）。
- **员工数据行**：前两列包含员工的名字（first_name, last_name），后列包含技能经验年限（years_of_experience）。

示例结构：
```
,,,,,,.NET,,,,,Front-end,,,Java,,,
First Name,Last Name,Full Name,Unit,...,C#,ASP.net,MVC,...,JavaScript,HTML,CSS,...,Java,Spring,...
John,Doe,John Doe,Unit 1,...,5,4,3,...,6,6,5,...,0,0,...
```

## 工作流程

### 第1步：技能类别

1. 解析第2行以提取唯一的类别名称。
2. 查询数据库以确认类别是否存在：
   ```sql
   SELECT name FROM skill_categories
   ```
3. 为缺失的类别生成幂等的INSERT脚本：
   ```sql
   INSERT INTO skill_categories (name) 
   VALUES ('Category1'), ('Category2'), ('Category3')
   ON CONFLICT (name) DO NOTHING;
   ```

### 第2步：技能信息

1. 解析技能名称行，并将其与第2行中的类别信息关联起来。
2. 查询数据库以确认技能是否存在：
   ```sql
   SELECT s.name, sc.name as category_name 
   FROM skills s 
   LEFT JOIN skill_categories sc ON s.category_id = sc.id
   ```
3. 对于每个需要插入的技能：
   - 使用子查询查找对应的类别ID。
   - 生成幂等的INSERT脚本：
   ```sql
   INSERT INTO skills (name, category_id)
   VALUES 
     ('C#', (SELECT id FROM skill_categories WHERE name = '.NET')),
     ('JavaScript', (SELECT id FROM skill_categories WHERE name = 'Front-end'))
   ON CONFLICT (name) DO NOTHING;
   ```

### 第3步：员工技能信息

1. 解析员工数据行（first_name, last_name, skill_values）。
2. 查询employees表以获取员工ID：
   ```sql
   SELECT id, first_name, last_name FROM employees
   ```
3. 对于每个员工及其每个技能（经验年限非零的情况）：
   - 通过first_name和last_name查找员工ID。
   - 使用子查询查找技能ID。
   **关键注意事项**：在WHERE子句中使用TRIM()函数来处理数据库中的空白字符。
   - 生成INSERT语句：
   ```sql
   INSERT INTO employee_skills (employee_id, skill_id, years_of_experience)
   VALUES 
     (
       (SELECT id FROM employees WHERE TRIM(first_name) = 'John' AND TRIM(last_name) = 'Doe'),
       (SELECT id FROM skills WHERE name = 'C#'),
       5
     )
   ON CONFLICT (employee_id, skill_id) DO UPDATE 
   SET years_of_experience = EXCLUDED.years_of_experience;
   ```

## 重要说明

### 数据库架构
- `skill_categories`表：id (uuid), name (text, 唯一)
- `skills`表：id (uuid), name (text, 唯一), category_id (uuid, 外键，引用skill_categories表)
- `employees`表：id (uuid), first_name (text), last_name (text)
- `employee_skills`表：id (uuid), employee_id (uuid, 外键，引用employees表), skill_id (uuid, 外键), years_of_experience (real)

### 幂等性
所有生成的SQL脚本都使用了`ON CONFLICT`子句，以确保可以多次执行而不会产生错误：
- 对于类别和技能：`ON CONFLICT (name) DO NOTHING`
- 对于员工技能：`ON CONFLICT (employee_id, skill_id) DO UPDATE SET years_of_experience = EXCLUDED.years_of_experience`

### 数据处理
- 跳过那些在某项技能上没有经验记录的员工。
- 处理数值型经验年限（可以是整数或小数，例如0.5、1.7等）。
- 通过去除空白字符和换行符来清理技能名称。
- 跳过在数据库中找不到对应员工的记录。
- 正确处理多行CSV数据。
- **关键注意事项**：在生成SQL之前，必须删除重复的员工-技能对，保留经验年限最高的记录。
- **关键注意事项**：自动纠正员工姓名的拼写错误（使用模糊匹配算法）。
- **关键注意事项**：删除所有姓名前后的空白字符。
- **关键注意事项**：在SQL的WHERE子句中使用TRIM()函数来处理数据库中的多余空白字符。
- **关键注意事项**：如果数据库中找不到匹配项，则跳过这些记录并报告它们。

### 错误预防
- 始终使用子查询来查找外键，而不是硬编码UUID。
- 确保CSV文件中的类别名称与数据库中的名称一致。
- 报告所有在数据库中找不到的员工记录。
- 报告无法映射到类别的技能记录。

**关键注意事项 - 防止重复键违规：**
1. 在生成员工技能INSERT语句之前，根据first_name、last_name和skill字段对所有记录进行去重。
2. 如果存在重复记录，保留经验年限最高的记录。
   这可以防止`ON CONFLICT DO UPDATE`命令重复修改同一行。

**关键注意事项 - 自动名称校正：**
1. 在生成SQL之前，确认所有员工都存在于数据库中。
2. 对于无法通过精确匹配找到的员工：
   - 使用模糊匹配算法（如Levenshtein距离）在数据库中查找相似的记录。
   - 如果找到相似记录（例如“Victoriia”对应“Viktoriia”），则使用数据库中的正确拼写。
   - 如果没有找到相似记录，则完全跳过该员工。
3. 生成报告，显示：
   - 经过自动校正的员工姓名（CSV中的名称 → 数据库中的名称）。
   - 被跳过的员工（未找到匹配项）及其对应的技能数量。
   这可以防止“employee_id”字段出现空值，从而违反非空约束。

## 输出格式

该工具生成三个SQL脚本和一个报告文件：
- **1_insert_categories.sql**
- **2_insert_skills.sql**
- **3_insert_employee_skills.sql**

## 执行步骤

当用户提供CSV文件时：
1. **解析CSV文件格式**：
   - 读取文件并验证格式。
   - 从第2行提取类别名称。
   - 从后续行提取技能名称（处理多行数据）。
   - 根据列位置将技能名称与其所属类别关联起来。
2. **查询Supabase数据库中的现有数据**：
   - 获取所有现有的技能类别。
   - 获取所有现有的技能及其所属类别。
   - 获取所有员工的ID（first_name, last_name）。
3. **生成脚本1：类别**：
   - 将CSV中的类别与数据库中的类别进行比较。
   - 为缺失的类别生成INSERT语句。
   - 将脚本保存到文件中并呈现给用户。
4. **生成脚本2：技能**：
   - 将CSV中的技能与数据库中的技能进行比较。
   - 对于缺失的技能，包含类别查找子查询。
   - 生成INSERT语句。
   - 将脚本保存到文件中并呈现给用户。
5. **生成脚本3：员工技能**：
   - 解析员工数据行。
   - **验证**：将CSV中的员工信息与数据库中的信息进行精确匹配。
   - **模糊匹配**：对于不精确匹配的情况，使用相似性算法在数据库中查找最接近的匹配项。
     - 分别计算first_name和last_name的相似性得分。
     - 如果总相似度超过阈值（例如85%），则使用数据库中的名称。
     - 记录所有自动校正的内容以供报告使用。
   - **校正**：将CSV中的名称替换为数据库中的名称。
   - **过滤**：跳过没有找到匹配项的员工。
   - **去重**：根据first_name和skill字段删除重复记录，保留经验年限最高的记录。
   - 生成包含校正后名称的INSERT语句。
   - 生成报告，显示校正内容和被跳过的员工。
   - 将SQL文件保存到输出目录。
   - 将所有文件呈现给用户。
6. **将所有文件呈现给用户**：
   - 三个SQL脚本（1_insert_categories.sql、2_insert_skills.sql、3_insert_employee_skills.sql）。
   - 如果有员工被跳过，则生成一个报告文件（skipped_employees_report.txt）。
   - 用户可以按顺序执行这三个SQL脚本（1 → 2 → 3）。
   - 用户需要查看报告以修复名称不匹配的问题（如果有的话）。

## 使用示例

用户上传CSV文件并请求：“解析这个员工技能CSV文件并生成SQL插入脚本。”

工具的操作流程如下：
1. 分析CSV文件的结构。
2. 连接到Supabase SkillsSystem项目。
3. 检查三个表中的现有数据。
4. 生成三个SQL文件。
5. 提供生成的报告（例如：“发现5个新类别，23个新技能，为47名员工生成插入语句”）。
6. 将三个SQL文件提供给用户下载。

## 项目配置

该工具配置为与Supabase项目配合使用：
- **项目名称**：SkillsSystem
- **项目ID**：ypibfhbklinkvybgotef
- **地区**：eu-central-1

该工具在执行查询时会自动连接到该项目。

## 常见错误及其解决方法

### 错误1：“ON CONFLICT DO UPDATE命令无法再次修改同一行”
**原因**：生成的INSERT语句中存在重复的员工-技能对。
**解决方法**：现在该工具在生成SQL之前会对所有记录进行去重。如果出现此错误，说明去重操作未执行。
**预防措施**：始终根据first_name、last_name和skill字段进行去重，并保留经验年限最高的记录。

### 错误2：“column 'employee_id'中的空值违反了非空约束”
**原因**：CSV中的员工在数据库中不存在（通常是由于姓名拼写差异或空白字符问题）。
**解决方法**：
1. 现在工具会使用模糊匹配算法自动纠正拼写错误。
2. 去除姓名中的所有空白字符。
3. 在SQL的WHERE子句中使用TRIM()函数来匹配数据库中的记录（即使存在多余的空格）。

**常见问题及解决方法：**
- 拼写差异：例如“Victoriia”↔“Viktoriia”，“Karasyov”↔“Karasov”。
- 数据库中的多余空白字符：例如“Yurii   Solokha”（包含3个空格）。
- 名称中的前导/尾随空白字符。

**工作原理：**
- 使用相似性算法将CSV中的姓名与数据库中的姓名进行比较。
- 如果找到相似度超过83%的匹配项，则使用数据库中的正确拼写。
- 在比较之前删除所有姓名中的空白字符。
- 在SQL中使用`TRIM(first_name)`和`TRIM(last_name)`来处理数据库中的多余空白字符。
- 如果没有找到匹配项，则跳过该员工并报告该员工。

### 名称匹配算法
该工具采用以下方法：
1. 首先尝试精确匹配（first_name AND last_name）。
2. 如果没有精确匹配，使用Levenshtein距离或其他相似性算法计算相似度。
- 处理常见的拼写差异（例如“Victoriia”↔“Viktoriia”，“Karasyov”↔“Karasov”）。
- 如果相似度超过83%的阈值，则认为匹配成功。
- 如果找到多个相似项，则选择最接近的一个。
- 如果没有找到匹配项，则跳过该员工。
- 始终删除CSV和数据库名称中的空白字符。
- 在SQL查询中使用TRIM()函数来处理数据库中的多余空白字符。