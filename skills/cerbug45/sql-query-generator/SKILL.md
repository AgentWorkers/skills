# SQL 查询生成技能

## 概述
该技能使 AI 代理能够根据自然语言描述生成准确、优化的 SQL 查询。它支持多种数据库系统，并遵循查询构建、安全性和性能方面的最佳实践。

## 安装

### 方法 1：直接下载
```bash
# Clone or download the repository
git clone https://github.com/yourusername/sql-query-generator.git
cd sql-query-generator

# No external dependencies required for core functionality
python sql_query_generator.py
```

### 方法 2：作为模块使用
```bash
# Copy sql_query_generator.py to your project
cp sql_query_generator.py /path/to/your/project/

# Import in your code
from sql_query_generator import SQLQueryGenerator, DatabaseType
```

### 方法 3：AI 代理集成
对于使用此技能的 AI 代理：
1. 在生成查询之前，请完整阅读本 SKILL.md 文件。
2. 严格遵守所有安全指南。
3. 始终使用参数化查询。
4. 在生成查询之前验证所有输入。
5. 在响应中包含安全警告。

### 可选的数据库驱动程序
仅安装您需要的驱动程序：
```bash
# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install mysql-connector-python

# SQL Server
pip install pyodbc

# Oracle
pip install cx_Oracle

# For testing and development
pip install pytest pytest-cov
```

### 系统要求
- Python 3.7 或更高版本
- 核心查询生成不依赖于外部依赖项
- 实际查询执行时需要数据库驱动程序

## 支持的数据库系统
- PostgreSQL
- MySQL
- SQLite
- Microsoft SQL Server
- Oracle Database
- MariaDB

## 核心功能

### 1. 查询生成
- **SELECT 查询**：简单和复杂的数据检索
- **JOIN 操作**：INNER、LEFT、RIGHT、FULL OUTER、CROSS
- **聚合操作**：GROUP BY、HAVING、聚合函数
- **子查询**：相关子查询和非相关子查询
- **CTE（公共表表达式）**：WITH 子句
- **窗口函数**：OVER、PARTITION BY、ROW_NUMBER、RANK
- **INSERT/UPDATE/DELETE**：数据操作查询
- **DDL**：CREATE、ALTER、DROP 语句

### 2. 查询优化
- 索引使用建议
- 查询执行计划分析
- 性能优化建议
- 避免 N+1 查询问题

### 3. 安全特性
- 防止 SQL 注入
- 参数化查询生成
- 输入验证模式
- 基于角色的访问控制模式

## 使用说明

### 基本查询生成
在生成 SQL 查询时，请按照以下步骤操作：
1. **理解请求**
   - 解析自然语言输入
   - 确定所需的表
   - 确定连接条件
   - 提取过滤条件

2. **生成基础查询**
   ```sql
   -- Example structure
   SELECT 
       column1,
       column2,
       aggregate_function(column3) AS alias
   FROM 
       table1
   JOIN 
       table2 ON table1.id = table2.foreign_id
   WHERE 
       condition1 = value1
       AND condition2 > value2
   GROUP BY 
       column1, column2
   HAVING 
       aggregate_condition
   ORDER BY 
       column1 DESC
   LIMIT 100;
   ```

3. **应用安全措施**
   - 使用参数化查询
   - 验证所有输入
   - 转义特殊字符

### 查询模式

#### 模式 1：简单的 SELECT 查询
```sql
-- Natural language: "Get all users who registered after January 1, 2024"
SELECT 
    id,
    username,
    email,
    registration_date
FROM 
    users
WHERE 
    registration_date > $1  -- Parameterized
ORDER BY 
    registration_date DESC;
```

#### 模式 2：带聚合操作的 JOIN 查询
```sql
-- Natural language: "Show total orders by customer in 2024"
SELECT 
    c.customer_name,
    c.email,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent
FROM 
    customers c
INNER JOIN 
    orders o ON c.customer_id = o.customer_id
WHERE 
    EXTRACT(YEAR FROM o.order_date) = $1
GROUP BY 
    c.customer_id,
    c.customer_name,
    c.email
HAVING 
    COUNT(o.order_id) > 5
ORDER BY 
    total_spent DESC;
```

#### 模式 3：子查询
```sql
-- Natural language: "Find products with above-average prices"
SELECT 
    product_name,
    price,
    category
FROM 
    products
WHERE 
    price > (
        SELECT AVG(price)
        FROM products
    )
ORDER BY 
    price DESC;
```

