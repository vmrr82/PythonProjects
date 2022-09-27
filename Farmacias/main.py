from base64 import encode
import datetime
import requests
from bs4 import BeautifulSoup


today = datetime.date.today()

r = requests.get(f"https://www.cofib.es/ca/llistat_guardies.aspx?z=Calvià&data={today}").content
soup = BeautifulSoup(r,'lxml')

tablaFarmacia = soup.find(id='tblLlistatGuardies')
rows = tablaFarmacia.find_all('tr')

listaFarmacias = []
for row in rows:
    listaFarmacias.append(row.get_text().replace('\xa2',''))

print('Generando archivo, espere por favor...')   
with open(f'COFIB{today}.txt','w') as archivo:
    archivo.writelines("LISTADO DE FARMACIAS DE GUARDIA DE COFIB\n\n")
    archivo.writelines(str(soup.find(id="ctl00_cphBody_titGuardies").string + "\n"))
    archivo.writelines("----------------------------------------------\n")
    archivo.writelines("%s\n" % i for i in listaFarmacias)



