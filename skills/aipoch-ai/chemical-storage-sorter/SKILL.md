---
name: chemical-storage-sorter
description: 根据化学品的兼容性对它们进行分类，以确保实验室的安全储存。通过将不相容的化学品（如酸、碱、氧化剂和易燃物）分开存放，可以防止危险反应的发生，并提供符合安全规定的储存建议。
allowed-tools: [Read, Write, Bash, Edit]
license: MIT
metadata:
  skill-author: AIPOCH
---
# 化学品储存管理系统

该系统根据化学品的兼容性和危险性将其分类，并组织到安全的储存区域中。通过识别不兼容的化学品对，并提供符合OSHA、NFPA和机构安全标准的储存指南，来防止危险反应的发生。

**主要功能：**
- **自动化学品分类**：将化学品分为不同的危险类别（酸、碱、氧化剂、易燃物、有毒物质）
- **兼容性检查**：识别如果存放在一起可能会发生危险反应的不兼容化学品对
- **储存分组**：自动将化学品清单分类到安全的储存区域
- **安全警告**：为不兼容的储存组合和危险相互作用生成警告
- **合规性**：遵循OSHA和NFPA的标准化学品分离规则

---

## 使用场景

**✅ 在以下情况下使用该系统：**
- 设置新的实验室储存系统并需要整理化学品清单
- 为EHS（环境健康与安全）检查或合规性审计做准备
- 搬迁或重新组织现有的化学品储存区域
- 清点化学品并检查当前的储存安排是否存在安全隐患
- 为新实验室成员提供化学品储存安全培训
- 调查因储存不当或反应引起的化学品事故
- 制定化学品处理和储存的标准操作程序（SOP）

**❌ 不适用的情况：**
- 处理未知成分的化学品或未标记的容器 → 首先联系EHS进行正确识别
- 需要特定的储存温度要求 → 使用专门的温度监测工具
- 处理放射性物质或生物危害物质 → 遵循这些物质的专门协议
- 需要化学品处置说明 → 使用`waste-disposal-guide`获取处置程序
- 需要查询SDS（安全数据表） → 使用`safety-data-sheet-reader`获取详细的化学品信息
- 需要规划化学品库存跟踪 → 使用`lab-inventory-tracker`进行数量和位置的跟踪

**相关技能：**
- **上游技能**：`safety-data-sheet-reader`、`chemical-structure-converter`
- **下游技能**：`lab-inventory-tracker`、`waste-disposal-guide`

---

## 与其他技能的集成

**上游技能：**
- `safety-data-sheet-reader`：从SDS中检索化学品属性和危险性分类
- `chemical-structure-converter`：根据结构或名称识别化学品类别以进行准确分类

**下游技能：**
- `lab-inventory-tracker`：在化学品分类和分配后记录储存位置
- `waste-disposal-guide`：识别需要移除的不兼容化学品的处置要求
- `equipment-maintenance-log`：跟踪安全柜的检查和维护

**完整工作流程：**
```
Chemical Inventory → safety-data-sheet-reader → chemical-storage-sorter → lab-inventory-tracker → Safe Storage
```

---

## 核心功能

### 1. 按危险类别对化学品进行分类

根据化学品名称、化学式或关键词，自动将化学品分类到标准的危险类别中。

```python
from scripts.main import ChemicalStorageSorter

sorter = ChemicalStorageSorter()

# Classify individual chemicals
chemicals = [
    "Hydrochloric acid",
    "Sodium hydroxide",
    "Hydrogen peroxide 30%",
    "Ethanol",
    "Sodium chloride"
]

for chem in chemicals:
    group = sorter.classify_chemical(chem)
    print(f"{chem}: {group}")

# Output:
# Hydrochloric acid: acids
# Sodium hydroxide: bases
# Hydrogen peroxide 30%: oxidizers
# Ethanol: flammables
# Sodium chloride: general
```

**危险类别：**

| 类别 | 示例 | 主要危险性 | 储存要求 |
|-------|----------|-------------|---------------------|
| **酸** | HCl、H₂SO₄、HNO₃、醋酸 | 腐蚀性、反应性 | 酸性储存柜，二次防护措施 |
| **碱** | NaOH、KOH、氨水、胺类 | 腐蚀性、碱性 | 碱性储存柜，与酸分开存放 |
| **氧化剂** | H₂O₂、KMnO₄、硝酸盐、次氯酸盐 | 易燃/爆炸风险 | 冷爽、干燥的环境，远离有机物 |
| **易燃物** | 乙醇、甲醇、丙酮、己烷 | 易燃性 | 易燃储存柜 |
| **有毒物质** | 氰化物、汞、砷化合物 | 有毒性、生物累积性 | 上锁储存柜，限制访问 |
| **其他** | NaCl、PBS、蔗糖、甘油 | 低危险性 | 通用储存柜 |

**分类关键词：**