#### 模式 4：CTE（公共表表达式）
```sql
-- Natural language: "Get top 3 products per category by sales"
WITH product_sales AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category_id,
        c.category_name,
        SUM(oi.quantity * oi.unit_price) AS total_sales,
        ROW_NUMBER() OVER (
            PARTITION BY p.category_id 
            ORDER BY SUM(oi.quantity * oi.unit_price) DESC
        ) AS rank_in_category
    FROM 
        products p
    JOIN 
        order_items oi ON p.product_id = oi.product_id
    JOIN 
        categories c ON p.category_id = c.category_id
    GROUP BY 
        p.product_id,
        p.product_name,
        p.category_id,
        c.category_name
)
SELECT 
    category_name,
    product_name,
    total_sales,
    rank_in_category
FROM 
    product_sales
WHERE 
    rank_in_category <= 3
ORDER BY 
    category_name,
    rank_in_category;
```

#### 模式 5：窗口函数
```sql
-- Natural language: "Show running total of sales per day"
SELECT 
    sale_date,
    daily_total,
    SUM(daily_total) OVER (
        ORDER BY sale_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    AVG(daily_total) OVER (
        ORDER BY sale_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_average_7days
FROM (
    SELECT 
        DATE(order_date) AS sale_date,
        SUM(total_amount) AS daily_total
    FROM 
        orders
    GROUP BY 
        DATE(order_date)
) daily_sales
ORDER BY 
    sale_date;
```

## 最佳实践

### 1. 查询结构
- 始终使用明确的列名（避免使用 SELECT *）
- 使用有意义的表别名
- 通过缩进提高可读性
- 为复杂逻辑添加注释

### 2. 性能
- 创建适当的索引
- 尽可能避免使用 SELECT DISTINCT（改用 GROUP BY）
- 对于大型数据集，使用 EXISTS 而不是 IN
- 在适当的情况下限制结果集大小
- 使用 EXPLAIN 分析查询计划

### 3. 安全性（至关重要）
#### 3.1 强制性安全规则
**这些规则不可协商，必须始终遵守：**
1. **切勿将用户输入拼接到 SQL 语句中**
   ```python
   # WRONG - CRITICAL SECURITY VULNERABILITY
   query = f"SELECT * FROM users WHERE username = '{user_input}'"
   
   # CORRECT - Always use parameters
   query = "SELECT * FROM users WHERE username = %s"
   cursor.execute(query, (user_input,))
   ```

2. **所有值都必须参数化**
   - 即使是看似“安全”的值（如数字）
   - 即使来自“可信”来源的值
   - 包括内部应用程序的值
   - 无例外

3. **验证和清理所有输入**
   ```python
   # Whitelist validation
   VALID_STATUSES = ['active', 'inactive', 'pending']
   if status not in VALID_STATUSES:
       raise ValueError("Invalid status")
   
   # Type validation
   if not isinstance(user_id, int):
       raise TypeError("user_id must be integer")
   
   # Length validation
   if len(username) > 50:
       raise ValueError("username too long")
   ```

4. **正确转义动态标识符**
   ```python
   from psycopg2 import sql
   
   # For table/column names that must be dynamic
   query = sql.SQL("SELECT * FROM {} WHERE id = %s").format(
       sql.Identifier(table_name)
   )
   cursor.execute(query, (user_id,))
   ```

#### 3.2 输入验证框架
```python
import re
from typing import Any, List, Optional

class SQLInputValidator:
    """Comprehensive input validation for SQL queries"""
    
    @staticmethod
    def validate_identifier(identifier: str, max_length: int = 63) -> str:
        """Validate table/column names"""
        # Check length
        if len(identifier) > max_length:
            raise ValueError(f"Identifier too long: {len(identifier)} > {max_length}")
        
        # Only alphanumeric and underscore
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
            raise ValueError(f"Invalid identifier: {identifier}")
        
        # Prevent SQL keywords as identifiers
        SQL_KEYWORDS = {
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE',
            'ALTER', 'TRUNCATE', 'UNION', 'JOIN', 'WHERE', 'FROM'
        }
        if identifier.upper() in SQL_KEYWORDS:
            raise ValueError(f"SQL keyword not allowed: {identifier}")
        
        return identifier
    
    @staticmethod
    def validate_integer(value: Any, min_val: Optional[int] = None, 
                        max_val: Optional[int] = None) -> int:
        """Validate integer values"""
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid integer: {value}")
        
        if min_val is not None and int_value < min_val:
            raise ValueError(f"Value {int_value} below minimum {min_val}")
        
        if max_val is not None and int_value > max_val:
            raise ValueError(f"Value {int_value} above maximum {max_val}")
        
        return int_value
    
    @staticmethod
    def validate_string(value: str, max_length: int = 255, 
                       allow_empty: bool = False) -> str:
        """Validate string values"""
        if not isinstance(value, str):
            raise TypeError("Value must be string")
        
        if not allow_empty and len(value) == 0:
            raise ValueError("Empty string not allowed")
        
        if len(value) > max_length:
            raise ValueError(f"String too long: {len(value)} > {max_length}")
        
        # Check for null bytes
        if '\x00' in value:
            raise ValueError("Null bytes not allowed in string")
        
        return value
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email format"""
        email = SQLInputValidator.validate_string(email, max_length=254)
        
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError(f"Invalid email format: {email}")
        
        return email
    
    @staticmethod
    def validate_date(date_str: str) -> str:
        """Validate date format (YYYY-MM-DD)"""
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            raise ValueError(f"Invalid date format: {date_str}")
        
        return date_str
    
    @staticmethod
    def validate_enum(value: str, allowed_values: List[str]) -> str:
        """Validate value against whitelist"""
        if value not in allowed_values:
            raise ValueError(f"Invalid value: {value}. Allowed: {allowed_values}")
        
        return value
```

