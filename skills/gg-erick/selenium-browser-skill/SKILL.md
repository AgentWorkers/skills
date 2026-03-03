---
name: selenium-automation
description: "该文档指导代理程序如何使用 Python、Selenium WebDriver 和 ChromeDriver 来执行高级网页自动化操作。"
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      - exec
      - write
    dependencies:
      system:
        - python3
        - chromedriver
        - google-chrome
      python:
        - selenium
    install: |
      pip install selenium
---
# Selenium自动化技能

您是使用Python和Selenium WebDriver进行网页自动化的专家。当用户要求您自动化浏览器操作、抓取网站内容或截取屏幕截图时，请根据以下代码片段编写相应的Python代码。

## 0. 安全性与执行规则
* **切勿自动运行脚本。**  
* 在编写完Python脚本（例如`automation.py`）后，必须先停止操作，并征得用户的明确许可才能运行该脚本。  
* 只有在用户表示“同意”或“批准”后，才能使用`exec`工具来执行脚本。  

## 1. 设置与ChromeDriver  
除非用户要求使用可见的浏览器界面，否则请始终将Chrome配置为无头模式（headless mode）运行。  
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)
```

## 2. 导航命令  
使用这些命令来打开网页并进行导航。  
```python
driver.get("[https://example.com](https://example.com)")
driver.refresh()
driver.back()
driver.forward()

current_url = driver.current_url
page_title = driver.title
```

## 3. 截取屏幕截图  
您可以截取整个可见窗口的屏幕截图，或者仅截取特定的HTML元素。  
```python
driver.save_screenshot("full_page.png")

from selenium.webdriver.common.by import By
element = driver.find_element(By.ID, "main-content")
element.screenshot("element.png")
```

## 4. JavaScript注入  
使用`execute_script`命令在浏览器中直接执行自定义JavaScript代码。  
```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
page_height = driver.execute_script("return document.body.scrollHeight;")

element = driver.find_element(By.ID, "hidden-button")
driver.execute_script("arguments[0].click();", element)

driver.execute_script("document.getElementById('cookie-banner').remove();")
```

## 5. 查找与操作元素  
使用这些标准命令来查找页面元素、点击按钮以及输入文本。  
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".submit-btn")))
button.click()

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("OpenClaw documentation")
search_box.send_keys(Keys.RETURN)

header = driver.find_element(By.TAG_NAME, "h1")
print("Text:", header.text)
print("Class attribute:", header.get_attribute("class"))
```

## 6. 关闭浏览器  
在脚本执行完毕之后，务必关闭浏览器以释放系统资源。  
```python
driver.quit()
```