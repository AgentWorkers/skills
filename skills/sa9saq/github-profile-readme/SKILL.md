---
description: 生成带有统计徽章、语言使用情况图表以及贡献记录的 GitHub 个人资料页面（README 文件）。
---

# GitHub 个人资料 README 生成器

生成精美的 GitHub 个人资料 README，其中包含统计信息、徽章和贡献记录。

**适用场景**：在创建或更新 GitHub 个人资料 README 时使用。

## 所需信息  
- GitHub 用户名  
- 无需 API 密钥（所有徽章服务都是免费且公开的）

## 使用步骤  
1. **收集信息**：  
   - GitHub 用户名（必填）  
   - 个人简介/标语  
   - 技术栈（使用的语言、框架、工具）  
   - 社交媒体链接（Twitter、LinkedIn、博客等）  
   - 主题偏好：`radical`、`tokyonight`、`dracula`、`gruvbox`、`dark`、`default`  

2. **构建 README 的各个部分**：  
   - **页眉**：包含动态效果（如文字动画或波浪效果）：  
     ```markdown
   ![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=667eea&width=435&lines=Full+Stack+Developer;Open+Source+Enthusiast)
   ```  

   - **GitHub 统计信息**：  
     ```markdown
   ![Stats](https://github-readme-stats.vercel.app/api?username={USER}&show_icons=true&theme={THEME}&hide_border=true)
   ![Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={USER}&layout=compact&theme={THEME}&hide_border=true)
   ```  

   - **贡献记录**：  
     ```markdown
   ![Streak](https://streak-stats.demolab.com?user={USER}&theme={THEME}&hide_border=true)
   ```  

   - **技术栈**：使用 Shields.io 生成的徽章：  
     ```markdown
   ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
   ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
   ```  

   - **社交媒体链接**：  
     ```markdown
   [![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/{handle})
   ```  

3. **生成完整的 Markdown 文件**：  
   - 提醒用户：  
     - 在 GitHub 上创建名为 `{username}/{username}` 的仓库（如果尚不存在）  
     - 将生成的代码片段粘贴到 `README.md` 文件中  
     - 仓库必须设置为 **公开** 才能显示个人资料信息  

## 设计建议  
- 保持页面简洁：最多使用 3-5 行徽章，过多的徽章会显得杂乱无章  
- 在所有统计信息展示组件中保持一致的主题风格  
- 将最重要的信息放在页面顶部（无需滚动即可看到）  
- 添加简短的个人简介：不要完全依赖自动生成的统计信息  
- 使用 `&hide=` 参数来隐藏不太相关的信息  

## 特殊情况处理  
- **新账户且贡献较少**：重点展示个人简介和技术栈。  
- **私有贡献未显示**：在统计信息链接中添加 `&count_private=true` 参数。  
- **统计信息更新不及时**：徽章服务会有 4 小时的缓存时间，可以使用 `&cache_seconds=1800` 来加快更新速度。  
- **徽章图片无法显示**：检查用户名拼写是否正确，并确认徽章服务是否正常运行。  

## 有用的徽章资源  
- [github-readme-stats](https://github.com/anuraghazra/github-readme-stats)：提供统计信息和语言卡片  
- [github-readme-streak-stats](https://github.com/DenverCoder1/github-readme-streak-stats)：用于显示贡献记录的插件  
- [shields.io](https://shields.io)：可自定义各种徽章  
- [simple-icons](https://simpleicons.org)：提供适用于 Shields.io 的徽章图标