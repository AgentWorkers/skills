---
name: megasquirt-tuner
description: Megasquirt ECU tuning and calibration using TunerStudio. Use when working with Megasquirt engine management systems for: (1) VE table tuning and fuel map optimization, (2) Ignition timing maps and spark advance, (3) Idle control and warmup enrichment, (4) AFR target tuning and closed-loop feedback, (5) Sensor calibration (TPS, MAP, CLT, IAT, O2), (6) Acceleration enrichment and deceleration fuel cut, (7) Boost control and launch control setup, (8) Datalog analysis and troubleshooting, (9) Base engine configuration and injector setup, (10) MSQ tune file analysis and safety review, (11) Any Megasquirt/TunerStudio ECU tuning tasks.
---

# 使用TunerStudio对Megasquirt发动机管理系统进行调校

本指南介绍了如何使用TunerStudio软件对Megasquirt发动机管理系统进行调校。

## 核心概念

### 所需燃油计算公式
Megasquirt通过以下公式计算燃油供给量：
```
Pulse Width = Required Fuel × VE% × MAP × AFR Target Correction × Air Density × Warmup × Accel Enrichment × Other Corrections
```

**所需燃油量**是指在100%混合气浓度（VE）、100kPa进气压力（MAP）和标准温度下的基础喷油器脉冲宽度。

### 主要调校表格

| 表格 | 用途 | 典型分辨率 |
|-------|---------|-------------------|
| 混合气浓度（VE）表 | 体积效率与转速/进气压力（RPM/MAP）的关系 | 16×16或12×12 |
| 空气燃油比（AFR）目标 | 所需的空燃比与转速/进气压力（RPM/MAP）的关系 | 12×12 |
| 火花提前角 | 点火正时与转速/进气压力（RPM/MAP）的关系 | 12×12或16×16 |
| 加热期燃油加浓 | 燃油修正量与冷却液温度的关系 | 10-20个点 |
| 基于转速传感器（TPS）的加速加浓 | 加速加浓量与TPS变化率（TPSdot）的关系 | 10-20个点 |
| 基于进气压力（MAP）的加速加浓 | 加速加浓量与MAP变化率（MAPdot）的关系 | 10-20个点 |

## 调校工作流程

### 1. 基础配置
调校前，请确认以下内容：
- 发动机排量和气缸数量
- 喷油器流量（cc/min或lb/hr）
- 喷油器的喷射方式（同时喷射、交替喷射或顺序喷射）
- 所需燃油计算结果是否与喷油器规格匹配
- 点火系统的输入/输出设置是否与硬件相符
- 触发轮和点火模式是否已正确配置

### 2. 传感器校准
调校前，请对传感器进行校准：
- **冷却液温度（CLT）**：在已知温度下设置电阻值
- **进气温度（IAT）**：与CLT类似
- **转速传感器（TPS）**：设置关闭和全开位置（0-100%）
- **进气压力（MAP）**：检查启动时的读数
- **氧传感器**：校准宽频控制器的输出范围

### 3. 混合气浓度（VE）表调校（速度密度）

**方法1：使用宽频氧传感器反馈**
1. 启用EGO（Engine Gas Oxygen）修正功能，修正幅度为±15-20%
2. 设置合理的AFR目标值
3. 使发动机在稳定状态下运行（固定转速/负载）
4. 记录EGO的修正百分比
5. 根据修正百分比反向调整混合气浓度（例如，若修正值为+10%，则将VE增加10%）
6. 保存设置并进入下一个调校参数

**方法2：根据测量的AFR值进行计算**
```
New VE = Current VE × (Measured AFR / Target AFR)
```

**调校顺序：**
1. 从怠速区域开始（600-1000 RPM，30-50kPa）
2. 轻度巡航状态（1500-2500 RPM，40-60kPa）
3. 部分油门加速状态
4. 全开油门高负载状态
5. 过渡区域

### 4. 空气燃油比（AFR）目标表
根据实际应用设置目标AFR值：

| 条件 | 目标AFR | Lambda值 |
|-----------|-----------|--------|
| 怠速 | 13.5-14.5 | 0.92-0.99 |
| 轻度巡航 | 14.5-15.5 | 0.99-1.06 |
| 部分油门 | 13.5-14.5 | 0.92-0.99 |
| 自然吸气（WOT） | 12.5-13.0 | 0.85-0.88 |
| 涡轮增压/机械增压（WOT） | 11.5-12.5 | 0.78-0.85 |

### 5. 点火正时
**基本设置：**
- 设置点火提前角（通常为10-20° BTDC）
- 设置怠速提前角（通常为15-25° BTDC）
- 根据发动机具体要求构建火花提前角表

**典型火花提前角表（自然吸气发动机）：**
- 低转速/高负载：10-20°
- 低转速/低负载：25-35°
- 高转速/高负载：25-35°
- 高转速/低负载：35-45°

**爆震处理：**
- 如果检测到爆震，每次减少1-2°的点火提前角
- 在易爆震区域增加燃油供给量
- 如有爆震传感器，可利用其反馈数据