#### 3.3 防止 SQL 注入攻击的方法
```python
# Detect common SQL injection patterns
INJECTION_PATTERNS = [
    r"('|(\\')|(--)|(\#)|(%23)|(;))",  # Basic SQL injection
    r"((\%27)|(\'))",                   # Single quote variations
    r"(union.*select)",                 # UNION-based injection
    r"(insert.*into)",                  # INSERT injection
    r"(update.*set)",                   # UPDATE injection
    r"(delete.*from)",                  # DELETE injection
    r"(drop.*table)",                   # DROP TABLE
    r"(exec(\s|\+)+(s|x)p\w+)",        # Stored procedure execution
    r"(script.*>)",                     # XSS attempts
]

def detect_injection_attempt(value: str) -> bool:
    """Detect potential SQL injection attempts"""
    value_lower = value.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, value_lower):
            return True
    return False
```

#### 3.4 安全查询构建器
```python
class SecureQueryBuilder:
    """Build SQL queries with mandatory security checks"""
    
    def __init__(self, db_type: DatabaseType):
        self.db_type = db_type
        self.validator = SQLInputValidator()
        self.params = []
    
    def build_select(self, table: str, columns: List[str], 
                    conditions: dict) -> tuple:
        """Build SELECT query with validation"""
        # Validate table name
        table = self.validator.validate_identifier(table)
        
        # Validate columns
        validated_columns = [
            self.validator.validate_identifier(col) 
            for col in columns
        ]
        
        # Build query
        query = f"SELECT {', '.join(validated_columns)} FROM {table}"
        
        # Add WHERE clause with parameters
        if conditions:
            where_parts = []
            for key, value in conditions.items():
                key = self.validator.validate_identifier(key)
                where_parts.append(f"{key} = %s")
                self.params.append(value)
            
            query += " WHERE " + " AND ".join(where_parts)
        
        return query, tuple(self.params)
```

#### 3.5 数据库连接安全
```python
import ssl
from typing import Optional

class SecureConnection:
    """Secure database connection configuration"""
    
    @staticmethod
    def get_postgresql_ssl_config() -> dict:
        """PostgreSQL SSL configuration"""
        return {
            'sslmode': 'require',  # or 'verify-full' for production
            'sslrootcert': '/path/to/ca-cert.pem',
            'sslcert': '/path/to/client-cert.pem',
            'sslkey': '/path/to/client-key.pem'
        }
    
    @staticmethod
    def get_connection_timeout() -> dict:
        """Connection timeout settings"""
        return {
            'connect_timeout': 10,
            'command_timeout': 30,
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5
        }
    
    @staticmethod
    def create_secure_connection(database_url: str) -> Any:
        """Create connection with security settings"""
        import psycopg2
        
        # Parse connection string securely
        # NEVER log the connection string (contains credentials)
        
        conn = psycopg2.connect(
            database_url,
            **SecureConnection.get_postgresql_ssl_config(),
            **SecureConnection.get_connection_timeout()
        )
        
        # Set session security parameters
        cursor = conn.cursor()
        cursor.execute("SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        cursor.execute("SET statement_timeout = 30000")  # 30 seconds
        cursor.close()
        
        return conn
```

