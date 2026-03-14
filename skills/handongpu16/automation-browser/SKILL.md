---
name: automation_browser
description: >
  **控制浏览器内核以实现网页自动化**  
  支持网页导航、元素交互、页面滚动、文件/视频下载以及内容提取功能。
metadata: { "openclaw": { "emoji": "🌍", "developer": "QQ浏览器", "requires": { "bins": ["python3"]} } }
---
# QB X5 使用指南

本工具基于浏览器开发，提供全面的浏览器自动化功能。

## 安装（仅需执行一次）

安装 QQ 浏览器以及 `x5use` Python 包。

```bash
bash skills/qb-x5-use/scripts/install_dep.sh
```

## 设置（每次使用前执行）

在端口 18009 启动 X5 后台服务。安装完成后必须执行此命令。如果服务已在运行，该命令会立即退出而不会重新启动服务。

```bash
bash skills/qb-x5-use/scripts/setup.sh
```

## 命令列表

### 导航
```bash
python3 skills/qb-x5-use/scripts/go_to_url.py <url>    # 导航到指定 URL
python3 skills/qb-x5-use/scripts/go_back.py             # 返回上一页
```

### 元素交互
```bash
python3 skills/qb-x5-use/scripts/click_element.py <index> [xpath]      # 根据索引点击元素
python3 skills/qb-x5-use/scripts/input_text.py <index> <text> [xpath]  # 根据索引和文本填充输入框
python3 skills/qb-x5-use/scripts/getDropdown_options.py <index>       # 获取下拉菜单的选项
python3 skills/qb-x5-use/scripts/selectDropdown_option.py <index> <text>  # 从下拉菜单中选择选项
```

### 滚动
```bash
python3 skills/qb-x5-use/scripts/scroll_down.py [amount]       # 向下滚动指定距离
python3 skills/qb-x5-use/scripts/scroll_up.py [amount]         # 向上滚动指定距离
python3 skills/qb-x5-use/scripts/scroll_to_text.py <text>      # 滚动到包含指定文本的位置
python3 skills/qb-x5-use/scripts/scroll_to_top.py              # 滚动到页面顶部
python3 skills/qb-x5-use/scripts/scroll_to_bottom.py           # 滚动到页面底部
```

### 下载
```bash
python3 skills/qb-x5-use/scripts/download_file.py <index>      # 根据索引下载文件
python3 skills/qb-x5-use/scripts/download_url.py <url>         # 根据 URL 下载文件
```

### 获取页面内容
```bash
python3 skills/qb-x5-use/scripts/get_content.py                # 获取页面内容（以 Markdown 格式）
```

### 等待
```bash
python3 skills/qb-x5-use/scripts/wait.py [seconds]             # 等待指定时间
```

## 核心工作流程

1. **导航**：使用 `go_to_url.py <url>` 导航到目标 URL。
2. **读取页面内容**：检查返回的页面元素（使用索引 `[0]`, `[1]` 等引用）。
3. **进行交互**：根据返回的元素信息执行点击、输入等操作。
4. **重新读取页面内容**：导航或交互后，再次检查页面上的可交互元素。

## 返回值

每个命令都会返回当前页面的状态，包括操作结果和所有可交互元素的信息。

### 数据结构

**操作结果**：
- 操作是否成功
- 目标 URL 和内容类型（Content-Type）

**页面内容**：
| 字段        | 描述                                      |
|-------------|-----------------------------------------|
| 上一页        | 上一页的标题和 URL                               |
| 操作          | 执行的操作名称和参数                              |
| 操作结果      | 操作的结果（例如：`navigation triggered` 表示导航被触发）       |
| 当前页面      | 当前页面的标题和 URL                               |
| 可交互元素      | 视口内的所有可交互元素（格式：`[index]<tag text/>`         |

### 示例输出

**导航到百度**：

```bash
python3 skills/qb-x5-use/scripts/go_to_url.py https://www.baidu.com/
```

```plaintext
操作结果：成功！已导航到 https://www.baidu.com/，响应头中的内容类型为 'text/html; charset=utf-8'。

>>>>> 页面内容
当前页面的状态：
[开始状态]
上一页：百度一下，你就知道 (https://www.baidu.com/)
操作：go_to_url ("url":"https://www.baidu.com/")
操作结果：导航被触发。
当前页面：[0] 百度一下，你就知道 (https://www.baidu.com/)
当前页面可视区域内的可交互元素：
[0]<a 新闻/>
[1]<a hao123/>
[2]<a 地图/>
[3]<a 贴吧/>
[5]<a 图片/>
[13]<textarea/>
[29]<button 百度一下/>
[12]<a tj_login>登录/>
...
[结束状态]
```

### 可交互元素的格式

每个可交互元素的格式为：`[index]<tag text/>`，其中：
- `index`：用于 `click_element`、`input_text` 等操作的元素索引。
- `<tag>`：元素的 HTML 类型（如 `a`、`button`、`textarea`、`div`、`img`、`span`）。
- `text`：元素显示的文本（可能为空）。

**示例：在百度上搜索**

```bash
# 导航到百度
python3 skills/qb-x5-use/scripts/go_to_url.py https://www.baidu.com/
# 输出：
[13]<textarea/>
[29]<button 百度一下/>
```

**操作步骤**：
1. 使用 `input_text.py 13 "搜索词"` 向搜索框输入搜索词。
2. 使用 `click_element.py 29` 点击搜索按钮。
3. 使用 `get_content.py` 获取搜索结果。

**示例：滚动和下载**：
```bash
# 导航到目标页面
python3 skills/qb-x5-use/scripts/go_to_url.py https://example.com/files/
# 向下滚动 500 像素
python3 skills/qb-x5-use/scripts/scroll_down.py 500
# 根据索引下载文件
python3 skills/qb-x5-use/scripts/download_file.py 5
# 或者直接通过 URL 下载文件
python3 skills/qb-x5-use/scripts/download_url.py https://example.com/file.pdf
```

## 故障排除：
- 如果找不到某个元素，请查看返回的可交互元素列表以确定正确的索引。
- 如果页面未完全加载，请在导航后添加 `wait.py` 命令等待页面加载完成。