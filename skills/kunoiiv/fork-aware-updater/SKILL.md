# 兼容分支更新的更新器  
（Fork-Aware Updater）  

该更新器能够监控分支的变化，自动更新评分高于当前版本的分支（即“更优秀的分支”），并执行安全沙箱测试以确认更新的安全性。  

## 使用方法  
- 使用命令 `node skills/fork-aware-updater/updater.js` 每 6 小时执行一次更新操作。  

## 配置文件（repos.json）  
```json
{
  "slug": "danie/molt-security-auditor",
  "threshold": 10
}
```  

## 工作流程：  
1. 监控新的分支（Radar forks）。  
2. 审查这些分支是否存在安全威胁或需要解决的工作量（PoW，Proof of Work）。  
3. 比较新分支与当前版本的评分。  
4. 如果新分支更优秀，将其放入安全沙箱进行测试。  
5. 由人工确认后，执行 `git pull` 或 `git merge` 操作以应用更新。