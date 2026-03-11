---
name: nccuoj
description: "在 NCCUOJ（https://nccuoj.ebg.tw）上解决编程竞赛题目。适用场景包括：解答在线编程题目、阅读题目描述、使用 C/C++/Python 编写解决方案、提交代码以及查看提交结果。"
argument-hint: "Problem ID or URL (e.g. '1001' or 'https://nccuoj.ebg.tw/problem/1001')"
---
# NCCUOJ 问题解决

在 [NCCUOJ](https://nccuoj.ebg.tw) 上解决编程竞赛题目。NCCUOJ 是南京航空航天大学（NCCU）计算机科学专业的在线Judge平台。

## 使用场景

- 阅读 NCCUOJ 上的问题描述
- 为特定问题编写解决方案
- 提交代码并查看结果
- 调试错误的答案或超时的情况
- 解决竞赛题目

## 目录结构

所有生成的文件都存储在工作空间根目录下的 `.nccuoj/` 目录中：

```
.nccuoj/
├── cookies.txt                                  # Session cookies (auto-managed)
└── solution/
    ├── public/<problem_id>/                      # Public problem solutions
    │   ├── problem.md                            # Problem statement
    │   └── solution.cpp / solution.py / ...      # Solution code
    └── contest/<contest_id>/<problem_id>/        # Contest problem solutions
        ├── problem.md
        └── solution.cpp / solution.py / ...
```

**在编写解决方案代码时，请务必将文件放在正确的目录中。** 脚本的 `--save` 标志和 `get_solution_dir()` 辅助函数会自动处理目录的创建。

## CSRF 令牌（重要）

所有 NCCUOJ API 请求都需要一个 CSRF 令牌。提供的脚本会自动处理这一点（通过 `GET /api/profile` 在初始化时获取）。如果需要手动发送请求，请参阅 [./references/api.md](./references/api.md) 以获取详细信息。

## 脚本

使用这些脚本来与 NCCUOJ 进行交互。它们会自动处理 CSRF 令牌和会话管理。

| 脚本 | 功能         |
|--------|------------|
| [get_problem.py](./scripts/get_problem.py) | 以 Markdown 格式获取问题描述（支持 `--username`/`--password`、`--contest`、`--raw` 参数） |
| [submit.py](./scripts/submit.py) | 提交代码（需要 `--username` / `--password` 命令行参数） |
| [check_result.py](./scripts/check_result.py) | 检查提交结果，可选参数 `--poll` |

所有脚本仅使用 Python 标准库（无需安装 pip）。

脚本位于本技能的 `./scripts/` 目录中。在下面的示例中，`$SCRIPTS` 表示该目录的绝对路径。在运行命令之前，请将其相对于此 SKILL.md 文件进行解析。

## 模式 A：公开问题解决

### 1. 获取问题

运行 [get_problem.py](./scripts/get_problem.py) 来获取问题。**如果问题需要登录（例如显示“请先登录”），请向用户索取他们的凭据，并传递 `--username`/`--password` 参数。**

```bash
# Public (no login)
python $SCRIPTS/get_problem.py <problem_id>

# With login
python $SCRIPTS/get_problem.py <problem_id> --username <username> --password <password>
```

或者，如果给定一个 URL（如 `https://nccuoj.ebg.tw/problem/1001`），提取 `1001` 并将其作为参数传递。

输出结果为格式化的 Markdown，包含：标题、元数据（内部 ID、难度、时间/内存限制、标签）、描述、输入/输出格式、示例测试用例、提示、允许使用的语言以及统计信息。所有 URL 编码的 HTML 字段都会被自动解码并转换为 Markdown 格式。

使用 `--raw` 可以获取原始的 JSON 数据。

### 2. 分析问题

- 从 `input_description` 和 `output_description` 中确定输入/输出格式
- 研究示例用例
- 确定约束条件（时间/内存限制）
- 确定所需的算法或数据结构

### 3. 编写解决方案

将解决方案文件保存在正确的目录中：
- **公开问题**：`.nccuoj/solution/public/<problem_id>/solution.cpp`（或 `.py`、`.java` 等）
- **竞赛问题**：`.nccuoj/solution/contest/<contest_id>/<problem_id>/solution.cpp`

支持的语言包括：

| 语言       | API 名称        | 备注                |
|------------|---------------|----------------------|
| C          | `C`           | 使用 GCC、C17 编译器           |
| C++        | `C++`         | 使用 GCC、C++20 编译器         |
| Python     | `Python3`     | 使用 Python 3.12             |
| Java       | `Java`        | 使用 Temurin 21 运行时环境       |
| Go         | `Golang`      | 使用 Go 1.22             |
| JavaScript | `JavaScript`  | 使用 Node.js 20                |

**默认使用 C++ 语言，除非用户另有指定。**

#### C/C++ 模板

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // solution
    return 0;
}
```

#### Python 模板

```python
import sys
input = sys.stdin.readline

def solve():
    # solution
    pass

solve()
```

### 4. 本地测试

在提交之前，使用示例用例验证解决方案。使用每个示例输入运行代码，并与预期输出进行比较。

### 5. 提交（可选）

**在提交之前，如果用户尚未提供他们的 NCCUOJ 用户名和密码，请向他们索取这些信息。** 然后将凭据作为命令行参数传递。

```bash
# Submit (problem_id is the internal numeric ID from the problem JSON's "id" field)
python $SCRIPTS/submit.py <problem_internal_id> "C++" .nccuoj/solution/public/<problem_id>/solution.cpp --username <username> --password <password>

# Check result (with --poll to wait for judging)
python $SCRIPTS/check_result.py <submission_id> --username <username> --password <password> --poll
```

结果代码：`-2`（编译错误），`-1`（答案错误），`0`（接受），`1`（超时），`2`（内存限制超出），`3`（运行时错误），`4`（系统错误），`6`（待审），`7`（正在评审），`8`（部分接受）。

### 6. 如有需要，进行调试

如果提交未被接受：
- **答案错误**：重新检查边界情况、数值错误、输出格式等问题
- **超时**：优化算法复杂度、减少 I/O 开销
- **运行时错误**：检查数组边界、除以零的情况、栈溢出等问题
- **编译错误**：查看提交响应中的错误信息
- **内存限制超出**：减小数据结构的大小、避免不必要的数据复制

## 模式 B：竞赛问题解决

竞赛模式的操作与公开模式相同，但所有 API 调用都需要 `contest_id` 参数。

### 1. 获取竞赛问题

运行 [get_problem.py](./scripts/get_problem.py) 并添加 `--contest` 参数。**竞赛问题始终需要登录。**

```bash
python $SCRIPTS/get_problem.py <problem_id> --contest <contest_id> --username <username> --password <password>
```

响应格式与公开问题相同。

### 2–4. 分析、编写、测试

与模式 A 的步骤 2–4 相同。

### 5. 向竞赛系统提交

**在提交之前，如果用户尚未提供他们的 NCCUOJ 用户名和密码，请向他们索取这些信息。**

```bash
python $SCRIPTS/submit.py <problem_internal_id> "C++" .nccuoj/solution/contest/<contest_id>/<problem_id>/solution.cpp --username <username> --password <password> --contest <contest_id>

# Check result
python $SCRIPTS/check_result.py <submission_id> --username <username> --password <password> --poll
```

### 7. 如有需要，进行调试

与模式 A 的步骤 6 相同。注意：在竞赛进行期间，竞赛提交内容**不能被共享**。

## API 参考

请参阅 [./references/api.md](./references/api.md) 以获取完整的 API 端点文档。