| 类别 | 关键词示例 |
|-------|------------------|
| **酸** | acid、hcl、sulfuric、nitric、acetic、citric、formic |
| **碱** | hydroxide、naoh、koh、ammonia、amine、carbonate |
| **易燃物** | ethanol、methanol、acetone、ether、hexane、toluene、benzene |
| **氧化剂** | peroxide、permanganate、hypochlorite、nitrate、chlorate、perchlorate |
| **有毒物质** | cyanide、mercury、arsenic、lead、cadmium、thallium |

**最佳实践：**
- ✅ 使用完整的化学品名称以获得最准确的分类
- ✅ 在相关情况下包含浓度信息（例如，“30%过氧化氢”而非“3%”）
- ✅ 如果分类似乎不正确，请手动检查化学品
- ✅ 为实验室特有的化学品更新关键词列表

**常见问题及解决方法：**

**问题：化学品未被识别**  
- 症状：尽管具有危险性，但仍被分类为“其他”  
- 解决方法：使用更具体的化学品名称；为实验室特有的化合物添加自定义关键词

**问题：相似名称的化学品分类错误**  
- 症状：由于包含“acet”关键词，将“sodium acetate”错误地分类为酸  
- 解决方法：检查分类结果；必要时手动调整

### 2. 检查化学品之间的兼容性**

确定两种化学品是否可以安全地一起储存，以避免危险反应。

```python
from scripts.main import ChemicalStorageSorter

sorter = ChemicalStorageSorter()

# Check specific chemical pairs
pairs_to_check = [
    ("Hydrochloric acid", "Sodium hydroxide"),
    ("Ethanol", "Hydrogen peroxide"),
    ("Sodium chloride", "Potassium chloride"),
    ("Nitric acid", "Acetone")
]

for chem1, chem2 in pairs_to_check:
    compatible, message = sorter.check_compatibility(chem1, chem2)
    status = "✅ Compatible" if compatible else "❌ INCOMPATIBLE"
    print(f"{chem1} + {chem2}: {status}")
    if not compatible:
        print(f"   Warning: {message}")

# Output:
# Hydrochloric acid + Sodium hydroxide: ❌ INCOMPATIBLE
#    Warning: INCOMPATIBLE: acids cannot be stored with bases
# Ethanol + Hydrogen peroxide: ❌ INCOMPATIBLE
#    Warning: INCOMPATIBLE: flammables cannot be stored with oxidizers
# Sodium chloride + Potassium chloride: ✅ Compatible
# Nitric acid + Acetone: ❌ INCOMPATIBLE
```

**不兼容性矩阵：**

| 化学品类别 | 不兼容的化学品 | 反应风险 |
|----------------|------------------|---------------|
| **酸** | 碱、氧化剂、氰化物、硫化物 | 强烈中和反应，产生有毒气体 |
| **碱** | 酸、氧化剂、卤化物 | 产生热量，分解 |
| **氧化剂** | 易燃物、酸、碱、还原剂 | 火灾、爆炸、剧烈反应 |
| **易燃物** | 氧化剂、酸 | 火灾，加剧燃烧 |
| **有毒物质** | 酸、氧化剂 | 释放有毒气体，增加危险性 |

**最佳实践：**
- ✅ 在放置前将所有新化学品与现有储存规则进行对比  
- ✅ 对于不兼容的化学品对，保持至少3英尺的间距  
- ✅ 对于高度反应性的化学品对，考虑使用二次防护措施  
- ✅ 记录需要特殊处理的例外情况

**常见问题及解决方法：**

**问题：误判兼容性**  
- 症状：工具显示兼容，但实际上化学品会发生反应  
- 原因：通用规则中未包含特定的不兼容性  
- 解决方法：始终参考SDS中的具体不兼容性信息；将其作为初步检查

### 3. 自动进行储存分组**

根据危险性分类，将整个化学品清单自动分类到安全的储存区域中。

```python
from scripts.main import ChemicalStorageSorter

sorter = ChemicalStorageSorter()

# Example lab inventory
inventory = [
    "Hydrochloric acid (conc.)",
    "Sodium hydroxide pellets",
    "Ethanol 95%",
    "Acetone",
    "Hydrogen peroxide 30%",
    "Potassium permanganate",
    "Sodium chloride",
    "PBS buffer",
    "Glycerol",
    "Sulfuric acid",
    "Ammonium hydroxide",
    "Methanol",
    "Hexane",
    "Mercury(II) chloride"
]

# Sort into storage groups
groups = sorter.sort_chemicals(inventory)

# Display results
for group, chemicals in groups.items():
    if chemicals:
        print(f"\n{group.upper()} STORAGE:")
        for chem in chemicals:
            print(f"  • {chem}")
```

**储存分组输出：**
```
ACIDS STORAGE:
  • Hydrochloric acid (conc.)
  • Sulfuric acid

BASES STORAGE:
  • Sodium hydroxide pellets
  • Ammonium hydroxide

OXIDIZERS STORAGE:
  • Hydrogen peroxide 30%
  • Potassium permanganate

FLAMMABLES STORAGE:
  • Ethanol 95%
  • Acetone
  • Methanol
  • Hexane

TOXICS STORAGE:
  • Mercury(II) chloride

GENERAL STORAGE:
  • Sodium chloride
  • PBS buffer
  • Glycerol
```

