# ClawHub Publisher

**版本：** 1.0.0  
**作者：** Midas Skills  
**许可证：** MIT  

## 产品描述  
该工具可自动将开发者的技能发布到 ClawHub 平台，支持版本管理、生成变更日志、打包相关资源，并通过单一命令完成部署。  

## 产品优势  
- 自动化技能发布至 ClawHub；  
- 提供版本控制功能（包括主要版本、次要版本和补丁版本）；  
- 通过 Git 生成详细的变更日志；  
- 支持多文件资源打包；  
- 对元数据进行验证；  
- 优化 README 文件的内容；  
- 自动插入 Gumroad 销售链接；  
- 提供发布历史记录及回滚功能；  
- 提供技能使用数据统计与分析功能；  
- 支持团队协作；  
- 集成持续集成/持续部署（CI/CD）流程（如 GitHub Actions）。  

## 适用场景  
- 自动管理技能的版本与部署流程；  
- 通过单一命令完成技能发布；  
- 自动生成变更日志；  
- 打包包含多个文件的资源文件；  
- 与 Gumroad 平台集成以实现销售功能；  
- 提供技能使用数据的可视化分析；  
- 在出现问题时能够快速回滚错误的部署版本；  
- 支持团队协作进行技能发布。  

## 安装说明  
```bash
npm install clawhub-publisher
# or
pip install clawhub-publisher
```  

## 快速入门指南  
```javascript
const Publisher = require('clawhub-publisher');

const publisher = new Publisher({
  apiKey: process.env.CLAWHUB_API_KEY,
  author: 'Your Name',
  gumroadLink: 'https://gumroad.com/your-product'
});

const result = await publisher.publish({
  skillPath: './my-skill',
  version: '1.0.0',
  changelog: 'Initial release with core features'
});

console.log('Published to:', result.clawHubUrl);
```  

## 项目仓库  
https://github.com/midas-skills/clawhub-publisher  

## 技术支持  
📧 邮箱：support@midas-skills.com  
🔗 文档：https://docs.midas-skills.com/clawhub-publisher