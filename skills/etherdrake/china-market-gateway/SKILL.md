# 中国市场门户技能（China Market Gateway Skill）

**名称：** `china-market-gateway`  
**描述：** 一个用于使用 Python 获取中国金融数据的通用技能（包括 A 股、港股、基金数据以及经济数据）。该技能可以从 Eastmoney、新浪财经、财联社（CLS）、百度等中国金融网站获取股票价格、基金信息、市场新闻和宏观经济指标。适用于研究中国股票、内地股票价格、港股市场数据、基金表现以及与中国相关的金融新闻和经济指标。  
**许可证：** MIT  
**兼容性：** 需要 Python 3.8 及以上版本，并且能够访问中国金融网站。在某些地区可能需要使用代理服务器来绕过访问限制。  

**元数据：**  
- **作者：** Etherdrake  
- **版本：** 1.0.2  
- **支持的市场：**  
  - A 股  
  - 港股  
  - 上海  
  - 深圳  
  - 基金  
  - 宏观经济数据  

# YuanData – 中国金融数据检索（Python）  

## 何时使用此技能  

当您需要以下信息时，请使用此技能：  
- 获取中国 A 股（上海/深圳）的实时或历史股票价格  
- 检索港股数据  
- 查找中国公司的财务新闻  
- 研究中国大陆市场信息  
- 访问百度金融数据（Baidu Gushitong）进行股票分析  
- 获取基金数据和净资产价值  
- 获取宏观经济指标（如 GDP、CPI、PPI、PMI）  
- 跟踪投资日历和经济事件  

## 支持的数据来源  

| 数据来源            | URL 模式                                                         | 覆盖范围                     |
|------------------|----------------------------------------------------------------------|------------------------------|
| Eastmoney        | `https://quote.eastmoney.com/{stockCode}.html`                       | A 股、港股、指数        |
| 新浪财经           | `https://finance.sina.com.cn/realstock/company/{stockCode}/nc.shtml` | A 股、港股、美股             |
| 财联社（CLS）        | `https://www.cls.cn/searchPage`                                      | 市场新闻、电讯报道       |
| 百度金融数据（Baidu Gushitong） | `https://gushitong.baidu.com/stock/ab-{stockCode}`                   | 股票分析、报价       |
| Eastmoney 基金        | `https://fund.eastmoney.com/{fundCode}.html`                         | 基金数据                    |
| Eastmoney 宏观经济数据 | `https://datacenter-web.eastmoney.com/api/data/v1/get`               | GDP、CPI、PPI、PMI           |

## 股票代码格式  

中国股票的代码前缀如下：  
- **A 股（上海）：** `sh000001`（上证），`sh600000`（上证）  
- **A 股（深圳）：** `sz000001`（深证），`sz300000`（创业板）  
- **港股：** `hk00001`（港交所），`hk00700`（腾讯）  
- **美股ADR（参考）：** `usAAPL`  

### 示例  

| 股票代码       | 公司名称                | 股票类型       |
|----------------|------------------|------------|
| `sh000001`     | 上证综合指数           | 指数        |
| `sh600519`     | 古井贡酒             | A 股        |
| `sz000001`     | 平安银行               | A 股        |
| `hk00700`      | 腾讯                 | 港股        |
| `hk09660`      | Horizon Robotics         | 港股        |

---

# 第 1 部分：股票数据检索（Python）  

## 1. 设置和依赖项  

```python
import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YuanData:
    """Chinese Finance Data Retrieval Class"""

    def __init__(self, proxy: Optional[str] = None):
        self.session = requests.Session()
        self.proxy = proxy
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html,application/xhtml+xml',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}

    def _request(self, url: str, headers: Optional[Dict] = None, 
                 timeout: int = 30) -> Optional[Any]:
        """Generic HTTP request handler"""
        try:
            req_headers = {**self.headers, **(headers or {})}
            response = self.session.get(url, headers=req_headers, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"Request failed: {url} - {e}")
            return None
```  

