---
name: lead-enrichment
description: >
  使用 LinkedIn 个人资料、电子邮件地址、公司信息和教育背景来丰富联系人和潜在客户的记录。当需要执行以下操作时，请使用此功能：  
  - “丰富联系人信息”  
  - “填写缺失的数据”  
  - “查找潜在客户的电子邮件地址”  
  - “完善潜在客户的个人资料”  
  - “查询公司信息”  
  - 或者任何针对 CRM 记录的大批量数据填充任务。
metadata: { "openclaw": { "emoji": "✨" } }
---
# 客户关系管理（CRM）数据优化——多源数据补全

通过从多个来源填充缺失的字段来优化CRM联系人记录。支持DuckDB工作区的数据或独立的JSON数据。

## 数据来源（优先级顺序）  
1. **领英（LinkedIn）**（通过linkedin-scraper技能）——姓名、职位、公司信息、教育背景、联系人  
2. **网络搜索**（通过web_search工具）——电子邮件地址、公司信息、社交媒体资料  
3. **公司官网**（通过web_fetch）——团队页面、公司简介页面、联系方式  
4. **电子邮件地址生成**——根据姓名和公司域名推断电子邮件地址  

## 数据优化流程  

### 第一步：识别缺失的信息  
```sql
-- Query the target object to find gaps
SELECT "Name", "Email", "LinkedIn URL", "Company", "Title", "Location"
FROM v_leads
WHERE "Email" IS NULL OR "LinkedIn URL" IS NULL OR "Title" IS NULL;
```  

### 第二步：根据重要性排序  
- **高优先级**：缺失的电子邮件地址（用于联系客户）  
- **中等优先级**：缺失的职位或公司名称（用于个性化信息）  
- **低优先级**：缺失的教育背景、联系人数量、公司简介  

### 第三步：逐条记录进行数据优化  

对于每条存在信息缺失的记录：  

#### 如果已知领英URL但其他字段缺失：  
1. 使用linkedin-scraper访问该用户的领英个人资料  
2. 提取：职位、公司名称、所在地、教育背景、公司简介  
3. 更新DuckDB中的记录  

#### 如果缺少领英URL：  
1. 在领英上搜索：`{name} {company}` 或 `{name} {title}`  
2. 验证搜索结果是否与实际信息一致  
3. 保存领英URL，然后抓取完整的个人资料  

#### 如果缺少电子邮件地址：  
1. 查找公司域名（通过网络搜索或领英公司页面）  
2. 尝试以下常见的电子邮件格式：  
   - `first@domain.com`  
   - `first.last@domain.com`  
   - `flast@domain.com`  
   - `firstl@domain.com`  
3. 可以通过网络搜索验证：`"email" "{name}" site:{domain}`  
4. 查看公司团队或公司简介页面以获取电子邮件格式的线索  

#### 如果缺少公司信息：  
1. 进行网络搜索：`"{name}" "{title}"` 或查看领英信息  
2. 从公司官网获取：行业、公司规模、公司描述、融资情况  

### 第四步：更新记录  
```sql
-- Update via DuckDB pivot view
UPDATE v_leads SET
  "Email" = ?,
  "LinkedIn URL" = ?,
  "Title" = ?,
  "Company" = ?,
  "Location" = ?
WHERE id = ?;
```  

## 批量数据优化模式  

- 一次性优化多条记录：  
1. 从DuckDB中查询所有不完整的记录  
2. 按公司名称分组（抓取一次公司信息后应用于所有员工）  
3. 分批处理（每批10-20条记录）  
4. 每处理一批后报告进度：  
   ```
   Enrichment Progress: 45/120 leads (38%)
   ├── Emails found: 32/45 (71%)
   ├── LinkedIn matched: 41/45 (91%)
   ├── Titles updated: 38/45 (84%)
   └── ETA: ~15 min remaining
   ```  
5. 每处理一批后保存进度（以防中断）  

## 数据优化质量规则  
- **置信度评分**：为每个优化后的字段标注置信度（高/中/低）：  
  - 高：直接从领英个人资料或公司官网获取  
  - 中：根据模式推断或部分匹配  
  - 低：通过网络搜索结果得出的最佳猜测  
- **切勿覆盖现有数据**（除非另有要求）  
- **标记冲突**：如果优化后的数据与现有数据矛盾，标记以供审核  
- **去重检查**：在插入领英URL之前，确认该URL尚未分配给其他联系人  

## 电子邮件地址生成策略  

常见的企业电子邮件格式（按出现频率排序）：  
1. `first.last@domain.com`（最常见，约45%）  
2. `first@domain.com`（约20%）  
3. `flast@domain.com`（约15%）  
4. `firstl@domain.com`（约10%）  
5. `first_last@domain.com`（约5%）  
6. `last.first@domain.com`（约3%）  
7. `first.l@domain.com`（约2%）  

**策略**：  
1. 如果知道某人在公司的电子邮件地址，就使用该地址生成格式  
2. 在网上搜索`"@{domain}"`格式的电子邮件地址  
3. 查看公司团队页面的源代码中的`mailto:`链接  
4. 使用最常见的格式作为默认选项  

## 输出结果  

优化完成后，提供以下汇总信息：  
```
Enrichment Complete: 120 leads processed
├── Emails: 94 found (78%), 26 still missing
├── LinkedIn: 108 matched (90%), 12 not found
├── Titles: 115 updated (96%)
├── Companies: 118 confirmed (98%)
├── Locations: 89 found (74%)
└── Avg confidence: High (82%), Medium (14%), Low (4%)

Top gaps remaining:
- 26 leads missing email (mostly small/stealth companies)
- 12 leads missing LinkedIn (common names, ambiguous matches)
```  

## DuckDB字段映射  

Ironclaw CRM对象的标准字段名称与DuckDB字段的对应关系：  
| 优化后的数据 | DuckDB字段 | 类型 |  
|----------------|--------------|------|  
| 全名 | Name       | text    |  
| 电子邮件地址 | Email       | email    |  
| 领英URL     | LinkedIn URL    | url      |  
| 职位       | Title       | text    |  
| 公司名称     | Company      | text    |  
| 所在地      | Location     | text    |  
| 教育背景    | Education     | text    |  
| 电话号码    | Phone       | phone    |  
| 公司规模     | Company Size   | text    |  
| 行业        | Industry     | text    |  
| 优化日期     | Enriched At    | date     |  
| 置信度      | Enrichment Confidence | enum (高/中/低) |