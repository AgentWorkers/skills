---
name: wikidata-query-skill
description: 将自然语言问题转换为用于Wikidata的SPARQL查询，并生成美观的HTML结果页面。使用简单的英文提示来查询Wikidata知识库。
---
# 维基数据查询技能

## 适用场景

当用户需要执行以下操作时，可以使用此技能：
- 使用自然语言查询维基数据
- 获取关于实体的全面、多语言信息
- 访问包含丰富属性的数据（维基数据拥有大量的属性）
- 创建维基数据查询结果的可视化展示
- 从SPARQL查询中生成HTML报告
- 查询比DBpedia具有更完整时间覆盖范围的数据

## 核心功能

✅ **自然语言转SPARQL**：将用户问题转换为有效的维基数据SPARQL语句
✅ **查询执行**：针对维基数据查询服务执行查询
✅ **HTML生成**：创建美观、交互式的HTML结果页面
✅ **多种输出格式**：JSON、Markdown表格或HTML
✅ **标签服务**：为结果提供自动标签解析功能（便于人类阅读）

## 维基数据端点

**SPARQL端点**：`https://query.wikidata.org/sparql`
**接受请求头**：`application/sparql-results+json`
**请求方法**：带有URL编码查询的HTTP GET请求
**用户代理**：必须指定（使用 `Claude-Code-Wikidata-Skill/1.0`）

## 维基数据命名规范

**属性**：`wdt:P###`（例如，`wdt:P57` 表示“导演”）
**实体**：`wd:Q###`（例如，`wd:Q51566` 表示“斯派克·李”）
**服务**：`wikibase:label` 用于自动标签解析

## 常见维基数据属性

```
P31  - instance of
P57  - director
P577 - publication date
P2130 - cost/budget
P50  - author
P170 - creator
P19  - place of birth
P20  - place of death
P569 - date of birth
P570 - date of death
P27  - country of citizenship
P106 - occupation
P735 - given name
P734 - family name
P1082 - population
P36  - capital
```

## 查询转换流程

当用户提供自然语言指令时：

### 1. 确定实体

找到相关实体的维基数据Q编号：
- 如有需要，可使用描述性搜索
- 例如：“斯派克·李” → `wd:Q51566`

### 2. 映射到维基数据属性

**常见映射关系**：
- “由……执导” → `wdt:P57`
- “发布日期” → `wdt:P577`
- “预算” → `wdt:P2130`
- “出生地” → `wdt:P19`
- “作者” → `wdt:P50`
- “人口” → `wdt:P1082`
- “首都” → `wdt:P36`

### 3. 构建SPARQL查询

**使用标签服务的模板：**
```sparql
SELECT DISTINCT ?item ?itemLabel ?property
WHERE {
  ?item wdt:P### wd:Q### ;     # property: entity
        wdt:P31 wd:Q### .       # instance of: type
  OPTIONAL { ?item wdt:P### ?property . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY <sort_criteria>
LIMIT <number>
```

**重要提示**：务必包含标签服务，以确保结果易于人类阅读！

### 4. 执行查询

使用curl并设置正确的请求头：
```bash
curl -s -G "https://query.wikidata.org/sparql" \
  -H "Accept: application/sparql-results+json" \
  -H "User-Agent: Claude-Code-Wikidata-Skill/1.0" \
  --data-urlencode "query=<SPARQL_QUERY>"
```

### 5. 生成输出

**输出选项**：
- **JSON**：原始查询结果
- **Markdown表格**：适合终端显示的格式化结果
- **HTML页面**：包含维基数据品牌标识的交互式结果页面

## 示例查询模式

### 模式1：导演执导的电影
**用户**：“展示斯派克·李执导的电影”

**SPARQL查询**：
```sparql
SELECT DISTINCT ?film ?filmLabel ?publicationDate ?budget
WHERE {
  ?film wdt:P57 wd:Q51566 ;        # director: Spike Lee
        wdt:P31 wd:Q11424 .         # instance of: film
  OPTIONAL { ?film wdt:P577 ?publicationDate . }
  OPTIONAL { ?film wdt:P2130 ?budget . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?publicationDate)
```

### 模式2：作者写的书籍
**用户**：“列出J.K.罗琳写的书籍”

**SPARQL查询**：
```sparql
SELECT DISTINCT ?book ?bookLabel ?publicationDate
WHERE {
  ?book wdt:P50 wd:Q34660 ;        # author: J.K. Rowling
        wdt:P31 wd:Q7725634 .      # instance of: literary work
  OPTIONAL { ?book wdt:P577 ?publicationDate . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?publicationDate
```

### 模式3：20世纪出生的著名物理学家
**用户**：“20世纪出生的著名物理学家有哪些？”

**SPARQL查询**：
```sparql
SELECT ?person ?personLabel ?birthDate ?birthPlaceLabel
WHERE {
  ?person wdt:P106 wd:Q169470 ;     # occupation: physicist
          wdt:P569 ?birthDate .     # date of birth
  OPTIONAL { ?person wdt:P19 ?birthPlace . }
  FILTER(YEAR(?birthDate) >= 1900 && YEAR(?birthDate) < 2000)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?birthDate
LIMIT 50
```

### 模式4：地理查询
**用户**：“欧洲国家的首都是哪些？”

**SPARQL查询**：
```sparql
SELECT ?country ?countryLabel ?capital ?capitalLabel ?population
WHERE {
  ?country wdt:P30 wd:Q46 ;         # continent: Europe
           wdt:P36 ?capital .       # capital
  ?capital wdt:P1082 ?population .  # population
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?population)
```

