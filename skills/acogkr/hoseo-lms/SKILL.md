---
name: hoseo_lms
description: LMS数据聚合与报告工具，用于课程信息管理。
homepage: https://learn.hoseo.ac.kr
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] }
      }
  }
---
# hoseo_lms

这是一个专为Hoseo大学的学习管理系统（LMS）设计的数据聚合工具。该工具可以收集课程元数据、课程安排信息，并生成相应的报告。该工具不支持自动提交考勤记录或修改成绩。

---

## 概述

该工具包含三个独立的实用程序：

1. **数据聚合**：读取公开课程页面并生成JSON格式的报告。
2. **日程分析**：解析课程截止日期和活动安排。
3. **视频播放工具**：用户可控制视频播放过程，并实时查看播放进度。

所有操作均由用户发起，仅具有读取权限，并且数据会存储在本地。

---

## 模块

### scraper

该模块负责将课程数据聚合到结构化的JSON报告中。

```bash
python3 src/scraper.py
```

**输入**：用户凭据（仅用于身份验证）
**输出**：`~/.config/hoseo_lms/data.json`
**收集的数据**：
- 课程标题、ID和教授姓名
- 作业截止日期及提交状态
- 小测验截止日期
- 活动类型（视频、作业、小测验、讨论）
- 出勤记录和视频观看要求

**技术细节**：
- 使用HTTP请求获取公开课程页面
- 解析HTML结构（不依赖浏览器自动化）
- 以纯文本JSON格式存储数据，便于本地分析
- 仅具有读取权限（不会修改LMS中的数据）

### summary

该模块负责在终端界面显示聚合后的课程数据。

```bash
python3 src/summary.py
```

**输入**：之前生成的`data.json`文件
**输出**：
- 课程列表
- 未完成的作业
- 小测验安排
- 出勤状态

### auto_attend

该模块是一个视频播放工具，支持进度跟踪功能。

```bash
python3 src/auto_attend.py [选项]
```

**用途**：用户可以指定要播放的视频数量并进行播放。

**主要功能**：
- **用户控制**：用户可以指定要播放的视频数量（`--limit-lectures`参数）。
- **手动触发**：需要用户明确输入命令才能开始播放。
- **进度记录**：会记录播放进度和完成状态。
- **不自动提交数据**：不会自动提交考勤记录或修改成绩。
- **等待完成后再退出**：在播放完成前会等待用户确认。

**使用示例**：
- 播放所有课程中的3个视频：`python3 src/auto_attend.py --limit-lectures 3`
- 播放特定课程中的2个视频：`python3 src/auto_attend.py --course Database --limit-lectures 2`
- 播放第1至第8周中的5个视频：`python3 src/auto_attend.py --limit-lectures 5 --max-week 8`
- 使用用户名和密码播放视频：`python3 src/auto_attend.py --id 20231234 --pw password --limit-lectures 4`
- 开启详细日志：`python3 src/auto_attend.py --limit-lectures 3 --verbose`

**选项**：

| 参数 | 默认值 | 类型 | 说明 |
|------|---------|------|-------------|
| `--id` | credentials.json | 字符串 | 学生ID |
| `--pw` | credentials.json | 字符串 | 密码 |
| `--course` | all | 字符串 | 过滤课程名称 |
| `--limit-lectures` | 0 | 整数 | 要播放的视频数量（0表示全部） |
| `--max-week` | 15 | 整数 | 要扫描的最终周数 |
| `--lecture-timeout` | 3600 | 整数 | 每个视频的播放超时时间（秒） |
| `--headed` | false | 标志 | 是否显示浏览器窗口 |
| `--verbose` | false | 标志 | 是否开启详细日志 |

**操作细节**：
- 在浏览器中打开视频播放器（弹出窗口或新标签页）。
- 在页面中查找视频元素及其嵌套的iframe。
- 等待视频元数据（时长）加载完成后才开始播放。
- 播放时视频会自动静音，播放结束后会取消静音。
- 如果连续三次播放失败，会自动跳过当前视频。
- 在网络错误时最多尝试重新导航页面3次。
- 记录播放完成状态。
- 不会修改学生的注册信息或成绩。
- 仅记录播放日志，不提交考勤数据。