### 6. 怠速控制
**怠速阀PWM设置：**
- 关闭位置：热怠速时的PWM占空比（通常为20-40%）
- 开启位置：冷启动时的PWM占空比（通常为60-80%）
- 启动时的PWM占空比（通常为50-70%）

**怠速目标转速表：**
- 热态：700-900 RPM
- 冷态（0°C）：1200-1500 RPM
- 在此范围内进行插值调整

### 7. 加热期燃油加浓
**启动后加浓：**
- 持续时间：30-200个循环（发动机转速）
- 加浓量：额外增加20-40%的燃油
- 在整个过程中逐渐减少加浓量

**加热期燃油加浓曲线：**
- -40°C：150-200%
- 0°C：120-140%
- 70°C（工作温度）：100%

### 8. 加速加浓
**基于转速传感器（TPS）的加浓：**
- 阈值：TPS变化率为5-10%/秒
- 加浓量：增加10-30%的燃油
- 减少加浓量的速度：0.5-2秒

**基于进气压力（MAP）的加浓（适用于MAP-dot系统）：**
- 阈值：MAP变化率为10-30 kPa/秒
- 加浓量随MAP变化率调整

**冷启动加浓倍数：**
- 在冷启动时增加加速加浓量（-20°C时增加1.5-3倍）

## 高级功能

### 增压控制
**开环控制：**
- 根据转速设置占空比

**闭环控制（如果支持）：**
- 使用PID参数控制废气门
- 根据转速和挡位设置目标增压值

### 发动机制动控制
- 设置最大转速限制（通常为4000-6000 RPM）
- 配置启动时的点火延迟（0-10° BTDC）
- 设置燃油/点火切断策略

### 挡位切换控制
- 挡位切换时保持油门开度不变
- 在挡位切换瞬间短暂切断燃油/点火
- 保持不同挡位间的增压效果

## 数据日志分析

### 需要记录的关键参数
| 参数 | 需要关注的内容 |
|-----------|---------------|
| 转速（RPM） | 系统稳定性，是否超过转速限制 |
| 进气压力（MAP） | 对油门输入的响应，是否存在泄漏 |
| 空气燃油比（AFR，宽频） | 与目标值的偏差 |
| EGO修正量 | 应在±10%范围内 |
| 冷却液温度（CLT） | 是否达到工作温度 |
| 进气温度（IAT） | 热量吸收效应 |
| 火花提前角 | 是否与设定值一致 |
| 喷油器脉冲宽度 | 是否在安全范围内 |
| 转速传感器（TPS） | 运行是否平稳，TPS变化率是否正常 |

### 常见问题及解决方法

**怠速时混合气过稀：**
- 增加基于TPS的加速加浓量
- 检查TPS变化率的敏感度

**减速时混合气过浓：**
- 启用减速时燃油切断功能（DFCO）
- 设置合适的TPS阈值（通常<10%）
- 设置高于怠速时的转速阈值

**怠速不稳：**
- 检查真空系统是否有泄漏
- 调整怠速PID参数
- 确认点火正时的稳定性

**高负载时爆震：**
- 减少受影响喷油器的点火提前角
- 增加混合气浓度（降低目标AFR值）

## TunerStudio使用说明

### 项目设置
1. 创建新项目 → 选择相应的固件版本（MS1、MS2、MS3）
2. 加载基础调校文件（.msq格式）或从默认设置开始
3. 连接到控制器（串行、USB或蓝牙）
4. 与控制器同步以加载当前设置

### 调校界面
- **基本/自定义调校**：浏览和编辑各种调校表格
- **实时数据**：实时监控系统参数
- **数据日志**：记录和回放调校过程

### 自动调校
- 启用VEAL（VE Analyze Live）功能，利用宽频氧传感器数据
- 设置可接受的AFR范围
- 遍历所有调校参数
- 审查并确认修改内容
- 完成后关闭自动调校功能

### 安全限制
**转速限制：**
- 软性限制：通过延迟点火提前角来控制转速
- 硬性限制：在超过最大转速时切断燃油/点火信号
- 设置超过目标压力的保护机制

**过压保护：**
- 当进气压力超过目标值时切断燃油供应
- 可选择切断点火信号

**混合气过稀时的处理：**
- 如果混合气过稀，关闭相关喷油器的燃油供应

## MSQ调校文件分析
该工具可以分析`.msq`格式的调校文件，识别潜在的安全问题、优化机会和配置错误。

### 使用分析工具
运行分析脚本以检查调校文件：

```bash
python3 scripts/analyze_msq.py your_tune.msq
```

或直接提供调校文件内容以进行分析。

### 提供MSQ文件的方法
**方法1：粘贴文件内容**（推荐）
- 在文本编辑器中打开`.msq`文件
- 复制全部内容
- 直接粘贴到聊天窗口中：例如：“分析此MSQ文件：[粘贴文件内容]”

