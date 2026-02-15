---
name: kenya-tax-rates
description: 计算肯尼亚员工的工资扣除项（包括PAYE、SHIF、NSSF和住房税），并使用2024/2025年的最新费率。
---

# 肯尼亚税率技能

使用最新的税率计算肯尼亚的工资税和扣除项，包括PAYE、SHIF、NSSF和住房税。

## 功能

- **PAYE**：五级累进税制（10%至35%）
- **SHIF**：2.75%的社会健康保险（2024年10月起取代NHIF）
- **NSSF**：双层养老金制度，金额根据日期自动调整
- **住房税**：1.5%的住房税
- **税收减免**：个人税收减免、保险费用减免、养老金减免、抵押贷款相关减免

## 使用方法

安装npm包：

```bash
npm install kenya-tax-rates
```

### 快速计算净工资

```typescript
import { getNetSalary } from 'kenya-tax-rates';

const netSalary = getNetSalary(100000);
// Returns ~KES 75,000
```

### 完整工资明细

```typescript
import { calculatePayroll } from 'kenya-tax-rates';

const result = calculatePayroll({
  grossSalary: 100000,
  pensionContribution: 5000,  // optional
  insurancePremium: 2000,     // optional
});

// Returns:
// {
//   grossSalary: 100000,
//   taxableIncome: 93590,
//   deductions: { shif: 2750, nssf: 2160, housingLevy: 1500, paye: 18594 },
//   netSalary: 74995,
//   employerContributions: { nssf: 2160, housingLevy: 1500 }
// }
```

### 个人计算器

```typescript
import { calculatePaye, calculateShif, calculateNssf, calculateHousingLevy } from 'kenya-tax-rates';

// PAYE with reliefs
const paye = calculatePaye(85000);

// SHIF (2.75%, min KES 300, no cap)
const shif = calculateShif(50000); // 1375

// NSSF (auto-detects 2024/2025 rates based on current date)
const nssf = calculateNssf(80000);

// Housing Levy (1.5%)
const levy = calculateHousingLevy(100000); // 1500
```

## 当前税率

### PAYE月度税率区间
| 收入（肯尼亚先令） | 税率 |
|--------------|------|
| 0 - 24,000 | 10% |
| 24,001 - 32,333 | 25% |
| 32,334 - 500,000 | 30% |
| 500,001 - 800,000 | 32.5% |
| 超过800,000 | 35% |

### NSSF缴纳额度（根据日期自动计算）
| 期间 | 下限 | 上限 | 最高缴纳额 |
|--------|-------------|-------------|------------------|
| 2024年2月 - 2025年1月 | 7,000肯尼亚先令 | 36,000肯尼亚先令 | 2,160肯尼亚先令 |
| 2025年2月起 | 8,000肯尼亚先令 | 72,000肯尼亚先令 | 4,320肯尼亚先令 |

### 税收减免
- 个人税收减免：每月2,400肯尼亚先令
- 保险费用减免：保费金额的15%，最高每月5,000肯尼亚先令
- 养老金减免：每月最高30,000肯尼亚先令

## API参考

| 函数 | 描述 |
|----------|-------------|
| `calculatePayroll(input)` | 计算包含所有扣除项的完整工资 |
| `getNetSalary(gross, date?)` | 快速计算净工资 |
| `calculatePaye(taxableIncome)` | 计算包含税收减免的PAYE金额 |
| `calculateShif(grossSalary)` | 计算SHIF保险费用 |
| `calculateNssf(earnings, date?)` | 计算NSSF的缴纳金额 |
| `calculateHousingLevy(grossSalary)` | 计算住房税（1.5%） |

## 来源

- npm: [kenya-tax-rates](https://www.npmjs.com/package/kenya-tax-rates)
- GitHub: [enjuguna/kenya-tax-rates](https://github.com/enjuguna/kenya-tax-rates)