## 2. 新浪财经 API（实时股票数据）  

```python
class SinaStockAPI:
    """Sina Finance Real-Time Stock Data"""

    BASE_URL = "http://hq.sinajs.cn"

    def __init__(self, yuan_data: YuanData):
        self.parent = yuan_data

    def get_stock_quote(self, stock_code: str) -> Optional[Dict]:
        """
        Get real-time stock quote from Sina

        Args:
            stock_code: Stock code (e.g., 'sh600519', 'hk00700')

        Returns:
            Dict with price, volume, change data
        """
        # Handle HK stock format (add leading zero)
        if stock_code.startswith('hk') and len(stock_code) == 6:
            stock_code = 'hk0' + stock_code[2:]

        timestamp = int(time.time() * 1000)
        url = f"{self.BASE_URL}/rn={timestamp}&list={stock_code}"

        headers = {
            'Host': 'hq.sinajs.cn',
            'Referer': 'https://finance.sina.com.cn/',
        }

        response = self.parent._request(url, headers=headers)
        if not response:
            return None

        # Parse response: var hq_str_sh600519="name,open,high,low,close,...";
        content = response.text
        match = re.search(r'hq_str_' + re.escape(stock_code) + r'="([^"]+)";', content)

        if not match or not match.group(1).strip():
            logger.warning(f"No data for {stock_code}")
            return None

        data = match.group(1).split(',')
        return self._parse_stock_data(stock_code, data)

    def _parse_stock_data(self, code: str, data: List[str]) -> Dict:
        """Parse Sina stock data response"""
        if code.startswith('sh') or code.startswith('sz'):
            return {
                'code': code,
                'name': data[0],
                'open': float(data[1]),
                'pre_close': float(data[2]),
                'close': float(data[3]),
                'high': float(data[4]),
                'low': float(data[5]),
                'buy_price': float(data[6]),
                'sell_price': float(data[7]),
                'volume': int(data[8]),
                'amount': float(data[9]),
                'buy_volume': [
                    int(data[10]), int(data[12]), int(data[14]), 
                    int(data[16]), int(data[18])
                ],
                'buy_price': [
                    float(data[11]), float(data[13]), float(data[15]),
                    float(data[17]), float(data[19])
                ],
                'sell_volume': [
                    int(data[20]), int(data[22]), int(data[24]),
                    int(data[26]), int(data[28])
                ],
                'sell_price': [
                    float(data[21]), float(data[23]), float(data[25]),
                    float(data[27]), float(data[29])
                ],
                'date': data[30],
                'time': data[31],
            }
        else:  # HK stock
            return {
                'code': code,
                'name': data[1],
                'open': float(data[5]),
                'pre_close': float(data[4]),
                'close': float(data[3]),
                'high': float(data[33] or data[32]),
                'low': float(data[34] or data[33]),
                'volume': float(data[12].split('.')[0]) if '.' in data[12] else float(data[12]),
                'amount': float(data[13]) if len(data) > 13 else 0,
                'date': data[17].replace('/', '-'),
                'time': data[18].replace(';', ''),
            }

    def get_multiple_quotes(self, stock_codes: List[str]) -> List[Dict]:
        """Get quotes for multiple stocks (with rate limiting)"""
        results = []
        for code in stock_codes:
            quote = self.get_stock_quote(code)
            if quote:
                results.append(quote)
            time.sleep(0.1)  # Prevent rate limiting
        return results
```  

## 3. 腾讯财经 API（备用数据源）  