**最佳实践：**
- ✅ 在每个类别内按字母顺序排序，以便于查找  
- ✅ 在标签上标注稀释和浓缩化学品的浓度  
- ✅ 根据使用频率分组——最常用的化学品应放在最容易获取的位置  
- ✅ 将大部分化学品存放在通用储存区域（通常占60-70%）

**常见问题及解决方法：**

**问题：化学品属于多个类别**  
- 症状：一种化学品具有多种危险性（例如，浓缩的HNO₃同时属于酸和氧化剂）  
- 解决方法：将其存放在最严格的类别中（例如氧化剂储存柜）；检查所有不兼容性

**问题：处理大量化学品清单**  
- 症状：需要处理数百种化学品  
- 解决方法：按实验室区域分批处理；将结果导出到电子表格中以便手动审核

### 4. 生成带有安全警告的储存计划**

生成包含具体警告和分离要求的完整储存计划。

```python
from scripts.main import ChemicalStorageSorter

sorter = ChemicalStorageSorter()

# Generate full storage plan
demo_inventory = [
    "HCl (concentrated)",
    "NaOH pellets",
    "Ethanol",
    "Hydrogen peroxide",
    "Sodium cyanide",
    "PBS",
    "Acetone"
]

groups = sorter.sort_chemicals(demo_inventory)
sorter.print_storage_plan(groups)
```

**示例输出：**
```
============================================================
CHEMICAL STORAGE PLAN
============================================================

ACIDS STORAGE:
----------------------------------------
  • HCl (concentrated)
  ⚠️  Keep away from: bases, oxidizers, cyanides, sulfides

BASES STORAGE:
----------------------------------------
  • NaOH pellets
  ⚠️  Keep away from: acids, oxidizers, halogenated

OXIDIZERS STORAGE:
----------------------------------------
  • Hydrogen peroxide
  ⚠️  Keep away from: flammables, acids, bases, reducing

FLAMMABLES STORAGE:
----------------------------------------
  • Ethanol
  • Acetone
  ⚠️  Keep away from: oxidizers, acids

TOXICS STORAGE:
----------------------------------------
  • Sodium cyanide
  ⚠️  Keep away from: acids, oxidizers

GENERAL STORAGE:
----------------------------------------
  • PBS

============================================================
```

**按类别划分的储存要求：**

| 类别 | 储存柜类型 | 通风要求 | 特殊要求 |
|-------|-------------|-------------|---------------------|
| **酸** | 酸性储存柜 | 需要通风罩 | 需要二次防护措施，耐腐蚀 |
| **碱** | 碱性储存柜 | 标准要求 | 与酸分开存放（至少3英尺距离） |
| **氧化剂** | 标准/氧化剂储存柜 | 需要冷却、干燥的环境 | 远离火源 |
| **易燃物** | 易燃储存柜 | 防爆设计 | 需要接地 |
| **有毒物质** | 上锁储存柜 | 标准要求 | 限制访问量 |
| **其他** | 标准货架 | 标准实验室储存要求 |

**最佳实践：**
- ✅ 将储存计划清晰地张贴在储存区域附近  
- ✅ 当化学品添加或移除时更新储存计划  
- ✅ 在储存计划上标注紧急联系信息  
- ✅ 每季度审查一次计划的准确性  

**常见问题及解决方法：**

**问题：储存空间不足**  
- 症状：多个类别需要相同类型的储存柜  
- 解决方法：根据危险性优先级选择储存柜；必要时购买额外的储存柜  

**问题：某些化学品有多重不兼容性**  
- 症状：一种化学品与许多其他化学品不兼容  
- 解决方法：将这些化学品隔离存放；考虑减少库存  

### 5. 批量处理化学品清单**

从文件中处理大量化学品清单，以实现全面的储存组织。

```python
from scripts.main import ChemicalStorageSorter
import json

def process_inventory_file(file_path: str) -> dict:
    """
    Process chemical inventory from text file.
    
    Expected format: One chemical per line
    """
    sorter = ChemicalStorageSorter()
    
    # Read inventory
    with open(file_path, 'r') as f:
        chemicals = [line.strip() for line in f if line.strip()]
    
    # Sort into groups
    groups = sorter.sort_chemicals(chemicals)
    
    # Calculate statistics
    stats = {
        'total_chemicals': len(chemicals),
        'groups': {group: len(items) for group, items in groups.items() if items},
        'hazardous_chemicals': sum(len(items) for group, items in groups.items() 
                                   if group != 'general' and items)
    }
    
    # Check for incompatibilities within current storage
    incompatibilities = []
    all_groups = list(groups.keys())
    
    for i, group1 in enumerate(all_groups):
        for group2 in all_groups[i+1:]:
            if group2 in sorter.COMPATIBILITY_GROUPS[group1]['incompatible']:
                if groups[group1] and groups[group2]:
                    incompatibilities.append({
                        'group1': group1,
                        'chemicals1': groups[group1],
                        'group2': group2,
                        'chemicals2': groups[group2]
                    })
    
    return {
        'groups': groups,
        'statistics': stats,
        'incompatibilities': incompatibilities
    }

# Example usage
# results = process_inventory_file('lab_inventory.txt')
# print(json.dumps(results, indent=2))
```