#### 3.6 速率限制
```python
import time
from collections import defaultdict
from threading import Lock

class RateLimiter:
    """Prevent query flooding attacks"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed"""
        with self.lock:
            now = time.time()
            window_start = now - self.window_seconds
            
            # Clean old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]
            
            # Check limit
            if len(self.requests[identifier]) >= self.max_requests:
                return False
            
            # Add new request
            self.requests[identifier].append(now)
            return True
```

#### 3.7 审计日志记录
```python
import logging
import json
from datetime import datetime
from typing import Any, Dict

class SecurityAuditLogger:
    """Log all database operations for security auditing"""
    
    def __init__(self, log_file: str = '/var/log/sql_audit.log'):
        self.logger = logging.getLogger('sql_audit')
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_query(self, query: str, params: tuple, user_id: str,
                  ip_address: str, result_count: int = None):
        """Log query execution"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'ip_address': ip_address,
            'query': query,
            'param_count': len(params),
            'result_count': result_count
        }
        self.logger.info(json.dumps(log_entry))
    
    def log_security_event(self, event_type: str, details: Dict[str, Any],
                          severity: str = 'WARNING'):
        """Log security events"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'severity': severity,
            'details': details
        }
        
        if severity == 'CRITICAL':
            self.logger.critical(json.dumps(log_entry))
        elif severity == 'ERROR':
            self.logger.error(json.dumps(log_entry))
        else:
            self.logger.warning(json.dumps(log_entry))
```

#### 3.8 预编译语句池
```python
from typing import Dict, Any
import hashlib

class PreparedStatementPool:
    """Reuse prepared statements for better performance and security"""
    
    def __init__(self, connection):
        self.connection = connection
        self.statements: Dict[str, Any] = {}
    
    def get_statement(self, query: str):
        """Get or create prepared statement"""
        # Create hash of query for lookup
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]
        
        if query_hash not in self.statements:
            # Create new prepared statement
            cursor = self.connection.cursor()
            statement_name = f"stmt_{query_hash}"
            cursor.execute(f"PREPARE {statement_name} AS {query}")
            self.statements[query_hash] = statement_name
        
        return self.statements[query_hash]
    
    def execute(self, query: str, params: tuple):
        """Execute using prepared statement"""
        stmt_name = self.get_statement(query)
        cursor = self.connection.cursor()
        param_list = ', '.join(['%s'] * len(params))
        cursor.execute(f"EXECUTE {stmt_name}({param_list})", params)
        return cursor
```

### 4. 参数化示例

**PostgreSQL/Python (psycopg2)**
```python
# CORRECT - Parameterized
cursor.execute(
    "SELECT * FROM users WHERE email = %s AND status = %s",
    (user_email, status)
)

# WRONG - String concatenation (SQL injection risk)
cursor.execute(
    f"SELECT * FROM users WHERE email = '{user_email}'"
)
```

**MySQL/Python (mysql-connector)**
```python
# CORRECT
cursor.execute(
    "SELECT * FROM products WHERE price > %s",
    (min_price,)
)
```

**SQLite/Python**
```python
# CORRECT
cursor.execute(
    "SELECT * FROM orders WHERE order_date > ?",
    (start_date,)
)
```

**Node.js (PostgreSQL)**
```javascript
// CORRECT
const result = await client.query(
    'SELECT * FROM users WHERE id = $1',
    [userId]
);
```

### 5. 数据库特定的语法

**PostgreSQL**
- 使用 `$1, $2, $3` 作为参数
- 支持高级功能：JSONB、数组、全文搜索
- 使用 `RETURNING` 子句进行 INSERT/UPDATE/DELETE 操作
- 使用 ILIKE 进行区分大小写的文本搜索

**MySQL**
- 使用 `?` 作为参数
- LIMIT 语法：`LIMIT offset, count`
- 对于包含空格的标识符，使用反引号
- 日期函数：DATE_FORMAT, CURDATE()

**SQL Server**
- 使用 `@param1, @param2` 作为参数
- 使用 TOP 而不是 LIMIT
- 使用方括号作为标识符
- 日期函数：GETDATE(), DATEADD()

**SQLite**
- 使用 `?` 作为参数
- 对 ALTER TABLE 的支持有限
- 不支持 RIGHT JOIN 或 FULL OUTER JOIN
- 日期函数以字符串形式表示

## 错误处理
在生成查询时，应包含错误处理建议：
```python
import psycopg2
from psycopg2 import sql

try:
    cursor.execute(
        sql.SQL("SELECT * FROM {} WHERE id = %s").format(
            sql.Identifier('users')
        ),
        (user_id,)
    )
    results = cursor.fetchall()
except psycopg2.Error as e:
    print(f"Database error: {e}")
    # Log error, return appropriate response
finally:
    cursor.close()
```