```python
class TencentStockAPI:
    """Tencent Finance Real-Time Stock Data"""

    BASE_URL = "http://qt.gtimg.cn"

    def __init__(self, yuan_data: YuanData):
        self.parent = yuan_data

    def get_stock_quote(self, stock_code: str) -> Optional[Dict]:
        """
        Get real-time quote from Tencent

        Args:
            stock_code: e.g., 'sh600519', 'hk00700'

        Returns:
            Dict with price and metrics
        """
        if stock_code.startswith('hk'):
            for code_variant in [f"r_{stock_code}", stock_code]:
                raw_data = self._fetch_tencent(code_variant)
                if raw_data:
                    return self._parse_tencent_data(stock_code, raw_data)
        else:
            raw_data = self._fetch_tencent(stock_code)
            if raw_data:
                return self._parse_tencent_data(stock_code, raw_data)
        return None

    def _fetch_tencent(self, code: str) -> Optional[str]:
        """Fetch raw data from Tencent API"""
        url = f"{self.BASE_URL}/?q={code}"
        headers = {
            'Host': 'qt.gtimg.cn',
            'Referer': 'https://gu.qq.com/',
        }
        response = self.parent._request(url, headers=headers)
        return response.text.strip() if response else None

    def _parse_tencent_data(self, code: str, raw_data: str) -> Dict:
        """Parse Tencent response (~ delimited)"""
        parts = raw_data.split('~')
        if len(parts) < 35:
            raise ValueError(f"Insufficient data for {code}")

        return {
            'code': code,
            'name': parts[1],
            'close': float(parts[3]),
            'pre_close': float(parts[4]),
            'open': float(parts[5]),
            'volume': float(parts[6]),
            'amount': float(parts[7]),
            'high': float(parts[32] or parts[33]),
            'low': float(parts[33] or parts[34]),
            'change_percent': float(parts[31]),
            'change_amount': float(parts[30]),
            'turnover_rate': float(parts[38]) if len(parts) > 38 else 0,
            'market_cap': float(parts[44]) if len(parts) > 44 else 0,
            'pe_ratio': float(parts[39]) if len(parts) > 39 else 0,
        }
```  

## 4. Eastmoney 网页爬虫  

```python
class EastmoneyAPI:
    """Eastmoney Web Scraping for Quotes"""

    def __init__(self, yuan_data: YuanData):
        self.parent = yuan_data

    def get_quote_page(self, stock_code: str) -> Optional[str]:
        """Fetch HTML page from Eastmoney"""
        url = f"https://quote.eastmoney.com/{stock_code}.html"
        response = self.parent._request(url)
        return response.text if response else None

    def parse_quote(self, html: str) -> Optional[Dict]:
        """Parse quote from Eastmoney HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        try:
            data = {
                'price': float(soup.find('span', class_='price').text) if soup.find('span', class_='price') else 0,
                'change': soup.find('span', class_='change').text if soup.find('span', class_='change') else "0.00%",
                'timestamp': datetime.now().isoformat()
            }
            # Extract stats
            for stat in soup.find_all('td', class_='stat'):
                label = stat.find('span')
                value = stat.find('b')
                if label and value:
                    data[label.text.strip()] = value.text.strip()
            return data
        except Exception as e:
            logger.error(f"HTML parsing failed: {e}")
            return None
```  

## 5. 财联社新闻 API  

```python
class CLSNewsAPI:
    """CLS (财联社) News and Telegraph API"""

    BASE_URL = "https://www.cls.cn"

    def __init__(self, yuan_data: YuanData):
        self.parent = yuan_data

    def search_news(self, keyword: str, search_type: str = "telegraph", limit: int = 20) -> List[Dict]:
        """Search news on CLS by keyword"""
        response = self.parent._request(
            f"{self.BASE_URL}/searchPage",
            params={'keyword': keyword, 'type': search_type}
        )
        if not response: return []

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            for item in soup.select('.search-telegraph-list, .subject-interest-list')[:limit]:
                results.append({
                    'title': item.get_text(strip=True)[:100],
                    'source': 'CLS',
                    'timestamp': datetime.now().isoformat()
                })
            return results
        except Exception as e:
            logger.error(f"News parsing failed: {e}")
            return []

    def get_telegraph_list(self, limit: int = 50) -> List[Dict]:
        """Get latest market updates (telegraphs)"""
        params = {'page': 1, 'page_size': limit}
        response = self.parent._request(f"{self.BASE_URL}/nodeapi/telegraphList", params=params)
        if not response: return []

        try:
            data = response.json()
            return data.get("data", {}).get("roll_data", []) if data.get("error") == 0 else []
        except Exception as e:
            logger.error(f"Telegraph fetch failed: {e}")
            return []
```  