**示例输出**：
```
[14:30:45] 登录成功
[14:30:50] [Database101] 开始处理
[14:30:55] [Database101] 已观看：1/3
[14:35:20] [Database101] 已观看：2/3
[14:39:45] [Database101] 已观看：3/3
[14:39:50] 处理完成：共观看3个视频，尝试播放3次
[14:39:50] 所有任务已完成。
```

---

## 设置与配置

### 创建凭据文件

**步骤1**：创建目录
```bash
mkdir -p ~/.config/hoseo_lms
```

**步骤2**：使用终端创建`credentials.json`文件

#### 选项A（Linux/Mac）：
```bash
cat << 'EOF' > ~/.config/hoseo_lms/credentials.json
{
  "id": "YOUR_STUDENT_ID",
  "pw": "YOUR_PASSWORD"
}
EOF
```

**示例**：
```bash
cat << 'EOF' > ~/.config/hoseo_lms/credentials.json
{
  "id": "20231234",
  "pw": "mypassword123"
}
EOF
```

#### 选项B（Linux/Mac/Windows）：
```bash
echo '{"id":"YOUR_STUDENT_ID","pw":"YOUR_PASSWORD"}' > ~/.config/hoseo_lms/credentials.json
```

#### 选项C（Windows）：
```powershell
@"{
  "id": "YOUR_STUDENT_ID",
  "pw": "YOUR_PASSWORD"
}
"@ | Out-File -Encoding UTF8 "$env:USERPROFILE\.config\hoseo_lms\credentials.json"
```

#### 选项D（所有操作系统）：
1. 创建`~/.config/hoseo_lms/`目录。
2. 创建`credentials.json`文件。
3. 输入以下内容：
```json
{
  "id": "YOUR_STUDENT_ID",
  "pw": "YOUR_PASSWORD"
}
```
4. 保存文件。

**步骤3**：设置文件权限：
```bash
chmod 600 ~/.config/hoseo_lms/credentials.json
```
（Windows系统中无需此步骤，文件权限由操作系统自动处理。）

---

**报告存储**：
- 存储位置：`~/.config/hoseo_lms/data.json`
- 数据格式：JSON结构化数据
- 权限设置：仅用户可访问（权限设置为600）
- 内容：课程数据、课程安排和元数据

**网络使用**：
- 仅通过HTTPS连接到`learn.hoseo.ac.kr`。
- 不会向外部服务传输任何数据。
- 除登录信息外，不会收集用户的任何个人信息。

---

## 技术范围

**实现范围**：
- 收集公开课程页面的数据。
- 解析HTML结构并提取所需信息。
- 将数据聚合为JSON格式。
- 将数据存储在本地文件中并方便检索。
- 支持视频播放进度跟踪。

**未实现范围**：
- 不支持成绩提交或修改。
- 不支持与考勤系统的集成。
- 不支持作业提交功能。
- 不支持自动处理讨论板内容。
- 不支持修改用户账户信息。

---

## 代理集成说明

该工具适用于本地数据分析工作流程：

1. **数据查询**：用户请求课程信息时，代理会读取`data.json`文件或运行`scraper.py`。
2. **日程管理**：用户查询截止日期时，代理会解析`data.json`文件并生成报告。
3. **视频播放**：用户请求播放视频时，代理会执行`auto_attend.py`命令。

**代理应遵循的原则**：
- 在执行`auto_attend.py`之前，必须获得用户的明确请求。
- 播放完成后，代理应向用户确认播放进度。
- 该工具仅作为辅助工具使用，无需修改系统设置。

**代理不应**：
- 在没有用户明确指令的情况下自行执行操作。
- 未经用户确认，不得自动执行任何操作。
- 不得修改脚本的运行逻辑或跳过任何步骤。

---

## 限制

- 如果LMS的HTML结构发生变化，可能需要更新解析器。
- 该工具的可用性受网络连接状况的影响。
- 仅支持Playwright兼容的浏览器环境。
- 视频播放需要LMS中支持的视频播放器。
- 该工具不支持离线模式。

---

## 免责声明

本工具仅供个人教育数据管理使用。用户需负责：
- 遵守学校关于工具使用的政策。
- 正确使用个人教育数据。
- 保护凭据的安全性和控制访问权限。
- 在使用前验证数据的准确性。

开发者不对任何违反学校政策的行为或数据误用承担责任。