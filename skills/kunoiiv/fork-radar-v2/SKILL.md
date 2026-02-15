# Fork Radar – 技能分支监控工具  
该工具用于监控 GitHub/ClawdHub 上的技能分支，以检测潜在的协作行为或后门攻击。通过 `molt-security-auditor` 进行扫描，并利用工作量证明（PoW）机制验证分支的真实性，对存在威胁或评分较高的分支发出警报。  

## 使用方法  
- 使用命令 `\"set up fork radar for molt-security-auditor\"` 来配置监控功能。  
- 通过 `cron` 定时任务（例如：`every=1h`）执行扫描并发送警报。  

## 工作流程：  
1. 从 GitHub API 获取分支列表。  
2. 下载相关技能的 `SKILL.md` 文件并进行安全审计。  
3. 使用工作量证明（PoW）机制验证分支的合法性。  
4. 根据评分（星号数量 > 5）和威胁数量来决定是否触发警报：  
   - 如果评分 > 5 且无威胁，则发出协作警报；  
   - 如果评分 > 0 且有威胁，则发出威胁警报。  

**相关脚本：**  
- `radar.js`：用于执行监控任务的脚本，需要传入仓库地址（例如：`danie/molt-security-auditor`）。