### 模式5：诺贝尔奖得主
**用户**：“列出诺贝尔文学奖得主”

**SPARQL查询**：
```sparql
SELECT ?person ?personLabel ?awardYear
WHERE {
  ?person wdt:P166 wd:Q37922 ;      # award received: Nobel Prize in Literature
          wdt:P569 ?birthDate .
  OPTIONAL { ?person wdt:P166 ?award .
             ?award wdt:P585 ?awardYear . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?awardYear)
```

## 查找维基数据实体

如果需要查找某个实体的Q编号：

**方法1：搜索查询**
```sparql
SELECT ?item ?itemLabel ?itemDescription
WHERE {
  ?item rdfs:label "Spike Lee"@en .
  ?item wdt:P106 wd:Q2526255 .      # occupation: film director
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 5
```

**方法2：使用维基数据搜索**
- 访问 https://www.wikidata.org
- 搜索该实体
- 注意URL中的Q编号

## HTML模板生成

生成HTML结果时，需要包含以下元素：
1. **标题**：问题或查询描述
2. **统计信息**：结果数量
3. **表格**：包含超链接的维基数据实体
4. **SPARQL查询显示**：展示带有语法高亮的查询内容
5. **页脚**：包含维基数据链接、来源信息和许可证说明

## 维基数据的设计规范

- 使用蓝色/绿色配色方案（维基数据的官方颜色）
- 包含维基数据标志链接
- 提供前往 https://www.wikidata.org 的链接
- 强调维基数据的协作性质

## HTML模板结构
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>[Query Description] - Wikidata</title>
    <style>
        /* Blue/green Wikidata theme */
        /* Responsive design */
        /* Interactive elements */
    </style>
</head>
<body>
    <div class="container">
        <h1>[Question/Title]</h1>
        <div class="wikidata-badge">Wikidata</div>
        <div class="stats">[Results count]</div>
        <table>[Results with Wikidata links]</table>
        <div class="sparql-query">[Query code]</div>
        <div class="footer">[Attribution + CC0 license]</div>
    </div>
</body>
</html>
```

## 错误处理

### 超时错误
维基数据查询服务有查询时间限制：
- 使用 `LIMIT` 子句（默认值：100）
- 简化复杂的连接操作
- 删除不必要的 `OPTIONAL` 子句

### 无结果
- 检查实体Q编号是否正确
- 验证属性P编号是否有效
- 建议使用维基数据搜索功能

### 标签服务问题
- 必须添加：`SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }`
- 使用 `?variableLabel` 获取人类可读的实体名称

## 最佳实践

1. **始终使用标签服务**：使结果更易于阅读
2. **检查Q/P编号**：验证实体和属性的标识符
3. **设置查询限制**：默认限制为100条结果
4. **处理可选属性**：对于可能不存在的属性，使用 `OPTIONAL` 子句
5. **按语言过滤结果**：在未使用标签服务时进行筛选
6. **有序显示结果**：确保输出信息有条理
7. **添加用户代理**：维基数据查询服务要求必须提供用户代理信息

## 维基数据与DBpedia的比较

- **何时使用维基数据**：
  - 当需要更精确的时间数据（如发布日期、出生日期）
  - 需要多语言支持
  - 需要全面的属性信息
  - 需要结构化的标识符（Q/P系统）

- **何时使用DBpedia**：
  - 查询与维基百科相关的数据
  - 需要预算/财务信息（DBpedia覆盖更全面）
  - 仅处理英文查询

## 示例会话

**用户**：“列出克里斯托弗·诺兰执导的所有电影及其发布日期和预算”

**助手**：
“我将查询维基数据中关于克里斯托弗·诺兰的电影信息。
首先，我需要找到他的维基数据ID……”
[搜索并找到 `wd:Q25191`]

“正在执行针对维基数据查询服务的SPARQL查询……”
[构建并执行查询]

“找到了12部电影！您希望结果以以下格式显示：
1. JSON
2. Markdown表格
3. HTML页面”

**用户**：“HTML页面”

**助手**：
[生成包含维基数据品牌标识的HTML页面]

“✓ HTML页面已生成并保存为：./christopher_nolan_films.html
✓ 找到12部电影
✓ 其中10部电影有发布日期
✓ 5部电影有预算信息”

## 输出格式选择

始终询问用户希望的结果格式：
```
"Would you like the results as:
1. JSON (raw data)
2. Markdown table (terminal display)
3. HTML page (interactive visualization)"
```

## 技能范围

- 支持对维基数据中的实体进行查询
- 提取包含属性的结构化数据
- 执行多属性查询
- 处理时间相关的查询（如日期、年份）
- 支持结果格式化和可视化展示

**本技能不支持的功能**：
- 全文搜索（请使用维基数据搜索功能）
- 数据修改（仅支持读取操作）
- 非英文标签的处理（需通过标签服务进行配置）

## 重要注意事项

- **必须提供用户代理**：请求头中必须包含用户代理信息
- **遵守查询服务限制**：避免超出查询服务的时间限制
- **查询超时**：最长60秒
- **许可证**：所有维基数据遵循CC0（公共领域）许可协议

---

**版本**：1.0.0
**端点**：`https://query.wikidata.org/sparql`
**数据来源**：维基数据（协作式知识库）
**许可证**：CC0（公共领域）