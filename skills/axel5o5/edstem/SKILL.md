---
name: edstem
description: 用于获取、同步并整理任何课程或机构的 EdStem 讨论主题。适用于查看新的 EdStem 帖子、同步课程讨论论坛的内容、审阅学生/教师的问答，或者当用户需要查看 EdStem 讨论、回顾课程讨论内容或保持对课堂论坛的更新时使用。
---
# EdStem

该工具可以从任何使用 EdStem 的课程或机构中获取并整理讨论帖子，并自动区分教师和学生的帖子。

## 快速入门

**获取任意课程的最新帖子：**

```bash
cd /home/axel/.openclaw/workspace/skills/edstem/scripts
python3 fetch-edstem.py <course_id> [output_dir] [--course-name "Course Name"]
```

**示例：**
```bash
# Fetch to default directory (./edstem-<course_id>)
python3 fetch-edstem.py 92041

# Fetch to specific directory
python3 fetch-edstem.py 92041 ./machine-learning

# Specify course name for clearer output
python3 fetch-edstem.py 92041 --course-name "Machine Learning"

# Combine directory and course name
python3 fetch-edstem.py 92041 ./ml-course --course-name "Machine Learning"

# Fetch more threads (default is 10)
python3 fetch-edstem.py 92041 --limit 25
```

## 查找您的课程 ID

要找到您的 EdStem 课程 ID，请按照以下步骤操作：
1. 登录 EdStem 并导航到您的课程页面。
2. 查看 URL：`https://edstem.org/us/courses/<course_id>/`
3. URL 中的数字就是您的课程 ID。

或者，您也可以使用 API 来列出您的课程：
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://us.edstem.org/api/user | jq '.courses[] | {id: .course.id, name: .course.name}'
```

## 获取的数据内容

对于每个课程：
- **threads.json**：包含元数据的完整帖子列表。
- **thread-XXX.md**：以 markdown 格式显示的单个帖子：
  - 帖子标题、分类、时间戳
  - 原始帖子内容
  - 所有的回答和评论
  - 每条帖子都会带有 `[STAFF]** 或 `[STUDENT]** 标签，用于区分教师和学生的帖子。

## 主要特性：
- **不受机构限制**：适用于任何使用 EdStem 的学校。
- **自动区分教师和学生的帖子**：能清晰地标记出教师和学生的帖子。
- **结构化输出**：采用 markdown 格式，便于阅读和搜索。
- **基于 API**：使用 EdStem 的官方 API（无需爬取数据）。
- **灵活的输出方式**：您可以自定义输出目录和文件组织结构。

## 认证

该工具使用存储在 Python 脚本中的 bearer token 进行认证。若要使用您的个人账户，请按照以下步骤操作：
1. 在浏览器中登录 EdStem。
2. 打开开发者工具 → 网络选项卡。
3. 重新加载任意 EdStem 页面。
4. 找到 API 请求，复制 `Authorization: Bearer ...` 标签中的 token。
5. 更新 `scripts/fetch-edstem.py` 文件中的 `ED_TOKEN` 变量。
**当前 token 的位置：`scripts/fetch-edstem.py` 文件的第 20 行**。

如果 API 请求失败（提示 401 Unauthorized），则可能是 token 已过期，需要重新获取。

## 脚本

### fetch-edstem.py（推荐使用）

这是一个功能齐全的 Python 脚本，支持 markdown 格式和教师/学生帖子的区分。

**使用方法：**
```bash
python3 scripts/fetch-edstem.py <course_id> [output_dir] [options]
```

**参数说明：**
- `output_dir`：帖子的保存路径（默认值：`./edstem-<course_id>`。
- `--course-name NAME`：课程的显示名称。
- `--limit N`：要获取的帖子数量（默认值：10）。

**脚本功能：**
- 获取帖子的元数据和详细信息。
- 采用完整的 markdown 格式显示帖子内容（包括回答和评论）。
- 自动检测帖子的作者角色。
- 生成帖子列表的 JSON 缓存文件。
- 自动创建输出目录。

### fetch-edstem.sh（轻量级替代方案）

这是一个使用 Bash 和 curl 的脚本，用于获取原始 JSON 数据，无需额外依赖。

**使用方法：**
```bash
bash scripts/fetch-edstem.sh <course_id> [output_dir]
```

**输出结果：**
- 每个帖子都会生成一个原始 JSON 文件。
- 需要手动对输出文件进行格式化或后处理。

## 常见使用场景：
- **检查新帖子**：```bash
python3 scripts/fetch-edstem.py 92041 ~/courses/ml-spring-2025
```
- **同步多个课程**：```bash
# Create a simple sync script
for course in "92041:machine-learning" "94832:advanced-rl"; do
    IFS=':' read -r id name <<< "$course"
    python3 scripts/fetch-edstem.py $id ~/courses/$name --course-name "$name"
done
```
- **查看近期活动**：获取帖子后，可以查看对应的 markdown 文件：```bash
ls -lt ./edstem-92041/*.md | head
cat ./edstem-92041/thread-001.md
```
- **跨帖子搜索**：```bash
grep -r "gradient descent" ./edstem-92041/*.md
```

## 输出文件结构

每个 markdown 文件包含以下内容：
- 帖子的元数据（编号、标题、分类、时间戳）。
- 帖子的原始内容及作者角色。
- 所有的回答（按角色分类显示）。
- 所有的评论（也按角色分类显示）。

## 集成示例：
- **与大型语言模型（LLM）集成**：```bash
# Fetch threads and analyze with your agent
python3 fetch-edstem.py 92041 ./course-data
# Then: "Summarize the most common questions in ./course-data/"
```
- **自动化监控**：```bash
# Add to cron for daily sync
0 9 * * * cd /path/to/skills/edstem/scripts && python3 fetch-edstem.py 92041 ~/courses/ml
```
- **自定义文件组织结构**：```bash
# Organize by semester and institution
python3 fetch-edstem.py 92041 ~/school/stanford/2025-spring/cs229
python3 fetch-edstem.py 94832 ~/school/mit/2025-spring/6.7920
```

## 故障排除：
- **401 Unauthorized**：Token 过期，请重新认证并更新 `ED_TOKEN`。
- **课程未找到**：请确认课程 ID 是否正确，以及您的账户是否具有访问权限。
- **帖子为空**：请检查该课程是否有讨论帖子，并确认您已注册该课程。
- **API 请求限制**：EdStem 可能会对 API 请求进行速率限制。如有需要，可以在请求之间添加延迟。

## 贡献方式

该工具是开源的，设计上不依赖于特定机构。欢迎提出改进建议：
- 提高内容解析效率（EdStem 使用基于 XML 的文档格式）。
- 支持按类别或日期范围筛选帖子。
- 实现增量同步（仅获取新帖子）。
- 支持将数据导出为其他格式（如 JSON、HTML 等）。

## 版本历史：
- **1.1.0**：实现不受机构限制的功能，并增加了参数配置选项。
- **1.0.0**：初始版本。