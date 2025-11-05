import requests
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET


class CurrencyConverter:
    def __init__(self):
        self.rates = {}
        self.last_update = None
        self.base_currency = 'RUB'
        self.load_currency_rates()

    def load_currency_rates(self):
        """从俄罗斯央行网站获取货币汇率"""
        try:
            url = 'https://www.cbr.ru/scripts/XML_daily.asp'
            response = requests.get(url)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                root = ET.fromstring(response.text)
                date_str = root.attrib['Date']
                self.last_update = datetime.strptime(date_str, '%d.%m.%Y')

                for currency in root.findall('Valute'):
                    code = currency.find('CharCode').text
                    nominal = int(currency.find('Nominal').text)
                    value = float(currency.find('Value').text.replace(',', '.'))
                    self.rates[code] = value / nominal

                self.rates['RUB'] = 1.0
                print(f"成功加载 {len(self.rates)} 种货币汇率")
            else:
                print(f"获取数据失败，状态码: {response.status_code}")
                self.load_fallback_rates()

        except Exception as e:
            print(f"获取汇率数据时出错: {e}")
            self.load_fallback_rates()

    def load_fallback_rates(self):
        """备用汇率数据"""
        fallback_rates = {
            'USD': 0.011, 'EUR': 0.010, 'GBP': 0.0085,
            'JPY': 1.45, 'CNY': 0.078, 'RUB': 1.0,
            'KZT': 5.0, 'BYN': 0.035, 'UAH': 0.4
        }
        self.rates = fallback_rates
        self.last_update = datetime.now()
        print("使用备用汇率数据")

    def get_available_currencies(self):
        """获取可用的货币列表"""
        return sorted(self.rates.keys())

    def convert(self, amount, from_currency, to_currency):
        """货币转换"""
        try:
            if from_currency not in self.rates or to_currency not in self.rates:
                return None, "货币代码不存在"

            amount_in_rub = amount / self.rates[from_currency]
            converted_amount = amount_in_rub * self.rates[to_currency]

            return round(converted_amount, 2), None

        except Exception as e:
            return None, f"转换错误: {str(e)}"

    def get_all_rates(self):
        """获取所有汇率"""
        return self.rates.copy()
