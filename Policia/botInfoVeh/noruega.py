from unittest import result
import requests
from bs4 import BeautifulSoup

matriculaNoruega = 'rk60920'
def noruega():
    matricula = input('Introduce la matrícula, por favor: ')
    cookies = dict(cookies_are='working')
    r = requests.get(f'https://www.vegvesen.no/kjoretoy/kjop-og-salg/kjoretoyopplysninger/sjekk-kjoretoyopplysninger/?registreringsnummer={matricula}',cookies=cookies,timeout=3)
    soup = BeautifulSoup(r.text,'html.parser')
    dtTag = soup.findAll('dt')
    ddTag = soup.findAll('dd')
    titulos = []
    resultados = []
    for x,i in enumerate(dtTag):
        resultados.append(ddTag[x].text)    
        titulos.append(i.text)
    #print(f"Matrícula: {resultados[3]}\nEstado: {resultados[2]} \nMarca: {resultados[5]} \nVIN: {resultados[4]} \n1ª Matriculación: {resultados[8]} \nÚltima comprobación: {resultados[0]}\nPróxima comprobación: {resultados[1]}\nColor: {resultados[12]}")
    print(soup)
noruega()