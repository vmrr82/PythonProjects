from ast import arg
import pandas as pd

class codificadoInfracciones(arg):

   
    df = pd.read_csv('LectorPDF\BUENO.csv',delimiter=',',encoding='utf-8').fillna(value=0)
    infraccion = df[df.INFRACCION.str.contains(str(arg),case=False,na=False)].to_dict()
    campoCIR = infraccion.get('CIR')
    for k,v in campoCIR.items():
        print(v) 
   
        

               

codificadoInfracciones('alcohol')


"""campoLSV = infraccion.get('LSV')
        campoART = infraccion.get('ART')
        campoAPT = infraccion.get('APT')
        campoOPC = infraccion.get('OPC')
        campoPTOS = infraccion.get('PTOS')
        campoCALIF = infraccion.get('CALIF')
        campoINFRACCION = infraccion.get('INFRACCION')"""
       