**输入文件格式：**
```
# lab_inventory.txt
Hydrochloric acid (37%)
Sodium hydroxide
Ethanol (95%)
Acetone
Hydrogen peroxide (30%)
Potassium permanganate
Sodium chloride
Phosphate buffered saline
Glycerol
Sulfuric acid (conc.)
```

**最佳实践：**
- ✅ 在清单文件中使用标准化的命名规则  
- ✅ 包括稀释化学品的浓度信息  
- ✅ 为清单添加日期以便追踪变化  
- ✅ 归档旧版本以供历史参考  

**常见问题及解决方法：**

**问题：拼写错误和命名不一致**  
- 症状：同一种化学品有多种命名方式  
- 解决方法：标准化命名规则；对于不确定的情况使用CAS编号  

**问题：浓度信息不一致**  
- 症状：同一化学品有多种不同的浓度记录  
- 解决方法：在名称中包含浓度信息；根据最危险的浓度进行储存  

### 6. 自定义分类规则**

扩展分类系统，以适应实验室特定的化学品和自定义规则。

```python
from scripts.main import ChemicalStorageSorter

class CustomChemicalSorter(ChemicalStorageSorter):
    """Extended sorter with lab-specific chemicals."""
    
    def __init__(self):
        super().__init__()
        # Add custom chemicals to groups
        self.COMPATIBILITY_GROUPS['acids']['examples'].extend([
            'trifluoroacetic acid',
            'trichloroacetic acid'
        ])
        
        self.COMPATIBILITY_GROUPS['flammables']['examples'].extend([
            'isopropanol',
            'isopropyl alcohol',
            '2-propanol'
        ])
        
        # Add custom keyword mappings
        self.custom_keywords = {
            'acids': ['tfa', 'tca'],
            'flammables': ['ipa', 'propanol']
        }
    
    def classify_chemical(self, name):
        """Override with custom keyword checking."""
        name_lower = name.lower()
        
        # Check custom keywords first
        for group, keywords in self.custom_keywords.items():
            if any(kw in name_lower for kw in keywords):
                return group
        
        # Fall back to parent classification
        return super().classify_chemical(name)

# Use custom sorter
custom_sorter = CustomChemicalSorter()
print(custom_sorter.classify_chemical("TFA"))  # Will classify as acid
print(custom_sorter.classify_chemical("IPA"))  # Will classify as flammable
```

**最佳实践：**
- ✅ 将自定义规则记录在实验室的SOP中  
- ✅ 与所有实验室成员共享这些规则以确保一致性  
- ✅ 定期审查规则的完整性  
- ✅ 当引入新的化学品时更新规则  

**常见问题及解决方法：**

**问题：自定义规则与默认规则冲突**  
- 症状：化学品的分类与预期不同  
- 解决方法：检查规则的优先级；通常自定义规则应优先于默认规则  

**问题：太多化学品需要自定义分类**  
- 症状：大多数化学品都需要自定义分类  
- 解决方法：更新默认数据库；向上游团队提出改进建议  

---

## 完整工作流程示例

**从化学品清单到有序的储存：**

```bash
# Step 1: List current chemicals
python scripts/main.py --chemicals "HCl,NaOH,ethanol,acetone,H2O2,PBS"

# Step 2: Check compatibility of specific pair
python scripts/main.py --chemicals "HCl" --check "NaOH"

# Step 3: View storage groups
python scripts/main.py --list-groups

# Step 4: Process full inventory file
python scripts/main.py --chemicals "$(cat inventory.txt | tr '\n' ',')"
```

**Python API使用方法：**