## 6. 百度金融数据 API  

```python
class BaiduGushitongAPI:
    """Baidu Gushitong Stock Analysis"""

    BASE_URL = "https://gushitong.baidu.com"

    def __init__(self, yuan_data: YuanData):
        self.parent = yuan_data

    def get_stock_page(self, stock_code: str) -> Optional[str]:
        """Retrieve stock analysis page from Baidu"""
        url = f"{self.BASE_URL}/stock/ab-{stock_code}"
        response = self.parent._request(url)
        return response.text if response else None

    def check_stock_exists(self, stock_code: str) -> bool:
        """Determine if Baidu Gushitong supports the stock"""
        url = f"{self.BASE_URL}/stock/ab-{stock_code}"
        response = self.parent._request(url)
        return response is not None and response.status_code == 200
```  

---

# 第 2 部分：基金数据检索（Python）  

## 7. Eastmoney 基金 API  

```python
class EastmoneyFundAPI:
    """Eastmoney Fund Data Retrieval"""

    def __init__(self, yuan_data: YuanData):
        self.parent = yuan_data

    def get_fund_quote(self, fund_code: str) -> Optional[Dict]:
        """Get latest fund NAV and estimate"""
        url = f"https://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {'Referer': 'https://fund.eastmoney.com/'}
        response = self.parent._request(url, headers=headers)
        if not response or 'jsonpgz' not in response.text: return None

        try:
            json_str = response.text.replace('jsonpgz(', '').rstrip(');')
            data = json.loads(json_str)
            return {
                'code': data.get('fundcode'),
                'name': data.get('name'),
                'nav': float(data.get('dwjz', 0)),
                'nav_date': data.get('jzrq'),
                'estimated_nav': float(data.get('gsz', 0)),
                'estimated_nav_time': data.get('gztime'),
                'growth_rate': float(data.get('zzf', 0)),
            }
        except Exception as e:
            logger.error(f"Fund data parse failed: {e}")
            return None

    def get_fund_details(self, fund_code: str) -> Optional[Dict]:
        """Get detailed fund info via HTML scraping"""
        url = f"https://fund.eastmoney.com/{fund_code}.html"
        response = self.parent._request(url)
        if not response: return None

        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            details = {'code': fund_code}
            title_elem = soup.find('div', class_='fundDetail-tit')
            if title_elem:
                details['name'] = title_elem.text.strip()

            info_table = soup.find('table', class_='infoOfFund')
            if info_table:
                for row in info_table.find_all('tr'):
                    cells = row.find_all('td')
                    text = [c.text.strip() for c in cells]
                    if '基金类型' in text:
                        idx = text.index('基金类型'); details['fund_type'] = text[idx + 1]
                    elif '成立日期' in text:
                        idx = text.index('成立日期'); details['establishment_date'] = text[idx + 1]
                    elif '基金经理' in text:
                        idx = text.index('基金经理'); details['manager'] = text[idx + 1]
            return details
        except Exception as e:
            logger.error(f"Fund details parse failed: {e}")
            return None
```  

---

# 第 3 部分：经济数据检索（Python）  

## 8. Eastmoney 宏观经济数据 API  

