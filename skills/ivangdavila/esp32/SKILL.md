---
name: ESP32
description: 避免常见的 ESP32 使用错误：GPIO 竞争冲突、WiFi 与 ADC2 的冲突、深度睡眠模式的相关问题，以及 FreeRTOS 的使用陷阱。
metadata: {"clawdbot":{"emoji":"📟","os":["linux","darwin","win32"]}}
---

## GPIO相关限制
- 某些GPIO引脚（GPIO0、GPIO2、GPIO12、GPIO15）会影响设备的启动模式。
- GPIO6至GPIO11引脚连接到闪存芯片上，切勿使用这些引脚，否则会导致系统立即崩溃。
- GPIO34至GPIO39引脚仅支持输入功能，不支持输出，且没有上拉/下拉电阻。
- 当WiFi功能开启时，ADC2无法使用；此时应使用ADC1（对应GPIO32至GPIO39引脚）。

## 深度睡眠模式
- 只有RTC相关的GPIO引脚可用于唤醒设备：GPIO0、GPIO2、GPIO4、GPIO12至GPIO15、GPIO25至GPIO27、GPIO32至GPIO39。
- 使用`RTC_DATA_ATTR`来保存需要在深度睡眠模式下保留的数据（因为常规RAM会在深度睡眠期间丢失）。
- 使用`esp_sleep_enable_ext0_wakeup()`来唤醒单个引脚；若需要唤醒多个引脚，则使用`ext1`。
- 设备从深度睡眠模式唤醒后，重新连接WiFi可能需要1至3秒的时间，请做好相应的延迟处理。

## 使用WiFi时的注意事项
- 在调用`WiFi.begin()`之前，必须先调用`WiFi.mode()`来设置WiFi的工作模式，因为模式会直接影响设备的运行行为。
- `WiFi.setAutoReconnect(true)`功能并不总是可靠的，建议在循环中实现重新连接逻辑。
- 使用`WiFi.onEvent()`进行事件驱动处理更为可靠，避免频繁调用`WiFi.status()`来检查WiFi状态。
- 使用静态IP地址比使用DHCP更快，连接速度可提升2至5秒。

## FreeRTOS相关注意事项
- FreeRTOS的默认堆栈空间较小，不足以支持复杂的程序逻辑（尤其是涉及`printf`或WiFi操作的代码），建议使用至少4096字节的堆栈空间。
- 任务监控机制会在5秒后触发，可以通过调用`vTaskDelay()`来手动触发监控。
- 使用`xTaskCreatePinnedToCore()`函数将任务绑定到特定的CPU核心上（例如，将WiFi任务绑定到核心0，将其他代码绑定到核心1）。
- `delay()`函数会立即返回给调度器，因此在任务中应使用`vTaskDelay(pdMS_TO_TICKS(ms))`来实现延迟。

## 内存管理
- 随着时间的推移，堆内存可能会变得碎片化，建议预先分配内存缓冲区以避免频繁的`malloc()`和`free()`操作。
- 可以使用`ESP.getFreeHeap()`函数来监控堆内存的使用情况，特别是在长时间运行的应用程序中。
- 某些开发板上提供了PSRAM（Programmable Secure Random Access Memory），可以使用`heap_caps_malloc(size, MALLOC_CAP_SPIRAM)`来分配内存。
- 字符串连接操作可能会导致堆内存碎片化，建议使用`reserve()`函数或字符数组来避免这种情况。

## 外设使用注意事项
- ESP32没有内置的`analogWrite()`函数，应使用`ledc`库来控制LED：`ledcSetup()`、`ledcAttachPin()`、`ledcWrite()`。
- I2C通信通常需要外部上拉/下拉电阻，因为内部上拉/下拉电阻的阻值可能不足以支持高速数据传输。
- SPI通信中的CS（Clock Select）引脚需要手动配置，`SPI.begin()`函数不会自动完成配置。
- UART0同时支持串行通信和USB功能，建议使用UART1或UART2来连接外部设备。

## OTA（Over-The-Air）更新
- OTA更新需要两个独立的存储分区，但默认的分区方案可能只有一个分区。请使用`ESP.getFreeSketchSpace()`函数检查是否有足够的空间进行更新。
- 如果内存不足，OTA更新可能会失败且不会产生任何提示；请在循环中处理这种情况。
- `ArduinoOTA`库在更新过程中可能会阻塞程序执行，建议将其放在非实时关键代码中处理。

## 电源管理
- 当电池供电时，系统会在电压降至约2.4V时触发保护机制（brown-out protection），此时可以调用`esp_brownout_disable()`来关闭相关保护功能。
- WiFi通信过程中峰值电流可能达到300mA，电源必须能够承受这种电流波动。
- 设备在深度睡眠模式下的功耗约为10µA；但如果启用了RTC相关的外设，功耗会增加。