```python
from scripts.main import ChemicalStorageSorter

def organize_lab_storage(chemical_inventory: list) -> dict:
    """
    Complete workflow for organizing laboratory chemical storage.
    
    Returns:
        Dictionary with storage groups, warnings, and recommendations
    """
    sorter = ChemicalStorageSorter()
    
    # Sort chemicals into groups
    groups = sorter.sort_chemicals(chemical_inventory)
    
    # Generate storage plan
    print("\n" + "="*60)
    print("LABORATORY CHEMICAL STORAGE ORGANIZATION")
    print("="*60)
    
    sorter.print_storage_plan(groups)
    
    # Identify potential issues
    issues = []
    
    # Check for high-hazard concentrations
    hazardous_chemicals = []
    for group in ['acids', 'bases', 'oxidizers']:
        for chem in groups[group]:
            if 'conc' in chem.lower() or 'concentrated' in chem.lower():
                hazardous_chemicals.append((chem, group))
    
    if hazardous_chemicals:
        issues.append({
            'type': 'concentrated_hazard',
            'chemicals': hazardous_chemicals,
            'recommendation': 'Ensure secondary containment and fume hood access'
        })
    
    # Check storage space distribution
    total_chemicals = len(chemical_inventory)
    general_percentage = len(groups['general']) / total_chemicals * 100
    
    if general_percentage < 50:
        issues.append({
            'type': 'high_hazard_ratio',
            'message': f'Only {general_percentage:.1f}% chemicals are general storage',
            'recommendation': 'Review if all hazardous classifications are necessary'
        })
    
    # Compile results
    results = {
        'storage_groups': groups,
        'statistics': {
            'total_chemicals': total_chemicals,
            'hazardous_chemicals': total_chemicals - len(groups['general']),
            'general_percentage': general_percentage
        },
        'issues': issues,
        'recommendations': [
            'Label all storage cabinets with group names',
            'Post incompatibility matrix near storage area',
            'Schedule quarterly storage inspections',
            'Train all lab members on chemical segregation'
        ]
    }
    
    return results

# Execute workflow
inventory = [
    "Hydrochloric acid (conc.)",
    "Sulfuric acid",
    "Sodium hydroxide",
    "Potassium hydroxide",
    "Ethanol 95%",
    "Methanol",
    "Acetone",
    "Hydrogen peroxide 30%",
    "Nitric acid",
    "Sodium chloride",
    "PBS",
    "Tris buffer",
    "EDTA",
    "Glycerol"
]

results = organize_lab_storage(inventory)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total chemicals: {results['statistics']['total_chemicals']}")
print(f"Hazardous: {results['statistics']['hazardous_chemicals']}")
print(f"General storage: {results['statistics']['general_percentage']:.1f}%")

if results['issues']:
    print("\n⚠️  Issues identified:")
    for issue in results['issues']:
        print(f"  - {issue['type']}: {issue.get('recommendation', '')}")

print("\n📋 Recommendations:")
for rec in results['recommendations']:
    print(f"  • {rec}")
```

**预期输出文件：**

```
storage_organization/
├── storage_plan.txt         # Human-readable storage layout
├── chemical_groups.json     # Machine-readable group assignments
├── incompatibilities.csv    # List of incompatible pairs
└── recommendations.md       # Safety recommendations
```

---

## 常见模式

### 模式1：新实验室设置**

**场景**：从零开始为新的实验室设置化学品储存系统。

```json
{
  "setup_type": "new_lab",
  "space": "2 fume hoods, 3 acid cabinets, 2 flammable cabinets",
  "inventory_size": "~200 chemicals expected",
  "special_requirements": [
    "Cell culture focus - many biological buffers",
    "Molecular biology - EtBr, acrylamide",
    "Some organic synthesis - various solvents"
  ],
  "compliance": "OSHA, university EHS"
}
```

**工作流程：**
1. 在化学品到达之前先进行清单统计  
2. 使用该工具对每种化学品进行分类  
3. 根据分类结果分配储存位置  
4. 购买相应的储存柜（酸性、易燃性等）  
5. 清晰地标记所有储存区域  
6. 对所有实验室成员进行系统培训  
7. 张贴紧急程序和联系信息  

**输出示例：**
```
New Lab Storage Plan:

CABINET ASSIGNMENTS:
  Acid Cabinet #1: 12 acids
  Acid Cabinet #2: 8 oxidizers (also acids)
  Base Cabinet: 6 bases
  Flammable Cabinet #1: 15 solvents (ethanol, methanol, etc.)
  Flammable Cabinet #2: 8 other flammables
  Toxic Cabinet: 3 chemicals (EtBr, acrylamide, mercury salts)
  General Storage: 148 buffers, salts, reagents

SPACE UTILIZATION:
  Acid cabinets: 20/30 capacity (67%)
  Flammable: 23/40 capacity (58%)
  General: 148/200 capacity (74%)

RECOMMENDATION: Current space adequate for planned inventory
```

### 模式2：安全检查准备**

**场景**：为年度EHS安全检查做准备。

```json
{
  "inspection_type": "annual_ehs",
  "focus_areas": [
    "Chemical segregation compliance",
    "Incompatible storage checks",
    "Labeling and signage",
    "Secondary containment"
  ],
  "documentation_required": [
    "Chemical inventory",
    "Storage plan",
    "Incompatibility records"
  ]
}
```

**工作流程：**
1. 使用储存管理系统对所有化学品进行分类  
2. 检查当前的储存情况是否符合建议  
3. 识别当前储存安排中的不兼容情况  
4. 将放置不当的化学品移至正确的储存位置  
5. 更新储存计划文档  
6. 打印并张贴当前的储存布局图  
7. 确保所有储存柜都正确标记  
8. 检查二次防护系统的状态  

**输出示例：**
```
Pre-Inspection Report:

✅ COMPLIANT STORAGE: 187/195 chemicals (95.9%)

⚠️  ISSUES IDENTIFIED:
  1. Acetic acid (glacial) stored with general chemicals
     → Move to acid cabinet
  2. Hydrogen peroxide near ethanol shelf
     → Move to oxidizer section
  3. Missing secondary containment for HCl
     → Add acid tray

📋 DOCUMENTATION READY:
  ✓ Chemical inventory (195 items)
  ✓ Storage plan (updated 2026-02-09)
  ✓ Incompatibility matrix (posted)
  ✓ Emergency contacts (current)

INSPECTION READINESS: 95% (2 chemicals need moving)
```

