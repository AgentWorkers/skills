---
name: stm32-cubemx
description: "STM32CubeMX命令行界面（CLI）用于配置引脚、外设、DMA（直接内存访问）、中断以及生成相应的代码。使用场景包括：  
1. 添加或修改STM32外设的配置；  
2. 配置USART（串行通信接口）、SPI（串行外设接口）、I2C（串行接口）、ADC（模数转换器）和TIM（定时器）等外设；  
3. 设置DMA和中断的相关参数；  
4. 生成CMake或GCC项目所需的代码文件。  
默认的目标微控制器为STM32F103C8Tx。"
---
# STM32CubeMX 命令行界面（CLI）操作

## 环境设置

```bash
# STM32CubeMX path (modify based on your installation)
CUBEMX=/path/to/STM32CubeMX/STM32CubeMX

# Project path (adjust for your project)
PROJECT_DIR=/path/to/your/project
IOC_FILE=$PROJECT_DIR/your_project.ioc
SCRIPT_FILE=$PROJECT_DIR/cube_headless.txt
```

## 核心工作流程

```
1. Modify IOC config file → 2. Run CLI to generate code → 3. CMake build verification
```

### 第1步：修改 `.ioc` 文件

编辑 `.ioc` 文件以添加或修改外设配置。

**关键配置部分：**
- `Mcu.IP0=XXX` - 外设IP地址列表，`Mcu.IPNb` 表示外设的数量
- `Mcu.Pin0=PAx` - 引脚列表，`Mcu.PinsNb` 表示引脚的数量
- `XXX.Signal=YYY` - 引脚信号映射
- `ProjectManager.functionlistsort` - 初始化函数列表

### 第2步：生成代码

```bash
# Headless mode (recommended)
$CUBEMX -q $SCRIPT_FILE

# Script file content
cat > $SCRIPT_FILE << 'EOF'
config load /path/to/your/project/your_project.ioc
project generate
exit
EOF
```

### 第3步：构建与验证

```bash
cd $PROJECT_DIR
rm -rf build/Debug
cmake --preset Debug
cmake --build build/Debug
```

## 命令行界面（CLI）命令参考

| 命令 | 功能 | 例 |
|------|------|------|
| `config load <路径>` | 加载 `.ioc` 配置文件 | `config load /path/to/project.ioc` |
| `config save <路径>` | 保存 `.ioc` 配置文件 | `config save /path/to/project.ioc` |
| `project generate` | 生成完整项目代码 | `project generate` |
| `project toolchain <名称>` | 设置工具链 | `project toolchain CMake` |
| `project path <路径>` | 设置项目路径 | `project path /path/to/project` |
| `project name <名称>` | 设置项目名称 | `project name MyProject` |
| `load <mcu>` | 加载指定的MCU | `load STM32F103C8Tx` |
| `setDriver <IP> <HAL\|LL>` | 设置驱动程序类型 | `setDriver ADC LL` |
| `exit` | 退出程序 | `exit` |

## 常见外设配置模板

### USART + DMA

详细配置请参阅 [references/USART_DMA.md](references/USART_DMA.md)

```ini
# Add IP
Mcu.IP6=USART2
Mcu.IPNb=7

# Pin configuration
PA2.Signal=USART2_TX
PA3.Signal=USART2_RX

# USART2 parameters
USART2.BaudRate=115200
USART2.Dmaenabledrx=1
USART2.Dmaenabledtx=1

# DMA configuration
Dma.Request0=USART2_RX
Dma.Request1=USART2_TX
Dma.USART2_RX.0.Instance=DMA1_Channel6
Dma.USART2_TX.1.Instance=DMA1_Channel7

# Interrupts
NVIC.USART2_IRQn=true\:0\:0\:false\:false\:true\:true\:true\:true
```

### ADC 数据采集

