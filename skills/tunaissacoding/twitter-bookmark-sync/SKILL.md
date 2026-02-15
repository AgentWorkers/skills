---
name: twitter-bookmark-sync
description: 该工具能够每日自动对您在 Twitter 上收藏的内容进行排名，并生成一份精心挑选的阅读列表供您阅读。
---

# twitter-bookmark-sync  
**自动化的Twitter书签整理与通知服务**  
再也不会错过任何重要的书签了。该工具会根据您的兴趣自动对Twitter书签进行排序，并每天为您推送一份精选的阅读列表。  

---

## 功能概述  
- **学习**您的书签习惯，了解哪些内容对您来说最重要  
- **自动调整**书签的排名权重（如果长时间未被使用，相关内容的权重会逐渐降低）  
- **按主题和价值类型**对书签进行分类  
- **每天早上**向您发送个性化的阅读建议  
- 使用得越多，功能就越完善  

---

## 系统要求  
- macOS 10.15或更高版本  
- 拥有Twitter账号及书签功能  
- 安装了bird CLI（通过`brew install steipete/tap/bird`命令安装）  
- 需要Clawdbot（用于任务调度和通知功能）  
- 配置了Twitter认证信息（详见“准备工作”部分）  

---

## 准备工作  
### 第一步：安装bird CLI  
```bash
brew install steipete/tap/bird
```  

### 第二步：配置Twitter认证  
从浏览器中提取Twitter认证信息：  
1. 打开浏览器，登录Twitter（访问https://x.com）  
2. 打开开发者工具（Cmd+Option+I），选择“应用程序”→“Cookies”，找到与Twitter相关的Cookie  
3. 复制以下信息：  
   - `auth_token`  
   - `ct0`  
4. 将这些信息保存到配置文件中：  
```bash
mkdir -p ~/.config/bird
cat > ~/.config/bird/config.json5 << 'EOF'
{
  authToken: "your_auth_token_here",
  ct0: "your_ct0_here"
}
EOF
```  
5. 测试连接是否正常：  
```bash
bird whoami
```  

---

## 安装流程  
安装完成后，系统会：  
1. 自动检测您的时区  
2. 设置每日定时任务（午夜获取数据，早上8点发送通知）  
3. 生成您的配置文件  

---

## 配置文件  
编辑`~/clawd/twitter-bookmark-sync-config.json`文件：  
```json5
{
  "fetch_time": "00:00",           // When to learn & rank (24h format)
  "notification_time": "08:00",     // When to send results
  "lookback_hours": 24,             // How far back to check
  "notification_channel": "telegram", // or "gmail", "slack"
  "output_dir": "~/Documents"      // Where to save reading lists
}
```  

**排名规则**（会持续更新）：  
`~/clawd/twitter-bookmark-sync-criteria.json`  
此文件会根据您的书签使用习惯自动更新。**请勿手动修改**——让系统根据您的行为进行学习。  

### 通知方式  
- **Telegram（默认）**  
```json5
{
  "notification_channel": "telegram"
}
```  
- **Gmail（通过gog skill）**  
```json5
{
  "notification_channel": "gmail",
  "gmail_to": "your.email@gmail.com"
}
```  
- **Slack**  
```json5
{
  "notification_channel": "slack",
  "slack_channel": "#bookmarks"
}
```  

---

## 工作原理  
### 每日流程  
- **午夜（00:00）：学习阶段**  
  - 获取过去24小时内的书签  
  - 对书签进行分类（按主题和价值类型）  
  - 更新排名规则：  
    - 未使用的书签权重每天降低5%  
    - 加强您经常使用的分类的权重  
    - 自动发现新的阅读模式  
    - 校正所有书签的权重  
  - 根据更新后的规则对书签进行重新排序  
  - 将结果保存到`~/Documents/twitter-reading-YYYY-MM-DD.md`文件中  

- **早上（08:00）：发送通知**  
  - 分析每本书签对您的价值  
  - 发送详细的阅读建议（而非书签摘要）  
  - 提供完整的阅读列表链接  

### 自学习机制  
- **首次安装时**：  
  - 从`USER.md`配置文件中初始化参数  
  - 创建`twitter-bookmark-sync-criteria.json`文件  
  - 设定11个初始分类及对应的权重（0-100分）  

- **每天午夜**：  
  - 对新添加的书签进行分类  
  - 根据使用情况更新各分类的权重  
  - 旧书签的权重每天降低5%  
  - 活跃使用的分类权重保持不变  
  - 自动发现新的阅读模式  

### 重要优势  
- **适应您的兴趣变化**  
- 无需手动管理关键词  
- 更准确地预测您的阅读偏好  
- 反映您的真实行为，而非预设的默认设置  

---

## 手动操作  
- **立即运行工具**：  
```bash
cd ~/clawd/skills/twitter-bookmark-sync
./scripts/sync.sh
```  
- **调整任务时间**：  
```bash
# Edit config
nano ~/clawd/twitter-bookmark-sync-config.json

# Reload cron jobs
./install.sh
```  

---

## 常见问题与解决方法  
- **“未找到书签”**：  
  - 检查bird CLI的认证是否正常（运行`bird whoami`）  
  - 确认您确实拥有Twitter书签（运行`bird bookmarks -n 5`）  

- **“权限被拒绝”**：  
  - 检查`~/.config/bird/config.json5`文件中的配置  
  - 确保Cookie有效（Cookie可能会过期）  

- **“通知未发送”**：  
  - 检查Clawdbot是否正在运行（运行`clawdbot status`）  
  - 确认配置文件中的通知渠道设置  
  - 查看日志文件`~/clawd/logs/twitter-bookmark-sync.log`  

---

## 许可证  
MIT许可证