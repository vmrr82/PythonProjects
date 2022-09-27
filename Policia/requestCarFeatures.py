import requests
from bs4 import BeautifulSoup
from time import sleep

url = '/home/vmr/Escritorio/Programacion/GitHub/car-specs.html'
with open(url) as pagina:
    web_parse = BeautifulSoup(pagina,'html.parser')
divSection = web_parse.find_all('div', attrs={"class" :"makelinks col-sm-6 col-md-3"})

for marca in divSection:
    print(f'- {marca.string}')