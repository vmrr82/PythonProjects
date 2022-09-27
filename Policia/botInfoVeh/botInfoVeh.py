import requests
from bs4 import BeautifulSoup
import json

#Telegram bot of car plate info research

class infoVeh:

    def __init__(self,bastidor):
        
        self.bastidor = bastidor

    def rumania(self):
    
        cookies = dict(cookies_are='working')
        r = requests.get(f'https://www.politiaromana.ro/ro/auto-furate?marca=&serie={self.bastidor}&categorie=',cookies=cookies,timeout=3)
        soup = BeautifulSoup(r.text,'html.parser')
        while True:
            try:
                matricula = soup.find("div",{"class":"listBoxLeft3"}).b.text
                marca = soup.find("a",{"class":"listBoxItem"}).text
                print("-----RUMANIA------VEHÍCULO ENCONTRADO-----")
                print("\nBASTIDOR: " + self.bastidor + "\nMARCA: " + marca + "\nMATRICULA: " + matricula)
                
            except (AttributeError,TypeError):
                print("-----RUMANIA------VEHÍCULO NO ENCONTRADO-----")
                break

    def hungria(self):
        cookies = dict(cookies_are='working')
        r = requests.get(f'http://www.police.hu/hu/koral/kozutijarmu-korozesek?ent_jarmu_kozuti_alvazszam={self.bastidor}&ent_jarmu_kozuti_rendszam=&ent_jarmu_kozuti_kore_szerv=All&ent_jarmu_kozuti_kori_szerv=All&ent_jarmu_kozuti_fajta=All&ent_jarmu_kozuti_gyartmany=All&ent_jarmu_kozuti_forgalomba_helyezo_orszag=All&ent_jarmu_kozuti_szin=All',cookies=cookies,timeout=3)
        soup = BeautifulSoup(r.text,'html.parser')
        
        while True:
            try:
                localizado = soup.find("div",{"class":"flex-grid table"}).text.split()
                matricula = localizado[2]
                bastidor = localizado[4]
                tipo_vehiculo = localizado[7]
                marca = localizado[9]
                color = localizado[-1]
                url = 'https://www.police.hu/hu/koral/kozutijarmu-korozesek'
                print("-----HUNGRIA------VEHÍCULO ENCONTRADO-----")
                print("\nBASTIDOR: " + self.bastidor + "\nMARCA: " + marca + "\nMATRICULA: " + matricula + "\nCOLOR: " + color + "\nURL: " + url)
                break
            except(AttributeError,TypeError):
                print("-----HUNGRIA------VEHÍCULO NO ENCONTRADO-----")
                break

    def eslovenia(self):
        
        with open('Policia/botInfoVeh/ukrvoz.json','r') as file:
                data = json.load(file).values()
                for lista in data:
                    for item in lista:
                        marca = item['znamka']
                        modelo = item['tip']
                        bastidorCoche = item['sasija']
                        color = item['barva']
                        fecha = item['datumodvzema']
                        
                        if (self.bastidor in bastidorCoche):
                                try:
                                        print('-----ESLOVENIA------VEHÍCULO ENCONTRADO-----')
                                        print("\nBASTIDOR: " + self.bastidor + "\nMARCA: " + marca + "\nCOLOR: " + color + "\nFECHA: " + fecha)
                                        
                                        
                                except KeyError as e:
                                        print("-----ESLOVENIA------VEHÍCULO NO ENCONTRADO-----",e)
                                        break
 
                
        



#BASTIDORES DE PRUEBA        
#RUMANIA ---'WADKJNCKJDSNC'
#HUNGRIA ---'VF42A262DP28622'
#ESLOVENIA --- 'ZZ1A8GBAP00842109'      
#BELGICAMATRI --- '0AAG527'
    
buscar = infoVeh('VF42A262DP28622')
#buscar.rumania()
buscar.hungria()
#buscar.eslovenia()
