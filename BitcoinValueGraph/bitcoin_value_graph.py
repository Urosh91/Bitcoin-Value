from urllib.request import urlopen
import pygal
from pygal.style import DarkGreenBlueStyle
import json
import platform
import getpass
import webbrowser

# url with Bitcoin USD value in JSON format
url = "https://api.coindesk.com/v1/bpi/historical/close.json"

bitcoin_data = urlopen(url)

bitcoin_data_in_bytes = bitcoin_data.read()

bitcoin_dict = json.loads(bitcoin_data_in_bytes)

bitcoin_dict_cleaned = bitcoin_dict["bpi"]

# url with current exchange values in JSON format
url_2 = "https://api.fixer.io/latest"

exchange_rates_data = urlopen(url_2)

exchange_rates_data_in_bytes = exchange_rates_data.read()

exchange_rates_dict = json.loads(exchange_rates_data_in_bytes)

exchange_rates_dict_cleaned = exchange_rates_dict["rates"]

exchange_rates_USD_to_EUR_ratio = exchange_rates_dict_cleaned["USD"]

dates = []
closing_prices_in_usd = []
closing_prices_in_eur = []

for key, value in bitcoin_dict_cleaned.items():
    dates.append(key)
    closing_prices_in_usd.append(value)

for value_in_usd in closing_prices_in_usd:
    value_in_eur = value_in_usd / exchange_rates_USD_to_EUR_ratio
    closing_prices_in_eur.append(value_in_eur)

line_chart = pygal.Line(style=DarkGreenBlueStyle)
line_chart.title = "Bitcoin value graph"
line_chart.x_labels = dates
line_chart.add("Value in USD", closing_prices_in_usd)
line_chart.add("Value in EUR", closing_prices_in_eur)

if platform.system() == "Linux":
    line_chart.render_to_file("/var/tmp/bitcoin-value-graph")
    webbrowser.open("/var/tmp/bitcoin-value-graph")

if platform.system() == "Darwin":
    line_chart.render_to_file("/var/tmp/bitcoin-value-graph")
    webbrowser.open("/var/tmp/bitcoin-value-graph")


if platform.system() == "Windows":
    user = getpass.getuser()
    line_chart.render_to_file(fr"C\Users\{user}\AppData\Local\Temp\bitcoin-value-graph")
    webbrowser.open(fr"C\Users\{user}\AppData\Local\Temp\bitcoin-value-graph")