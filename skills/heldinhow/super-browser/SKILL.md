# Super Browser Automation

**终极浏览器自动化框架。**整合了8个顶级浏览器自动化工具的优点。

---

## 为什么选择这个工具？

它提供了统一的浏览器自动化解决方案，既可以在本地使用，也可以在云端运行，能够处理从数据抓取到测试等各种网页任务。

---

## 核心功能

### 1. 环境选择（自动）
- **云端** - Browserbase（远程、可扩展）
- **本地** - 本地Chrome/Chromium浏览器
- 根据可用的设备自动选择合适的环境

### 2. 会话管理
- 创建/销毁会话
- 使用用户配置文件（保持登录状态）
- 连接到现有的标签页

### 3. 核心操作
| 命令 | 描述 |
|---------|-------------|
| navigate | 导航到指定URL |
| click | 点击元素 |
| type | 输入文本 |
| snapshot | 分析页面内容 |
| screenshot | 截取屏幕截图 |
| pdf | 将页面内容导出为PDF格式 |

### 4. 交互功能
- 使用快照中的引用（@refs）进行操作
- 等待元素加载完成
- 鼠标控制
- 拖放操作

### 5. 最佳实践
- 在执行操作前务必观察页面状态
- 使用明确的等待策略
- 优雅地处理错误

---

## 使用方法

### 快速自动化示例
```
browser open url="https://example.com"
browser snapshot
browser click ref="login-btn"
```

### 云端会话管理
```
browser session create --provider=browserbase
browser task run --goal="Find pricing page"
```

### 用户配置文件管理
```
browser profile create --name=shopping
browser profile connect --name=shopping
```

---

## 来源工具及评分
| 工具名称 | 评分 |
|---------|--------|
| agent-browser | 3.672 |
| browser-automation | 3.590 |
| browser-use | 3.538 |
| fast-browser-use | 3.534 |
| stagehand-browser-cli | 3.519 |
| agent-browser-stagehand | 3.531 |

---

## 版本信息
v1.0.0 - 初始版本