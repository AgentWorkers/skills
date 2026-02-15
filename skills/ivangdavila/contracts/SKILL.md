---
name: Contracts
description: 组织、跟踪和分析合同，提供续期提醒、条款查询功能，并支持个人、房东、自由职业者和法律团队等多角色用户的使用。
---

## **角色**  
在一个地方管理所有合同。跟踪合同日期，提取关键条款，标记即将到期的合同。支持从个人订阅扩展到企业级合同库的管理。

---

## **存储**  
```
~/contracts/
├── index.md                    # Master list with quick stats
├── by-type/                    # NDAs, leases, subscriptions, etc.
├── by-party/                   # Organized by counterparty
├── {contract-name}/
│   ├── executed.pdf            # Final fully-signed version
│   ├── meta.md                 # Key terms + signature status
│   ├── versions/               # Signature flow tracking
│   │   ├── 01-draft.pdf        # Initial version sent
│   │   ├── 02-signed-them.pdf  # Signed by counterparty
│   │   └── 03-signed-us.pdf    # Countersigned (if sequential)
│   ├── history/                # Amendments after execution
│   └── notes.md                # User notes, flags
```  

**合同状态**：`draft` → `pending-them` → `pending-us` → `executed`  

---

## **快速参考**  
| 内容 | 说明 | 参考文件 |
|---------|------|--------|  
| 与角色相关的工作流程 | `roles.md` |  
| 合同分析模板 | `analysis.md` |  
| 警报与截止日期跟踪 | `alerts.md` |  
| 安全性与权限设置 | `security.md` |  

---

## **核心功能**  
1. **提取关键条款**：合同日期、签约方、金额、通知期限、自动续订条款  
2. **跟踪截止日期**：续订日期、终止窗口、里程碑付款时间  
3. **主动提醒**：在续订或到期前90天/60天/30天发出警告  
4. **快速查询条款**：“X合同的取消通知期限是多少？”  
5. **跨合同搜索**：“查找本季度到期的所有合同”  
6. **版本管理**：将合同修订内容链接到原始合同  
7. **费用汇总**：统计所有订阅或供应商的总花费  

---

## **上传流程**  
当用户上传新合同时：  
1. 在 `~/contracts/{name}` 目录下创建一个文件夹  
2. 将合同文件保存为 `.pdf` 格式  
3. 从合同文件中提取关键信息（签约方、生效日期、条款内容、金额、续订条款、通知期限）并保存到 `meta.md` 文件中  
4. 将这些信息添加到 `index.md` 文件中  
5. 根据 `alerts.md` 文件设置相应的日历提醒  

---

## **使用限制**  
- **不提供法律建议**：无法解读合同条款、评估风险或提供具体操作建议  
- **不使用云存储**：所有合同文件均保存在本地，除非用户自行迁移  
- **禁止内容共享**：严禁通过消息发送合同文本  
- 如有疑问（例如：“这条条款是否合理？”），可提供条款内容供参考，但建议咨询专业律师进行解读  

---

### **活跃中的合同**  
（具体数量和分类信息请参见 `~/contracts/index.md`）  

### **即将到期的合同**  
（具体列表请参考 `meta.md` 文件中标记的“Next 90 days”部分的合同）