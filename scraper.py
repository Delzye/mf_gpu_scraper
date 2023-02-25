import requests
import re
from bs4 import BeautifulSoup
from pyexcel_ods import save_data
from collections import OrderedDict

URL = "https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/Radeon+RX+Serie.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
result_container = soup.find(id="bProducts")
result_list = result_container.find_all("div", class_="pcontent")

sheets = OrderedDict()
frame_data_sheet = OrderedDict()
frame_data_sheet["RX 6700 XT"] = 120
frame_data_sheet["RX 6800 XT"] = 180

price_data_sheet = list()
for result in result_list:
    name_div = result.find("div", class_="pname")
    model = re.search("RX( )?[0-9]+( )?(XT)?", name_div.text)
    gpu_model_str = model.group()

    price_div = result.find("div", class_="pprice")
    price_str = re.search("([0-9]*\.)?[0-9]*,[0-9]*", price_div.text).group()
    price_data_sheet.append([name_div.text, gpu_model_str, price_str])
sheets.update({"Angebote und Preise": price_data_sheet})
sheets.update({"Frame Data": frame_data_sheet.items()})
save_data("test_code.ods", sheets)