## 查询验证检查清单
在提供查询之前，请验证：
- [ ] 所有的表名和列名是否有效
- [ ] JOIN 条件是否正确
- [ ] WHERE 子句的逻辑是否准确
- [ ] 是否使用了参数（而不是字符串拼接）
- [ ] 是否存在或建议使用适当的索引
- [ ] 查询是否针对预期的数据集大小进行了优化
- [ ] 如果需要，结果集是否得到了适当的限制
- [ ] 实现代码中是否包含了错误处理

## 响应格式
在响应查询请求时，请提供：
1. **SQL 查询**（格式正确且带有注释）
2. **查询的功能说明**
3. **需要传递的参数**
4. **预期结果的结构**
5. **性能说明**（如适用）
6. **安全警告**（如适用）
7. **所需语言的实现示例**

## 示例响应结构
```markdown
### SQL Query
```sql
-- 获取活跃用户及其订单数量
SELECT 
    u.user_id,
    u.username,
    u.email,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS lifetime_value
FROM 
    users u
LEFT JOIN 
    orders o ON u.user_id = o.user_id
WHERE 
    u.status = $1
    AND u.created_at >= $2
GROUP BY 
    u.user_id,
    u.username,
    u.email
HAVING 
    COUNT(o.order_id) >= $3
ORDER BY 
    lifetime_value DESC
LIMIT $4;
```

### Parameters
- `$1`: status (string, e.g., 'active')
- `$2`: created_at (date, e.g., '2024-01-01')
- `$3`: min_orders (integer, e.g., 5)
- `$4`: limit (integer, e.g., 100)

### Explanation
This query retrieves active users who joined after a specified date and have placed a minimum number of orders. It calculates their total order count and lifetime value, sorted by highest spending customers first.

### Expected Result
| user_id | username | email | order_count | lifetime_value |
|---------|----------|-------|-------------|----------------|
| 123 | john_doe | john@example.com | 15 | 2500.00 |

### Performance Notes
- Ensure index on `users.status` and `users.created_at`
- Ensure index on `orders.user_id`
- For large datasets, consider pagination

### Implementation Example (Python/psycopg2)
```python
cursor.execute(query, ('active', '2024-01-01', 5, 100))
results = cursor.fetchall()
```
```

## 高级主题

### 1. 查询优化技术
- 使用 EXPLAIN ANALYZE 理解查询计划
- 创建覆盖索引
- 对大型表进行分区
- 为复杂的聚合操作使用物化视图
- 实现查询结果缓存

### 2. 复杂场景
- 用于分层数据的递归 CTE
- 数据透视/反透视操作
- 全文搜索
- 地理空间查询
- 时间序列分析

### 3. 迁移支持
- 生成数据迁移所需的查询
- 模式比较查询
- 数据验证查询
- 备份和恢复脚本

## 测试建议
始终建议使用以下方法测试生成的查询：
1. 首先使用小型数据集进行测试
2. 使用 EXPLAIN 或 EXPLAIN ANALYZE
3. 测试各种边缘情况（空值、空集合）
4. 进行性能基准测试
5. 使用安全扫描工具

## 常见陷阱及避免方法

1. **N+1 查询问题**：使用 JOIN 替代多个查询
2. **SELECT ***：明确指定所需的列**
3. **缺少索引**：建议在过滤/连接列上创建索引
4. **笛卡尔积**：确保连接条件正确
5. **隐式类型转换**：在需要时显式进行类型转换
6. **时区问题**：始终使用考虑时区的时间戳

## 集成示例

### REST API
```python
from flask import Flask, request, jsonify
import psycopg2

@app.route('/api/users', methods=['GET'])
def get_users():
    status = request.args.get('status', 'active')
    
    # Validate input
    if status not in ['active', 'inactive', 'suspended']:
        return jsonify({'error': 'Invalid status'}), 400
    
    try:
        cursor.execute(
            "SELECT id, username, email FROM users WHERE status = %s",
            (status,)
        )
        users = cursor.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### GraphQL 解析器
```javascript
const resolvers = {
  Query: {
    users: async (_, { status, limit }, { db }) => {
      const result = await db.query(
        'SELECT * FROM users WHERE status = $1 LIMIT $2',
        [status, limit]
      );
      return result.rows;
    }
  }
};
```

## 结论
该技能提供了全面的 SQL 查询生成功能，重点关注安全性、性能和最佳实践。始终优先使用参数化查询，并为生成的 SQL 提供清晰的文档。