**方法2：上传文件**
- 如果聊天界面支持文件附件，请上传`.msq`文件
- 工具会自动读取并分析文件

**方法3：提供文件路径**（适用于本地文件）
```bash
python3 scripts/analyze_msq.py /path/to/your/tune.msq
```

**脚本使用安全限制：**
- 仅接受扩展名为`.msq`的文件
- 禁止使用相对路径（如`../`）
- 不支持符号链接
- 文件必须是纯文本格式

**方法4：分享特定部分**
如果文件较大，可以仅分享感兴趣的部分：
- `[veTable1]`：混合气浓度表
- `[sparkTable1]`：点火提前角表
- `[afrTable1]`：空气燃油比目标表
- `[revLimiter]`：安全限制设置

### 分析示例
```
"Review this MSQ file for safety issues before I start my engine: [paste content]"

"Check my VE table - does anything look suspicious? [paste veTable section]"

"Analyze my ignition timing map for knock risk: [paste sparkTable section]"

"I just updated my AFR targets, review them: [paste afrTable section]"
```

### 分析内容
**安全检查：**
- 🚨 **严重问题**：可能导致发动机损坏的AFR目标值，过高的点火提前角
- ⚠️ **警告**：未配置转速限制，混合气浓度值异常，喷油器占空比过高

**配置审查：**
- 检查燃油计算是否合理
- 混合气浓度表的连续性和稳定性
- 根据发动机类型（自然吸气或涡轮增压）设置合适的AFR目标
- 点火正时范围及爆震风险
- 喷油器脉冲宽度是否合适
- 加热期燃油加浓曲线是否合理
- 安全限制是否设置正确

**优化建议：**
- 检查喷油器占空比的余量
- 混合气浓度表的连续性
- 点火正时设置的合理性

### 结果解读示例
```
📋 VE Table
----------------------------------------
  ⚠️ VE table has very low values (15.0) - check for empty/untuned cells
  📊 12 cells have >30% jumps from neighbors - consider smoothing
  ✓ VE table range: 15.0 - 105.0 (avg: 62.3)

📋 Ignition Timing
----------------------------------------
  ⚠️ High ignition advance (48°) - verify on dyno with knock detection
  ✓ Spark advance range: 8° - 48° BTDC

SUMMARY
============================================================
🚨 CRITICAL ISSUES: 0
⚠️  WARNINGS: 2
✓ Suggestions: 4
ℹ️  Notes: 1
```

### 常见问题及处理建议
**高优先级问题：**
- 未配置转速限制
- 高负载时混合气过稀（AFR目标值过高）
- 点火提前角过大（存在严重爆震风险）
- 喷油器占空比过高（超过90%）

**中等优先级问题：**
- 混合气浓度值过低或过高
- 相邻调校参数之间的变化过大（超过30%）
- 加热期燃油加浓曲线不完整
- 启动时的喷油器脉冲宽度不合适

**低优先级问题：**
- 点火正时设置过于保守，可能导致动力不足
- 混合气过浓
- 喷油器占空比过大

### 调校流程
1. **首次启动前：**
   ```
   You: "Review this base tune before I start the engine"
   AI: [Runs analysis, flags safety issues]
   ```

2. **修改后：**
   ```
   You: "I just updated my VE table, check it"
   AI: [Analyzes for anomalies, suggests smoothing]
   ```

3. **进行动态测试/赛道测试前：**
   ```
   You: "Review my tune before high load testing"
   AI: [Checks timing, AFR, safety limits, injector headroom]
   ```

## 参考资料
详细文档请参阅：
- [references/tunerstudio-reference.md](references/tunerstudio-reference.md) - 完整的TunerStudio使用手册
- [references/megasquirt-tuning-guide.md](references/megasquirt-tuning-guide.md) - 综合调校指南

## 快速参考公式
**喷油器占空比（Injector Duty Cycle）：**
```
DC% = (Injector PW / Injection Period) × 100
```
为确保安全，建议保持占空比在85%以下。

**所需燃油计算公式：**
```
Required Fuel (ms) = (Engine CC × 5) / (Number of Injectors × Injector CC/Min) × 2
```
（乘以2是因为每个循环有两个喷油动作）

**气流估算公式：**
```
MAF (g/s) ≈ (RPM × Displacement × VE% × MAP/100) / (2 × 60 × R × Temp)
```

## 安全检查清单
启动发动机前请确认：
- [ ] 喷油器流量设置正确
- [ ] 点火正时已通过点火测试工具验证
- [ ] 燃油泵已正常工作并保持压力
- [ ] 无燃油泄漏
- [ ] 宽频氧传感器已预热
- [ ] 紧急燃油/点火切断功能可用

调校过程中请注意：
- [ ] 如果有EGT（排气温度）传感器，请监控其数据
- [ ] 注意发动机是否出现爆震声
- [ ] 关注混合气浓度在切换挡位时的变化
- [ ] 调校参数的更改应保持保守
- [ ] 定期保存调校结果并记录版本信息