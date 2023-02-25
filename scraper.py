import requests
import re
from bs4 import BeautifulSoup
from pyexcel_ods import save_data, get_data
from collections import OrderedDict

URL = "https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/Radeon+RX+Serie.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
result_container = soup.find(id="bProducts")
result_list = result_container.find_all("div", class_="pcontent")

frame_data_sheet = get_data("frame_data.ods")
frame_data = frame_data_sheet.values()
frame_dict = {item[0]: item[1] for item in list(frame_data)[0]}

sheets = OrderedDict()
price_data_sheet = list()
price_data_sheet.append(["Name", "Modell", "Preis", "Preis/Frame"])

for result in result_list:
    # Modell herausfinden
    name_div = result.find("div", class_="pname")
    model = re.search("RX( )?[0-9]+( )?(XTX?)?", name_div.text)
    gpu_model_str = model.group().strip()
    # Kein Leerzeichen Nach "RX"
    if gpu_model_str[2] != " ":
        gpu_model_str = gpu_model_str[:2] + " " + gpu_model_str[2:]
    # Kein Leerzeichen vor XT
    if gpu_model_str[-2:] == "XT" and gpu_model_str[-3] != " ":
        gpu_model_str = gpu_model_str[:-2] + " " + gpu_model_str[-2:]

    if gpu_model_str[-3:] == "XTX" and gpu_model_str[-4] != " ":
        gpu_model_str = gpu_model_str[:-3] + " " + gpu_model_str[-3:]
    # Preis herausfinden
    price_div = result.find("div", class_="pprice")
    price_str = re.search("([0-9]*\.)?[0-9]*,[0-9]*", price_div.text).group()
    # Wenn der Preis ganzzahlig ist
    if price_str[-1:] == ",":
        price_str = price_str + "00"
    # Tausender-Punkt ersetzen und Cent-Trennung mit Punkt machen
    price_float = float(price_str.replace('.','').replace(',', '.'))
    try:
        euro_per_frame = price_float / frame_dict[gpu_model_str]
    except KeyError:
        euro_per_frame = '-'
    # Zeile hinzufügen
    price_data_sheet.append([name_div.text, gpu_model_str, price_float, euro_per_frame])
sheets.update({"Angebote und Preise": price_data_sheet})
sheets.update({"Frame Data": list(frame_data)[0]})
save_data("test_code.ods", sheets)