
import requests,json;

#DESCODIFICADOR VIN NHTSA -----------------------------------------------
def vinDecodeValues(vin):
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
    post_fields = {'format': 'json', 'data':vin}
    r = requests.post(url, data=post_fields).text
    r_dict = json.loads(r)

    for concepto in r_dict['Results']:
            for clave,valor in concepto.items():
                if len(valor) > 0:
                    print(clave.upper() + " --> " + valor)
                else:
                    pass

#vinDecodeValues('SCBFR7ZA5CC072256')
vin_seat_leon = 'VSSZZZ5FZJR117085'
vin = 'SCBFR7ZA5CC072256'
url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/SCBFR7ZA5CC072256?format=json&modelyear=2011'
post_fields = {'format': 'json', 'data':vin}
r = requests.get(url).text
r_dict = json.loads(r)

for concepto in r_dict['Results']:
    for clave,valor in concepto.items():
        if type(valor) == int and valor > 0 or type(valor) == str and len(valor) > 0:
            print (clave,valor)