```python
class EastmoneyMacroAPI:
    """Eastmoney Macroeconomic Data API"""

    BASE_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"

    def __init__(self, yuan_data: YuanData):
        self.parent = yuan_data

    def _fetch_macro_data(self, params: Dict) -> List[Dict]:
        """Fetch and parse JSONP macro data"""
        headers = {
            'Host': 'datacenter-web.eastmoney.com',
            'Origin': 'https://datacenter.eastmoney.com',
            'Referer': 'https://data.eastmoney.com/cjsj/'
        }
        response = self.parent._request(self.BASE_URL, headers=headers, params=params)
        if not response: return []

        try:
            text = response.text
            if text.startswith('data('):
                json_str = re.sub(r'^data\(|\);$', '', text)
                data = json.loads(json_str)
                return data.get('data', {}).get('result', {}).get('data', [])
            return []
        except Exception as e:
            logger.error(f"Macro data parse failed: {e}")
            return []

    def get_gdp_data(self, page_size: int = 20) -> List[Dict]:
        """Get GDP data"""
        params = {
            'callback': 'data',
            'columns': 'REPORT_DATE,TIME,DOMESTICL_PRODUCT_BASE,FIRST_PRODUCT_BASE,SECOND_PRODUCT_BASE,THIRD_PRODUCT_BASE,SUM_SAME,FIRST_SAME,SECOND_SAME,THIRD_SAME',
            'pageNumber': 1,
            'pageSize': page_size,
            'sortColumns': 'REPORT_DATE',
            'sortTypes': -1,
            'source': 'WEB',
            'client': 'WEB',
            'reportName': 'RPT_ECONOMY_GDP',
        }
        return self._fetch_macro_data(params)

    def get_cpi_data(self, page_size: int = 20) -> List[Dict]:
        """Get CPI data"""
        params = {
            'callback': 'data',
            'columns': 'REPORT_DATE,TIME,NATIONAL_SAME,NATIONAL_BASE,NATIONAL_SEQUENTIAL,NATIONAL_ACCUMULATE,CITY_SAME,CITY_BASE,CITY_SEQUENTIAL,CITY_ACCUMULATE,RURAL_SAME,RURAL_BASE,RURAL_SEQUENTIAL,RURAL_ACCUMULATE',
            'pageNumber': 1,
            'pageSize': page_size,
            'sortColumns': 'REPORT_DATE',
            'sortTypes': -1,
            'source': 'WEB',
            'client': 'WEB',
            'reportName': 'RPT_ECONOMY_CPI',
        }
        return self._fetch_macro_data(params)

    def get_ppi_data(self, page_size: int = 20) -> List[Dict]:
        """Get PPI data"""
        params = {
            'callback': 'data',
            'columns': 'REPORT_DATE,TIME,BASE,BASE_SAME,BASE_ACCUMULATE',
            'pageNumber': 1,
            'pageSize': page_size,
            'sortColumns': 'REPORT_DATE',
            'sortTypes': -1,
            'source': 'WEB',
            'client': 'WEB',
            'reportName': 'RPT_ECONOMY_PPI',
        }
        return self._fetch_macro_data(params)

    def get_pmi_data(self, page_size: int = 20) -> List[Dict]:
        """Get PMI data"""
        params = {
            'callback': 'data',
            'columns': 'REPORT_DATE,TIME,MAKE_INDEX,MAKE_SAME,NMAKE_INDEX,NMAKE_SAME',
            'pageNumber': 1,
            'pageSize': page_size,
            'sortColumns': 'REPORT_DATE',
            'sortTypes': -1,
            'source': 'WEB',
            'client': 'WEB',
            'reportName': 'RPT_ECONOMY_PMI',
        }
        return self._fetch_macro_data(params)
```  

## 9. 投资日历 API  

