---
slug: dashboard-manager
display_name: Dashboard Manager
version: 1.0.0
---




# 仪表板管理技能（Dashboard Manager Skill）

## 描述  
该技能用于管理与Jarvis仪表板的交互，能够实时读取、更新和同步`data.json`文件。

## 功能  
- **读取/保存**：访问`data.json`文件  
- **笔记管理**：检索待处理的笔记并将其标记为已处理  
- **日志记录**：将操作记录到历史日志中  
- **系统更新**：更新系统状态、发送心跳信号（heartbeat）以及当前使用的模型  
- **统计信息**：统计令牌数量和成本  
- **任务管理**：添加和更新任务  
- **子代理管理**：管理正在运行的代理（sub-agents）  

## 配置  

### 文件路径  
```javascript
const DATA_FILE_PATH = 'D:\\Projets\\ClaudBot\\Jarvis_Dashboard\\data.json';
```  

### 权限要求  
- **读取/写入**：具有访问`data.json`文件的权限  
- **系统操作**：能够更新系统状态和发送心跳信号  
- **日志记录**：能够将操作记录到历史日志中  

## API  
### 主要功能  
```javascript
// Chargement de la base de données
await loadDatabase();

// Sauvegarde de la base de données
await saveDatabase(db);

// Récupération des notes en attente
const pendingNotes = await getPendingNotes();

// Marquage d'une note comme traitée
await processNote(noteId);

// Ajout d'un log
await addLog('Action effectuée');

// Mise à jour du statut du système
await updateSystemStatus('idle', 'Claude-3-Opus');

// Mise à jour des statistiques
await updateStats(1500, 2800, 0.52);

// Ajout/mise à jour d'une tâche
await updateTask(1, { status: 'done' });

// Gestion des sub-agents
await addSubAgent('dashboard_agent', 'Monitoring dashboard');
await removeSubAgent('dashboard_agent');
```  

## 初始化  
```javascript
const dashboardSkill = require('./skills/dashboard-manager');
const success = await dashboardSkill.init();
if (success) {
    console.log('🚀 Dashboard Manager initialisé');
}
```  

## 所需权限  
- **文件访问权限**：`D:\Projets\ClaudBot\Jarvis_Dashboard\data.json`  
- **系统写入权限**：用于更新系统状态和发送心跳信号  
- **日志记录权限**：用于将操作记录到历史日志中  

## 使用说明  
该技能设计为在后台运行，以实现Jarvis与仪表板之间的实时同步。  

### 运行流程  
1. **输入处理**：查询`quick_notes`并处理待处理的笔记  
2. **输出更新**：将更改内容写入`data.json`文件  
3. **自动同步**：每2秒发送一次心跳信号  
4. **静默模式**：无需用户交互即可自动运行  

## 使用示例  
```javascript
// Dans une réponse conversationnelle
await updateStats(estimatedInputTokens, estimatedOutputTokens, estimatedCost);
await addLog('Réponse à la question sur les agents');
await updateSystemStatus('idle');
```  

## 安装步骤  
1. 将`dashboard-manager`文件夹复制到技能目录中  
2. 确认`data.json`文件的路径正确  
3. 在配置中启用该技能  
4. 技能将自动进行初始化  

## 故障排除  
- **文件未找到**：检查`DATA_FILE_PATH`是否正确  
- **权限问题**：确保具有访问文件的权限  
- **JSON格式错误**：检查`data.json`文件的语法是否正确  

## 日志记录  
所有操作都会自动记录到`data.json`文件的`logs`部分，便于后续追踪。  

## 安全性  
- **访问限制**：仅允许访问`data.json`文件  
- **写入控制**：所有更新操作均需经过验证  
- **审计日志**：所有操作都会被记录下来  

## 兼容性  
该技能兼容OpenClaw，适用于使用V2 Ultimate版本仪表板的任何Jarvis实例。