```ini
# Add ADC1
Mcu.IP0=ADC1

# ADC configuration
ADC1.Channel-1\#ChannelRegularConversion=ADC_CHANNEL_5
ADC1.Rank-1\#ChannelRegularConversion=1
ADC1.SamplingTime-1\#ChannelRegularConversion=ADC_SAMPLETIME_1CYCLE_5
ADC1.NbrOfConversionFlag=1
ADC1.master=1

# Pin
PA5.Signal=ADCx_IN5
SH.ADCx_IN5.0=ADC1_IN5,IN5
```

### TIM/PWM

```ini
# TIM3 configuration
TIM3.Channel-PWM\ Generation1\ CH1=PWM_CHANNEL1
TIM3.Channel-PWM\ Generation2\ CH2=PWM_CHANNEL2
TIM3.IPParametersWithoutCheck=Prescaler,Period

# Pins
PA6.Signal=TIM3_CH1
PA7.Signal=TIM3_CH2
```

## STM32F103C8T6 资源映射

### USART

| 外设 | 发送引脚（TX） | 接收引脚（RX） | DMA 发送通道（DMA TX） | DMA 接收通道（DMA RX） |
|------|-----|-----|--------|--------|
| USART1 | PA9 | PA10 | DMA1_Ch4 | DMA1_Ch5 |
| USART2 | PA2 | PA3 | DMA1_Ch7 | DMA1_Ch6 |
| USART3 | PB10 | PB11 | DMA1_Ch2 | DMA1_Ch3 |

### ADC通道

| 通道 | 引脚 | ADC通道 | 对应引脚 |
|------|------|------|------|
| IN0 | PA0 | IN5 | PA5 |
| IN1 | PA1 | IN6 | PA6 |
| IN2 | PA2 | IN7 | PA7 |
| IN3 | PA3 | IN8 | PB0 |
| IN4 | PA4 | IN9 | PB1 |

### TIM通道

| 定时器 | 通道（CH1） | 通道（CH2） | 通道（CH3） | 通道（CH4） |
|--------|-----|-----|-----|-----|
| TIM1 | PA8 | PA9 | PA10 | PA11 |
| TIM2 | PA0/PA5/PA15 | PA1/PB3 | PA2 | PA3 |
| TIM3 | PA6/PB4 | PA7/PB5 | PB0 | PB1 |
| TIM4 | PB6 | PB7 | PB8 | PB9 |

## 故障排除

### 问题1：CLI命令执行无效
**原因**：路径必须是绝对路径

```bash
# Wrong
./STM32CubeMX -q script.txt
# Correct
/path/to/STM32CubeMX/STM32CubeMX -q /path/to/project/script.txt
```

### 问题2：生成的代码缺少初始化函数
**原因**：`functionlistsort` 没有包含相应的初始化函数

```ini
# Add initialization function
ProjectManager.functionlistsort=...,N-MX_XXX_Init-XXX-false-HAL-true
```

### 问题3：未生成外设相关代码
**检查事项**：
1. 该外设的IP地址是否在 `Mcu.IPx` 列表中？
2. `Mcu.IPNb` 的值是否正确？
3. 相关引脚的信号配置是否完成？

### 问题4：DMA通道未配置
**解决方法**：启用相应的外设DMA参数

```ini
USART2.Dmaenabledrx=1
USART2.Dmaenabledtx=1
```

## 快速参考

```bash
# Complete workflow
cd /path/to/your/project
# 1. Edit IOC file
# 2. Generate code
/path/to/STM32CubeMX/STM32CubeMX -q cube_headless.txt
# 3. Build
cmake --preset Debug && cmake --build build/Debug
# 4. Check size
arm-none-eabi-size build/Debug/your_project.elf
```

## 参考资料

- [references/USART_DMA.md](references/USART_DMA.md) - 完整的USART + DMA配置指南
- [references/IOC_structure.md](references/IOC_structure.md) - `.ioc` 文件结构说明
- [UM1718 STM32CubeMX 用户手册](https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-description-stmicroelectronics.pdf)