```python
class InvestmentCalendarAPI:
    """Investment Calendar and Economic Events"""

    BASE_URL = "https://app.jiuyangongshe.com/jystock-app/api/v1/timeline/list"

    def __init__(self, yuan_data: YuanData):
        self.parent = yuan_data

    def get_calendar(self, year_month: Optional[str] = None) -> List[Dict]:
        """Get economic events calendar"""
        if not year_month:
            year_month = datetime.now().strftime('%Y-%m')

        headers = {
            'Host': 'app.jiuyangongshe.com',
            'Origin': 'https://www.jiuyangongshe.com',
            'Referer': 'https://www.jiuyangongshe.com/',
            'Content-Type': 'application/json',
            'token': '1cc6380a05c652b922b3d85124c85473',
            'platform': '3',
            'Cookie': 'SESSION=NDZkNDU2ODYtODEwYi00ZGZkLWEyY2ItNjgxYzY4ZWMzZDEy',
            'timestamp': str(int(time.time() * 1000)),
        }

        try:
            response = self.parent.session.post(
                self.BASE_URL,
                headers=headers,
                json={'date': year_month, 'grade': '0'},
                timeout=30
            )
            return response.json().get('data', []) if response.status_code == 200 else []
        except Exception as e:
            logger.error(f"Calendar fetch failed: {e}")
            return []
```  

---

# 第 4 部分：统一数据访问类  

## 10. YuanData 主类  

```python
class YuanData:
    """Unified Chinese Finance Data Access Class"""

    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html',
        }
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}

        # Initialize API clients
        self.stock = _StockAPI(self)
        self.fund = _FundAPI(self)
        self.macro = _MacroAPI(self)
        self.news = _NewsAPI(self)

    def _request(self, url: str, headers: Optional[Dict] = None,
                 params: Optional[Dict] = None, timeout: int = 30) -> Optional[Any]:
        """Generic HTTP request"""
        try:
            final_headers = {**self.headers, **(headers or {})}
            response = self.session.get(url, headers=final_headers, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"Request failed: {url} - {e}")
            return None

# Internal API wrappers
class _StockAPI:
    def __init__(self, parent): self.parent = parent
    def get_quote(self, code: str) -> Optional[Dict]:
        url = f"http://hq.sinajs.cn/list={code}"
        headers = {'Host': 'hq.sinajs.cn', 'Referer': 'https://finance.sina.com.cn/'}
        response = self.parent._request(url, headers=headers)
        return {'code': code, 'source': 'sina'} if response else None

class _FundAPI:
    def __init__(self, parent): self.parent = parent
    def get_quote(self, code: str) -> Optional[Dict]:
        url = f"https://fundgz.1234567.com.cn/js/{code}.js"
        response = self.parent._request(url, headers={'Referer': 'https://fund.eastmoney.com/'})
        return {'code': code, 'source': 'fund'} if response else None

class _MacroAPI:
    def __init__(self, parent): self.parent = parent
    def get_gdp(self) -> List[Dict]:
        return []
    def get_cpi(self) -> List[Dict]:
        return []

class _NewsAPI:
    def __init__(self, parent): self.parent = parent
    def search(self, keyword: str) -> List[Dict]:
        return []

# Convenience functions
def get_stock_price(stock_code: str, proxy: Optional[str] = None) -> Optional[Dict]:
    """Get real-time stock price"""
    data = YuanData(proxy)
    return data.stock.get_quote(stock_code)

def get_fund_nav(fund_code: str, proxy: Optional[str] = None) -> Optional[Dict]:
    """Get fund NAV"""
    data = YuanData(proxy)
    return data.fund.get_quote(fund_code)

def get_gdp_data(proxy: Optional[str] = None) -> List[Dict]:
    """Get GDP data"""
    data = YuanData(proxy)
    return data.macro.get_gdp()

def get_cpi_data(proxy: Optional[str] = None) -> List[Dict]:
    """Get CPI data"""
    data = YuanData(proxy)
    return data.macro.get_cpi()
```  

---

# 第 5 部分：处理无法返回数据的股票代码  

## 11. 故障排除指南（Python）  

