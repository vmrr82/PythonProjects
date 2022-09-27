import requests
from bs4 import BeautifulSoup

def conocerPais():
    matricula = input('Introduce la matrícula (NO ESPAÑOLA), por favor: ')
    cookies = dict(cookies_are='working')
    r = requests.get(f'https://www.ofesauto.es/tramites/conocer-la-nacionalidad-de-un-vehiculo-por-su-matricula/?matricula={matricula}',cookies=cookies,timeout=3)
    soup = BeautifulSoup(r.text,'html.parser')
    tabla = soup.find('tbody',class_='resultados-table')
    resultados = len(soup.findAll('div',class_='cell-zona'))
    contador = 0
    while contador < resultados:
        zona = tabla.findAll('div',class_='cell-zona')
        probabilidad = tabla.findAll('div',class_='progress')
        for x, i in enumerate(zona):
            prob = probabilidad[x].text
            print(f'Probabilidad: {prob}  Pais:{i.text}'.split())
            contador+=1
conocerPais()