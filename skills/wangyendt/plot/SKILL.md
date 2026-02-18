---
name: pywayne-plot
description: 增强型频谱图可视化工具，适用于时频分析。适用于生成频谱图、进行频谱分析或绘制时频图，适用于包括惯性测量单元（IMU）数据（加速度计、陀螺仪）、生理信号（脉搏血氧饱和度、心电图、呼吸信号）、振动分析以及音频处理等多种信号类型。支持频率单位转换（Hz、bpm、kHz），多种归一化模式（全局归一化/局部归一化/不归一化），并支持MATLAB风格的Parula颜色映射。
---
# Pywayne Plot

这是一个专为专业时频分析设计的增强型频谱图可视化工具。

## 快速入门

```python
import matplotlib.pyplot as plt
from pywayne.plot import regist_projection, parula_map
import numpy as np

# Register custom projection
regist_projection()

# Create spectrogram
fig, ax = plt.subplots(subplot_kw={'projection': 'z_norm'})
spec, freqs, t, im = ax.specgram(
    x=signal_data,
    Fs=100,
    NFFT=128,
    noverlap=96,
    cmap=parula_map,
    scale='dB'
)
ax.set_ylabel('Frequency (Hz)')
plt.colorbar(im, label='Magnitude (dB)')
plt.show()
```

## 函数

### regist_projection

用于注册自定义的 `SpecgramAxes` 投影方式。在使用增强型频谱图功能之前必须调用此函数。

```python
from pywayne.plot import regist_projection
regist_projection()
```

### SpecgramAxes.specgram

提供具有高级功能的增强型频谱图。

**关键参数：**

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `NFFT` | FFT 窗长（点数） | 256 |
| `Fs` | 采样频率（Hz） | 2 |
| `noverlap` | 窗口之间的重叠点数 | 128 |
| `cmap` | 色彩映射（推荐使用 `parula_map`） | - |
| `mode` | 'psd', 'magnitude', 'angle', 'phase' | 'psd' |
| `scale` | 'dB' 或 'linear' | 'dB' |
| `normalize` | 'global', 'local', 'none' | 'global' |
| `freq_scale` | 频率缩放因子 | 1.0 |
| `Fc` | 中心频率偏移（Hz） | 0 |

**返回值：**
- `spec` - 二维频谱图数组（n_freqs, n_times）
- `freqs` - 频率轴数组
- `t` - 时间轴数组
- `im` - matplotlib 图像对象（用于颜色条）

### get_specgram_params

根据信号特性自动推荐 STFT 参数。

```python
from pywayne.plot import get_specgram_params

params = get_specgram_params(
    signal_length=10000,
    sampling_rate=100,
    time_resolution=0.1  # or freq_resolution=0.5
)
# Returns: NFFT, noverlap, actual_freq_res, actual_time_res, n_segments
```

### parula_map

一种基于 MATLAB 的、具有良好视觉均匀性的色彩映射函数，适用于科学可视化。

```python
from pywayne.plot import parula_map
plt.imshow(data, cmap=parula_map)
```

## 使用示例

### IMU 信号分析

```python
fs = 100  # Sampling rate
win_time, step_time = 1, 0.1

fig, ax = plt.subplots(subplot_kw={'projection': 'z_norm'})
spec, freqs, t, im = ax.specgram(
    x=acc_data,
    Fs=fs,
    NFFT=int(win_time * fs),
    noverlap=int((win_time - step_time) * fs),
    scale='dB',
    cmap=parula_map
)
ax.set_ylabel('Frequency (Hz)')
ax.set_ylim(0, 30)
```

### 生理信号（PPG - 心率）

```python
# Convert Hz to bpm for heart rate visualization
fig, ax = plt.subplots(subplot_kw={'projection': 'z_norm'})
spec, freqs, t, im = ax.specgram(
    x=ppg_signal,
    Fs=100,
    NFFT=400,
    noverlap=300,
    freq_scale=60,  # Hz -> bpm
    scale='dB'
)
ax.set_ylabel('Heart Rate (bpm)')
ax.set_ylim(40, 180)
```

### 带全局归一化的振动分析

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'z_norm'})
spec, freqs, t, im = ax.specgram(
    x=vibration_data,
    Fs=1000,
    NFFT=1024,
    noverlap=512,
    scale='linear',
    normalize='global'
)
plt.colorbar(im, label='Normalized Magnitude')
```

### 使用零填充的高分辨率分析

```python
fig, ax = plt.subplots(subplot_kw={'projection': 'z_norm'})
spec, freqs, t, im = ax.specgram(
    x=signal,
    Fs=100,
    NFFT=100,
    pad_to=512,  # Zero-pad for smoother spectrum
    noverlap=80,
    scale='dB'
)
```

## 缩放和归一化模式

### 缩放模式

| 模式 | 描述 | 使用场景 |
|------|-------------|----------|
| `dB` | 对数刻度（PSD 时为 10*log10，幅度时为 20*log10） | 适用于动态范围较大的信号 |
| `linear` | 线性幅度 | 用于直接比较幅度 |

### 归一化模式（仅适用于 `scale='linear'`）

| 模式 | 描述 | 使用场景 |
|------|-------------|----------|
| `global` | 全局归一化（Z 到 Z 的最大值） | 用于跨时间比较信号强度 |
| `local` | 每列归一化到 [0,1] | 用于关注随时间变化的频率成分 |
| `none` | 无归一化 | 显示原始频谱图值 |

## 频率缩放

| freq_scale | 单位 | 使用场景 |
|------------|------|----------|
| 1.0 | Hz | 默认值，适用于大多数信号 |
| 60 | bpm | 用于转换心率、呼吸频率 |
| 0.001 | kHz | 用于音频信号 |

**示例：`freq_scale=60` 会将 2 Hz 转换为 120 bpm**

## 分辨率指南

- **频率分辨率**：Δf = Fs / NFFT
- **时间分辨率**：Δt = (NFFT - overlap) / Fs
- **权衡**：无法同时实现高频率分辨率和时间分辨率

建议使用 `get_specgram_params()` 自动计算最佳参数。

## 交互式分析

```python
spec, freqs, t, im = ax.specgram(...)

def on_click(event):
    if event.xdata and event.inaxes == ax:
        time_idx = np.argmin(np.abs(t - event.xdata))
        plt.figure()
        plt.plot(freqs, spec[:, time_idx])
        plt.title(f'FFT at t={event.xdata:.2f}s')
        plt.show()

fig.canvas.mpl_connect('button_press_event', on_click)
```

## 应用领域

- **IMU 数据**：加速度计和陀螺仪数据分析
- **生理信号**：PPG（心率）、ECG、呼吸信号
- **振动分析**：机械设备故障诊断
- **音频处理**：语音和音频频谱分析

## 注意事项

- 使用 `projection='z_norm'` 之前，请务必先调用 `regist_projection()`
- 建议使用 `parula_map` 以获得最佳的视觉均匀性
- `dB` 模式会自动处理对数值（如 0）
- 为提高 FFT 效率，请将 `NFFT` 设置为 2 的幂次