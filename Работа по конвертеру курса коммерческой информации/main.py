import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 配置页面
st.set_page_config(
    page_title="货币转换器 | Конвертер валют",
    page_icon="💰",
    layout="centered"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-title {
        color: #FF6B6B;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-title {
        color: #4ECDC4;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        background-color: #FFD93D;
        color: #000000;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .bilingual-text {
        font-size: 1.1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 使用自定义样式的标题
st.markdown('<h1 class="main-title">🌍 全球货币转换器 | Глобальный конвертер валют</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-title">基于俄罗斯央行实时汇率 | На основе реальных курсов ЦБ РФ</h2>',
            unsafe_allow_html=True)


class CurrencyApp:
    def __init__(self):
        self.rates = self.get_currency_rates()

    def get_currency_rates(self):
        """获取货币汇率 | Получение курсов валют"""
        try:
            url = "https://www.cbr.ru/scripts/XML_daily.asp"
            response = requests.get(url)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                root = ET.fromstring(response.text)
                rates = {'RUB': 1.0}

                for currency in root.findall('Valute'):
                    code = currency.find('CharCode').text
                    value = currency.find('Value').text
                    nominal = currency.find('Nominal').text

                    if code and value and nominal:
                        rate = float(value.replace(',', '.')) / int(nominal)
                        rates[code] = rate

                st.success("🎯 汇率数据更新成功！最新汇率已加载 | Данные курсов обновлены! Актуальные курсы загружены")
                return rates
            else:
                return self.get_fallback_rates()

        except Exception as e:
            st.warning("📡 网络连接问题，使用本地汇率数据 | Проблемы с сетью, используются локальные данные")
            return self.get_fallback_rates()

    def get_fallback_rates(self):
        """备用汇率数据 | Резервные данные курсов"""
        return {
            'USD': 0.011, 'EUR': 0.010, 'GBP': 0.0085,
            'JPY': 1.45, 'CNY': 0.078, 'KZT': 5.0,
            'CAD': 0.014, 'AUD': 0.016, 'RUB': 1.0
        }

    def convert_currency(self, amount, from_curr, to_curr):
        """货币转换 | Конвертация валюты"""
        try:
            if from_curr == to_curr:
                return amount
            amount_in_rub = amount / self.rates[from_curr]
            result = amount_in_rub * self.rates[to_curr]
            return round(result, 2)
        except:
            return None


# 创建应用实例
app = CurrencyApp()

# 用户界面
st.markdown("### 💰 转换设置 | Настройки конвертации")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input(
        "📊 输入转换金额 | Введите сумму",
        min_value=0.01,
        value=100.0,
        step=1.0,
        help="请输入要转换的金额数量 | Пожалуйста, введите сумму для конвертации"
    )

with col2:
    currencies = sorted(app.rates.keys())
    from_currency = st.selectbox(
        "🔄 源货币 | Исходная валюта",
        options=currencies,
        index=currencies.index('RUB') if 'RUB' in currencies else 0,
        help="选择您要转换的原始货币 | Выберите исходную валюту"
    )

to_currency = st.selectbox(
    "🎯 目标货币 | Целевая валюта",
    options=currencies,
    index=currencies.index('USD') if 'USD' in currencies else 1,
    help="选择您要转换成的目标货币 | Выберите целевую валюту"
)

# 转换按钮
if st.button("🚀 立即转换 | Конвертировать сейчас", use_container_width=True):
    if amount > 0:
        result = app.convert_currency(amount, from_currency, to_currency)
        if result is not None:
            # 使用自定义样式的成功消息
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                color: white;
                text-align: center;
                margin: 1rem 0;
            '>
                <h2>💫 转换结果 | Результат конвертации</h2>
                <h1>{amount:,.2f} {from_currency} = {result:,.2f} {to_currency}</h1>
            </div>
            """, unsafe_allow_html=True)

            # 显示汇率信息
            reverse_rate = 1 / (app.rates[from_currency] / app.rates[to_currency])
            st.info(
                f"💱 当前汇率: 1 {to_currency} = {reverse_rate:.4f} {from_currency} | Текущий курс: 1 {to_currency} = {reverse_rate:.4f} {from_currency}")
        else:
            st.error("❌ 转换失败，请检查货币代码 | Ошибка конвертации, проверьте коды валют")
    else:
        st.error("⚠️ 请输入有效的金额 | Пожалуйста, введите корректную сумму")

# 显示支持的货币
st.markdown("### 🌐 支持货币列表 | Список поддерживаемых валют")
st.info(
    f"💡 当前支持 {len(currencies)} 种货币 | В настоящее время поддерживается {len(currencies)} валют: {', '.join(currencies[:10])}...")

# 添加一些统计信息
st.markdown("### 📈 汇率信息 | Информация о курсах")
col3, col4, col5 = st.columns(3)
with col3:
    st.metric("支持货币数量 | Количество валют", f"{len(currencies)} 种 | {len(currencies)} валют")
with col4:
    usd_rate = app.rates.get('USD', 0)
    usd_rub_rate = 1 / usd_rate if usd_rate else 0
    st.metric("USD/RUB | Доллар/Рубль", f"{usd_rub_rate:.2f}" if usd_rate else "N/A")
with col5:
    eur_rate = app.rates.get('EUR', 0)
    eur_rub_rate = 1 / eur_rate if eur_rate else 0
    st.metric("EUR/RUB | Евро/Рубль", f"{eur_rub_rate:.2f}" if eur_rate else "N/A")

# 汇率表格
st.markdown("### 📊 主要货币汇率 | Основные курсы валют")
major_currencies = ['USD', 'EUR', 'CNY', 'JPY', 'GBP', 'KZT']
rate_data = []
for curr in major_currencies:
    if curr in app.rates:
        rate_to_rub = 1 / app.rates[curr]
        rate_data.append({
            '货币 | Валюта': curr,
            '兑卢布汇率 | Курс к рублю': f"{rate_to_rub:.2f}",
            '兑美元汇率 | Курс к доллару': f"{(app.rates['USD'] / app.rates[curr]):.2f}" if 'USD' in app.rates else "N/A"
        })

if rate_data:
    import pandas as pd

    df = pd.DataFrame(rate_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# 使用说明
st.markdown("### 📝 使用说明 | Инструкция по использованию")
st.markdown("""
<div class="bilingual-text">
1. <strong>输入金额 | Введите сумму</strong> - 在上方输入要转换的金额 | Введите сумму для конвертации выше
</div>
<div class="bilingual-text">
2. <strong>选择货币 | Выберите валюты</strong> - 选择原始货币和目标货币 | Выберите исходную и целевую валюту
</div>
<div class="bilingual-text">
3. <strong>点击转换 | Нажмите конвертировать</strong> - 查看实时转换结果 | Посмотрите результат конвертации в реальном времени
</div>
""", unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 数据来源: 俄罗斯中央银行 | Источник данных: Центральный банк РФ</p>
    <p>🛠️ 使用 Streamlit 构建 | Построено на Streamlit</p>
    <p>⭐ 实时汇率更新 • 🔄 自动错误恢复 | Обновление курсов в реальном времени • Автовосстановление при ошибках</p>
</div>
""", unsafe_allow_html=True)

# 最后添加一个刷新按钮
if st.button("🔄 刷新汇率数据 | Обновить курсы валют", use_container_width=True):
    st.rerun()