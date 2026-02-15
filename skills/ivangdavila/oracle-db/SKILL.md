---
name: Oracle DB
description: 编写符合正确语法的 Oracle SQL 和 PL/SQL 代码，同时提供相关提示和性能优化建议。
metadata: {"clawdbot":{"emoji":"🔴","requires":{"anyBins":["sqlplus","sql"]},"os":["linux","darwin","win32"]}}
---

## 语法差异

- 使用 `ROWNUM` 来限制查询结果的行数：`WHERE ROWNUM <= 10`；12c+ 版本支持 `FETCH FIRST 10 ROWS ONLY`。
- 使用 `DUAL` 表来生成表达式：`SELECT sysdate FROM dual`。
- 使用 `VARCHAR2` 而不是 `VARCHAR` —— `VARCHAR` 是保留关键字，`VARCHAR2` 是标准类型。
- 字符串连接使用 `||`，而不是 `CONCAT`（用于多个值）。
- 空字符串等于 `NULL`：`'' IS NULL` 的判断结果为 `true`，这与其他数据库的逻辑不同。

## 分页

- `ROWNUM` 应在 `ORDER BY` 之前分配：需要使用子查询来实现分页：`SELECT * FROM (SELECT ... ORDER BY x) WHERE ROWNUM <= 10`。
- 使用偏移量时需要嵌套子查询：`SELECT * FROM (SELECT a.*, ROWNUM rn FROM (...) a WHERE ROWNUM <= 20) WHERE rn > 10`。
- 12c+ 版本支持更简洁的分页语法：`OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY`，在支持的情况下应优先使用。

## NULL 处理

- 使用 `NVL(col, default)` 来替换 `NULL` 值，比 `COALESCE` 更高效（尤其是处理两个参数时）。
- 使用 `NVL2(col, if_not_null, if_null)` 进行条件判断，这是 Oracle 的常见用法。
- 空字符串被视为 `NULL`：`LENGTH('')` 的返回值为 `NULL`，而不是 `0`。
- `NULLIF(a, b)` 如果 `a` 和 `b` 相等则返回 `NULL`，有助于避免除以零的错误。

## 日期处理

- 使用 `SYSDATE` 获取当前日期时间，无需加括号。
- 使用 `TO_DATE('2024-01-15', 'YYYY-MM-DD')` 将字符串转换为日期格式。
- 使用 `TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS')` 将日期转换为字符串。
- 日期运算：`SYSDATE + 1` 表示明天，`SYSDATE + 1/24` 表示一小时后。

## 序列

- 创建序列：`CREATE SEQUENCE seq_name START WITH 1 INCREMENT BY 1`。
- 获取序列的下一个值：`seq_name.NEXTVAL` 或 `SELECT seq_name.NEXTVAL FROM dual`。
- 获取当前序列值：`seq_name.CURRVAL`（仅在同一个会话中调用 `NEXTVAL` 之后有效）。
- 12c+ 版本支持自动生成序列 ID：`GENERATED ALWAYS AS IDENTITY`。

## 层次查询

- 使用 `CONNECT BY PRIOR child = parent` 进行树形遍历。
- 使用 `START WITH parent IS NULL` 来指定根节点。
- 使用 `LEVEL` 伪列来表示查询的深度：`WHERE LEVEL <= 3` 可以限制查询的深度。
- 使用 `SYS_CONNECT_BY_PATH(col, '/')` 来构建路径字符串。

## 绑定变量

- 始终使用绑定变量，因为字面量会导致每次查询时都需要重新解析。
- 在 PL/SQL 中使用 `:variable_name` 语法来定义绑定变量。
- 绑定变量对性能至关重要：字面量会填充共享内存池，可能导致性能瓶颈。
- 可以使用 `CURSOR_SHARING=FORCE` 作为临时解决方案，但不建议长期使用。

## 指示器（Hints）

- 使用 `/*+ INDEX(table idx_name) */` 强制使用指定索引。
- 使用 `/*+ FULL(table) */` 强制执行全表扫描。
- 使用 `/*+ PARALLEL(table, 4) */` 启用并行查询。
- 指示器通常放在 `SELECT` 关键字后面：`SELECT /*+ hint */`。

## PL/SQL 块

- 匿名块：使用 `BEGIN ... END;`，并在新行开始时使用 `/` 来执行块。
- 使用 `DBMS_OUTPUT.PUT_LINE()` 输出调试信息：需要先使用 `SET SERVEROUTPUT ON`。
- 异常处理：`EXCEPTION WHEN OTHERS THEN` —— 必须处理异常或记录异常信息。
- 使用 `EXECUTE IMMEDIATE 'sql string'` 来执行动态 SQL 语句，注意防止 SQL 注入攻击。

## 事务

- 默认情况下没有自动提交功能，必须手动使用 `COMMIT`。
- 使用 `SAVEPOINT name` 后再使用 `ROLLBACK TO name` 来部分回滚事务。
- DDL 操作会自动提交事务：`CREATE TABLE` 会提交所有未完成的事务。
- 使用 `SELECT FOR UPDATE WAIT 5` 可以等待 5 秒以获取锁，避免程序无限期挂起。

## 性能优化

- 使用 `EXPLAIN PLAN FOR sql; SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY)` 查看查询执行计划。
- 使用 `V$SQL` 和 `V$SESSION` 监控数据库性能（需要相应权限）。
- 避免使用 `SELECT *`，因为它会获取所有列（包括大型对象）。
- 当优化器选择错误的索引时，可以使用 `/*+ INDEX(t idx) */` 来指定索引。

## 常见错误

- 使用 `MINUS` 而不是 `EXCEPT` 来计算集合差集。
- `DECODE` 是 Oracle 特有的函数，为了跨平台兼容性应使用 `CASE` 语句。
- 隐式类型转换：`WHERE num_col = '123` 可以正常工作，但会阻止索引被使用。
- `ROWID` 是物理标识符，不要在不同事务之间存储或依赖它。