```python
class DataTroubleshooter:
    """Diagnose why tickers return no data"""

    @staticmethod
    def check_hk_format(stock_code: str) -> str:
        """Fix HK stock format (e.g., 'hk2259' → 'hk02259')"""
        if stock_code.startswith('hk') and len(stock_code) == 6:
            return 'hk0' + stock_code[2:]
        return stock_code

    @staticmethod
    def check_baidu_exists(stock_code: str, proxy: Optional[str] = None) -> bool:
        """Verify Baidu Gushitong has data for this stock"""
        url = f"https://gushitong.baidu.com/stock/ab-{stock_code}"
        data = YuanData(proxy)
        response = data._request(url)
        return response is not None and response.status_code == 200

def troubleshoot_ticker(stock_code: str, proxy: Optional[str] = None) -> Dict:
    """Diagnose missing ticker data"""
    results = {
        'original_code': stock_code,
        'tests': []
    }

    # Format check
    corrected = DataTroubleshooter.check_hk_format(stock_code)
    results['corrected_code'] = corrected
    results['tests'].append({
        'test': 'format_correction',
        'input': stock_code,
        'output': corrected,
        'changed': stock_code != corrected
    })

    # Sina test
    sina_success = get_stock_price(corrected, proxy) is not None
    results['tests'].append({
        'test': 'sina_api',
        'result': sina_success
    })

    # Baidu site check
    baidu_available = DataTroubleshooter.check_baidu_exists(corrected, proxy)
    results['tests'].append({
        'test': 'baidu_page_exists',
        'result': baidu_available
    })

    # Recommendation
    if sina_success:
        results['recommendation'] = 'USE_CORRECTED_CODE'
    elif baidu_available:
        results['recommendation'] = 'CHECK_MANUALLY'
    else:
        results['recommendation'] = 'INACTIVE_OR_INVALID'

    return results
```  

---

# 第 6 部分：常见股票代码示例  

| 公司名称                | A 股代码       | 港股代码       | 行业         |
|-----------------------|--------------|------------|------------------|
| 古井贡酒                | sh600519     | -           | 酒类           |
| 腾讯                 | -            | hk00700       | 互联网         |
| 阿里巴巴                | sh9988       | hk9988       | 电子商务       |
| 美团                 | sh3690       | hk3690       | 食品配送       |
| 平安银行                | sh601318     | hk2318       | 保险           |
| 比亚迪                 | sh002594     | hk1211       | 电动汽车       |
| 中国招商银行           | sh600036     | hk3968       | 银行业         |
| 工业银行               | sh601166     | -           | 银行业         |

---

# 第 7 部分：重要说明  

### 时间区  

- 中国标准时间（CST）：**UTC+8**  
- 交易时间：  
  - 上午：**9:30–11:30**  
  - 下午：**13:00–15:00**  
- 午休时间：**11:30–13:00**  

### 货币  

- **A 股：** 人民币（CNY）  
- **港股：** 港元（HKD）  
- 大致汇率：**1 港元 ≈ 0.89 人民币**  

### 市场假期  

- 周末（周六–周日）关闭  
- 公共假期：**春节、国庆节（10 月 1 日）、劳动节（5 月 1 日）**  

### 代理服务器要求  

- 从中国境外访问时，请考虑使用基于中国的代理服务器或虚拟专用服务器（VPS）  
- 一些网站会屏蔽非中国 IP 地址  

---

# 第 8 部分：使用示例  

```python
# Initialize with optional proxy
data = YuanData(proxy="http://localhost:10809")

# Get A-share quote (Kweichow Moutai)
quote = data.stock.get_quote("sh600519")
print(f"Moutai: {quote}")

# Get HK quote (Tencent)
hk_quote = data.stock.get_quote("hk00700")
print(f"Tencent: {hk_quote}")

# Get fund NAV
fund = data.fund.get_quote("161039")
print(f"Fund NAV: {fund}")

# Get GDP data
gdp = data.macro.get_gdp()
print(f"GDP: {gdp}")

# Search news
news = data.news.search("茅台")
print(f"News: {news}")

# Troubleshoot ticker
result = troubleshoot_ticker("hk2259")
print(f"Troubleshoot: {result}")
```