### 模式3：化学品搬迁**

**场景**：将化学品搬迁到新的位置或不同的实验室。**

```json
{
  "relocation_type": "lab_move",
  "from": "Building A, Room 301",
  "to": "Building B, Room 205",
  "chemicals_to_move": 150,
  "special_considerations": [
    "Some chemicals expire soon",
    "Unknown origin of 5 chemicals",
    "Need to dispose of 20 chemicals"
  ]
}
```

**工作流程：**
1. 统计当前位置的所有化学品  
2. 对所有化学品进行分类和排序  
3. 识别需要处理的化学品（过期、未知或不再需要的化学品）  
4. 按储存类别规划打包  
5. 确保运输过程中的正确分离  
6. 设计新位置的储存布局  
7. 将化学品直接存放在新的储存区域  
8. 更新化学品清单中的位置信息  

**输出示例：**
```
Relocation Plan:

CHEMICALS TO MOVE: 130 items
  - Acids: 8 (pack together, upright)
  - Bases: 5 (pack together, separate from acids)
  - Flammables: 22 (DOT-approved containers)
  - Oxidizers: 6 (separate transport)
  - Toxics: 2 (locked container, manifest required)
  - General: 87 (standard boxes)

CHEMICALS TO DISPOSE: 20 items
  - Expired: 12
  - Unknown: 5
  - Unneeded: 3
  → Schedule waste pickup before move

PACKING SEQUENCE:
  Day 1: Dispose of waste chemicals
  Day 2: Pack general chemicals
  Day 3: Pack flammables and toxics
  Day 4: Transport and unpack
  Day 5: Final inventory at new location
```

### 模式4：新实验室成员培训**

**场景**：为新研究生或技术人员提供化学品安全培训。

```json
{
  "training_type": "new_member_safety",
  "trainees": 3,
  "duration": "2 hours",
  "topics": [
    "Chemical hazard recognition",
    "Storage segregation rules",
    "Emergency procedures",
    "Finding chemicals in lab"
  ]
}
```

**工作流程：**
1. 使用该工具介绍化学品危险类别  
2. 使用实验室清单中的实际案例进行演示  
3. 演示如何检查化学品的兼容性  
4. 练习对未知化学品进行分类  
5. 参观实际的储存区域  
6. 进行关于不兼容化学品对的测验  
7. 提供储存计划作为参考  
8. 记录培训完成情况  

**输出示例：**
```
Training Session: Chemical Storage Safety

DEMONSTRATION EXAMPLES:
  1. Show classification: "ethanol" → flammable
  2. Show incompatibility: HCl + NaOH → violent reaction
  3. Show safe storage: PBS + NaCl → general storage together

INTERACTIVE QUIZ:
  Q: Can you store acetone near hydrogen peroxide?
  A: No - flammable + oxidizer = fire risk ✅
  
  Q: Where should concentrated HCl go?
  A: Acid cabinet with secondary containment ✅

HANDOUTS PROVIDED:
  ✓ Storage plan (current)
  ✓ Incompatibility matrix
  ✓ Emergency contact card
  ✓ SDS access instructions

TRAINING COMPLETE: 3/3 trainees passed quiz (100%)
```

---

## 质量检查清单

**组织前的准备：**
- [ ] **关键**：确保所有化学品容器都正确标记  
- [ ] 获取完整的化学品清单（包括浓度信息）  
- [ ] 查看SDS中分类不明确的化学品  
- [ ] 测量可用的储存空间（储存柜、货架）  
- [ ] 识别需要处理的过期或不再需要的化学品  
- [ ] 确认紧急设备的可用性（洗眼器、淋浴设施、泄漏处理工具）  
- [ ] 查看机构的EHS要求和限制  

**分类过程中的注意事项：**
- [ ] 使用完整的化学品名称对每种化学品进行分类  
- [ ] 注意稀释和浓缩形式的浓度信息  
- **关键**：手动检查边界情况的化学品分类  
- [ ] 检查具有多种危险性的化学品  
- [ ] 记录任何需要特殊储存的化学品  
- [ ] 标记需要特殊储存条件的化学品（如温度敏感或光照敏感的化学品）  
- [ ] 识别需要二次防护措施的化学品  
- [ ] 注意标明有保质期的化学品  

**储存分配时的注意事项：**
- [ ] **关键**：确保不兼容的化学品物理上分开存放（至少3英尺距离）  
- [ ] 确保每个储存类别有足够的空间  
- [ ] 将最危险的化学品存放在最安全的位置  
- [ ] 确保常用化学品易于获取  
- [ ] 确保储存柜的通风设施适合储存内容物  
- [ ] 确认酸性储存柜具有耐腐蚀结构  
- [ ] 确保有毒化学品存放在上锁的储存柜中  

