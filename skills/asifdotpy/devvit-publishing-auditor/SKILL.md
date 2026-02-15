# Devvit 发布审核器（Devvit Publishing Auditor）

这是一个专为 Reddit Devvit 开发者设计的专用审核工具，用于在将应用程序上传到 Reddit 服务器之前验证其是否满足发布要求。该工具可确保应用程序符合 Devvit CLI v0.12.x 的规范以及 Reddit 的发布标准。

## 概述  
该工具充当一个预发布检查工具，执行环境检查、依赖项验证、配置审核以及针对 Web View 游戏的合规性扫描。

## 使用方法  
1. 将该工具文件夹/脚本添加到您的项目中。  
2. 命令您的开发人员运行 “Devvit 发布审核器”。  
3. 按照工具生成的 “通过/未通过” 报告中的指示进行操作。  

## 包含的检查项目：  
- **CLI/环境（CLI/Environment）**：版本检查、授权状态以及配置文件的完整性。  
- **配置（Configuration）**：`devvit.json` 文件的验证以及权限映射的准确性。  
- **游戏合规性（Game Compliance）**：资产大小限制、滚动条限制的检测以及启动界面的验证。  
- **文档（Documentation）**：README 文件和隐私政策的相关要求。