**组织后的验证：**
- [ ] **关键**：确保没有不兼容的化学品被存放在一起  
- [ ] 确保所有容器都正确标记了化学品名称和危险性  
- [ ] 确认储存计划已张贴在化学品区域附近  
- [ ] 确认紧急程序已张贴并易于查看  
- [ ] 确认泄漏处理工具适合储存的化学品  
- [ ] 确保SDS手册易于获取且信息是最新的  
- [ ] 确保所有实验室成员都能轻松找到化学品  
- [ ] 安排下一次检查的时间  

**文档记录：**
- [ ] **关键**：根据新的储存位置更新化学品清单  
- [ ] 记录任何对标准储存规则的例外情况  
- [ ] 记录所有实验室成员的培训完成情况  
- [ ] 将储存计划文件保存在实验室笔记本或ELN中  
- [ ] 与EHS协调员共享储存计划  
- [ ] 设置下一次检查的提醒  
- [ ] 归档旧的储存计划以供参考  
- [ ] 更新实验室的SOP中的储存程序  

## 常见问题及解决方法**

**分类错误：**
- ❌ **误认为稀释就安全** → 即使是稀释的酸/碱也需要适当的储存  
  - ✅ 应根据化学品的真正性质进行分类，而不仅仅是浓度  
- ❌ **忽略化学品名称中的关键词** → 复杂名称中可能遗漏危险性信息  
  - ✅ 检查化学品名称中是否包含多种危险性指示  
- ❌ **未考虑混合物** → 商业试剂可能含有多种成分  
  - ✅ 根据SDS中的混合物成分进行分类，并根据最危险的成分进行储存  
- ❌ **按用途而非危险性进行分类** → 例如将缓冲盐与酸一起储存  
  - ✅ 始终根据危险性进行储存分类  

**储存安排错误：**
- ❌ **分离不足** → 未保持至少3英尺的间距  
  - ✅ 使用物理屏障（如储存柜）将不兼容的化学品分开  
- ❌ **按字母顺序储存** → 例如将醋酸与丙酮放在一起  
  - ✅ 应始终优先考虑化学品的兼容性，而非字母顺序  
- ❌ **忽略泄漏防护** → 液体化学品未使用适当的二次防护措施  
  - ✅ 对于液体化学品，使用托盘或捆绑方式  
- ❌ **储存柜过于拥挤** → 阻挡了紧急设备的通道  
- ✅ 确保所有化学品和安全设备都能方便使用  

**文档记录错误：**
- **储存计划过时** → 化学品位置改变但储存计划未更新  
- ✅ 化学品搬迁后未更新储存计划  
- ✅ 未张贴不兼容性矩阵  
- ✅ 未张贴储存计划和危险警告  
- ✅ 无培训记录  
- ✅ 无法证明已经进行了安全培训  
- ✅ 未记录所有安全培训情况  
- ✅ 清单不完整，缺少某些化学品  

**操作错误：**
- ❌ **使用食品容器储存化学品** → 将化学品存放在饮料瓶中  
  - ✅ 应仅使用适当的化学品储存容器  
- ✅ 未进行过期监控 | 过期的过氧化物或其他易降解物质未及时处理  
- ✅ 未正确标注浓度 | 应标注浓度信息  
- ✅ 标签不准确 | 应使用完整的化学品名称和危险性符号  
- ✅ 堆放方式不当 | 阻挡了紧急设备的通道  

**故障排除：**

**问题：无法对化学品进行分类**  
- 症状：工具将明显危险的化学品分类为“其他”  
- 原因：  
  - 化学品名称不在关键词数据库中  
  - 化学品名称不常见或专有  
  - 化学品为混合物  
- 解决方法：  
  - 查看SDS中的正确化学品名称和危险性  
  - 使用CAS编号查询化学品类别  
  - 如遇不常见的化学品，咨询EHS  
  - 为实验室特有的化学品添加自定义分类规则  

**问题：识别出太多“不兼容”的化学品对**  
- 症状：在小实验室中识别出大量不兼容的化学品对  
- 原因：  
  - 不兼容性规则过于宽泛  
  - 化学品实际上已经分开存放但被标记为不兼容  
  - 未考虑浓度因素（如稀释溶液）  
- 解决方法：  
  - 重点关注实际的储存情况，而非理论上的不兼容性  
  - 检查化学品是否已经正确分离  
  - 考虑浓度因素（如非常稀释的溶液）  
  - 根据危险性的严重程度进行优先处理  

**问题：储存空间不足**  
- 症状：实际需要的储存柜数量超过可用空间  
- 原因：  
  - 随时间推移库存增加  
- 旧化学品处理不当  
- 购买了过多的化学品  
- 解决方法：  
  - 处理过期或不再需要的化学品  
  - 在可能的情况下与其他实验室共享化学品  
- 向EHS申请额外的储存设备  
  - 对昂贵的化学品实施“按需购买”政策  
- 考虑减少化学品库存  

**问题：实验室成员抗拒新储存系统**  
- 症状：重新组织后化学品位置错误  
- 原因：  
  - 培训不足  
- 系统过于复杂  
- 旧习惯难以改变  
- 解决方法：  
  - 提供清晰、实用的培训  
- 使储存位置直观易用  
- 在使用点张贴清晰的储存布局图  
- 提供温和的提醒和积极的反馈  
- 定期进行审计并提供反馈  

**问题：储存过程中发生化学反应**  
- 症状：出现反应迹象（变色、气体释放、发热）  
- 原因：  
  - 不兼容的化学品被放在一起  
  - 不稳定的化学品发生降解  
  - 储存过程中发生污染  
- 解决方法：  
  - 发现反应后立即疏散人员  
  - 联系EHS进行安全清理  
  | 审查储存安排以防止类似事件再次发生  
  | 检查其他可能受影响的化学品  
  | 记录事件并总结经验教训  

**问题：需要化学品时找不到**  
- 症状：化学品在清单中存在，但在实际位置找不到  
- 原因：  
  - 化学品位置更改后清单未更新  
- 标签错误或不清楚  
- 命名不一致（例如将“acetic acid”标记为“ethanoic acid”  
- 解决方法：  
  - 化学品移动后立即更新清单  
  | 使用标准化的、完整的化学品名称  
  | 实施条形码或二维码追踪  
  | 保持储存计划的最新状态并易于访问  

## 参考资料**

参考资料位于`references/`目录中：

- （目前该技能暂无参考文件）

**外部资源：**
- OSHA化学品储存指南：https://www.osha.gov/chemical-storage  
- NFPA 45：《实验室化学品防火规范》  
- 《实验室中的谨慎操作》（国家研究委员会）  
- MSDS在线搜索：https://www.msdsonline.com  

## 脚本**

脚本位于`scripts/`目录中：

- `main.py`：化学品分类和储存管理系统  

---

## 化学品储存快速参考

**通用规则：**
1. **将不兼容的化学品至少分开3英尺或使用物理屏障**  
2. **将酸性和碱性化学品分开储存**  
3. **将氧化剂远离易燃物和有机物**  
4. **将有毒化学品上锁并限制访问**  
5. **对液体腐蚀性化学品使用二次防护措施**  
6. **所有容器都需标注化学品名称和危险性**  
7. **切勿将化学品存放在食品容器中或靠近食品区**  
8. **确保可以方便地使用紧急设备（洗眼器、淋浴设施、出口）**  

**紧急联系电话：**
- 火灾：911  
- 中毒控制中心：1-800-222-1222  
- 校园EHS：[插入当地电话号码]  
- 化学品泄漏热线：[插入当地电话号码]  

## 参数**

| 参数 | 类型 | 默认值 | 是否必需 | 说明 |
|-----------|------|---------|----------|-------------|
| `--chemicals`, `-c` | 字符串 | 否 | 化学品列表（用逗号分隔） |
| `--check` | 字符串 | 否 | 检查两种化学品的兼容性 |
| `--list-groups`, `-l` | 标志 | 否 | 是否需要列出储存类别 |

## 使用方法**

### 基本使用方法：**

```bash
# Sort list of chemicals
python scripts/main.py --chemicals "HCl,NaOH,ethanol,H2O2"

# Check compatibility between two chemicals
python scripts/main.py --chemicals "HCl" --check "NaOH"

# List all storage groups
python scripts/main.py --list-groups
```

## 风险评估**

| 风险指标 | 评估内容 | 风险等级 |
|----------------|------------|-------|
| **代码执行** | 在本地执行Python脚本 | 低风险 |
| **网络访问** | 不使用外部API | 低风险 |
| **文件系统访问** | 不访问文件系统 | 低风险 |
| **数据暴露** | 不涉及敏感数据 | 低风险 |
| **安全风险** | 提供化学品安全指导 | 中等风险 |

## 安全性检查清单**

- [x] 无硬编码的凭证或API密钥  
- [x] 无文件系统访问权限  
- [x] 对化学品名称进行输入验证  
- [x] 输出不暴露敏感信息  
- [x] 错误信息经过处理  
- [x] 脚本在沙箱环境中执行  

## 先决条件**

```bash
# Python 3.7+
# No additional packages required (uses standard library)
```

## 评估标准**

### 成功指标  
- **成功将化学品分类到相应的储存类别**  
- **识别出不兼容的化学品对**  
- **提供储存建议**  
- **列出所有可用的储存类别**  

### 测试用例**
1. **化学品清单**：输入清单 → 按兼容性类别进行排序  
2. **兼容性检查**：两种化学品 → 显示兼容/不兼容的结果  
3. **未知化学品**：名称未知 → 分类为“其他”  

## 生命周期状态**

- **当前阶段**：活跃  
- **下一次审查日期**：2026-03-09  
- **已知问题**：无  
- **计划中的改进**：  
  - 扩充化学品数据库  
  - 添加SDS集成功能  
  - 支持自定义储存规则  

---

**最后更新时间**：2026-02-09  
**技能ID**：184  
**版本**：2.0（K-Dense Standard）