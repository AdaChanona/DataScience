from tkinter.constants import INSERT
import pandas as pd
import numpy as np
import math
import statistics as st
from pandas.core import frame
from scipy import stats
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Button, Text, filedialog, ttk

#tkinter
raiz=tk.Tk()
raiz.title('Star wars - Estadistica')
raiz.geometry('2000x1300')
raiz.pack_propagate(False)
raiz.config(bg='white',width=1300,height=700)


#leer csv y ordenar
def repararArreglo(continuas):
    if continuas=='0':
        continuas='00:00'
    if len(continuas)<5:
        continuas='0'+continuas
    return continuas
    
def convertirTiempo(time):
    horas = float(time[0:2])
    minutos = float(time[3:5]) /60
    time = horas+minutos
    return round(time,2)

path=filedialog.askopenfilename()
dataframe=pd.read_csv(path)
discretas=np.array(dataframe['¿Cuantas peliculas has visto?'].sort_values())
continuas=np.array(dataframe['¿Cuantas horas inviertes en ver?'].sort_values())
cualitativos=np.array(dataframe['¿Cual es tu favorita?'].sort_values())
horas=[]
for i in continuas:
    i=repararArreglo(i)
    i=convertirTiempo(i)
    horas.append(i)
continuas=np.sort(np.array(horas))

#medidas de tendencia central
def mediaAritmetica(variable):
    m_a=variable.mean()
    return round(m_a,2)

def mediaGeometrica(variable):
    m_g=stats.gmean(variable)
    return round(m_g,2)

def mediaTruncada(variable):
   m_t = stats.trim_mean(variable, .10)
   return round(m_t,2)

def mediana(variable):
    mediana=st.median(variable)
    return round(mediana,2)

def moda(variable):
    moda=st.mode(variable)
    return moda

def sesgo(media,mediana,moda):
    sesgo=''
    if(media<mediana and mediana<moda):
        sesgo='izquierda'
    elif(moda<mediana or mediana<media):
        sesgo='derecha'
    else:
        sesgo='simetrico'
    
    return sesgo

def varianza(variable):
    varianza=variable.var()
    return round(varianza,2)

def desvEstandar(varianza):
    desvEstandar=0
    desvEstandar=math.sqrt(varianza)
    return round(desvEstandar,2)

#distribucion de frecuencia
def rango (variable):
    maximo=variable[len(variable)-1]
    minimo=variable[0]
    rango=int(maximo-minimo)
    return rango

def numeroClases(variable):
    numClases=int(1+3.3*math.log10(len(variable)))
    return round(numClases,2)

def Clases(rang, numClases,variable):
    anchoClase=int(rang/numClases)
    clases={}
    limInferior=variable[0]
    frecAbs=0
    frecRel=0
    for i in range(numClases):
        limSuperior=limInferior+anchoClase
        marcaClase=round((limInferior+limSuperior)/2,2)
        for y in range(len(variable)):
            val = variable[y]
            if  val >= limInferior and val <= limSuperior:
                frecAbs = frecAbs + 1
        frecRel = (frecAbs*100)/len(variable)
        clases[f'Clase {i+1}']={'Limite Inferior':limInferior,'limite superior':limSuperior,'Marca de clase':marcaClase, 
                                'Absoluta':frecAbs,'Relativa':frecRel}
        limInferior=limSuperior
        frecAbs=0
        frecRel=0
    clases=pd.DataFrame(clases).transpose()
    return clases

#DATOS AGRUPADOS
def mediaAgrupada(variable,numero_clases,dataframe_clases):
    marca_clase=np.array(dataframe_clases['Marca de clase'])
    frecuencia=np.array(dataframe_clases['Absoluta'])
    suma=0
    mult=0
    for i in range(numero_clases):
        mult=marca_clase[i]*frecuencia[i]
        suma=suma+mult
    media_agrupada=suma/len(variable)
    return round(media_agrupada,2)

def modaAgrupada(dataframe_clases):
    marca_clase=np.array(dataframe_clases['Marca de clase'])
    frecuencia=np.array(dataframe_clases['Absoluta'])
    frecMax= max(frecuencia, key=int)
    posicion=-1
    for i in range(len(frecuencia)):
        if(frecuencia[i]==frecMax):
            posicion=posicion+1
    modaAgrupada=marca_clase[posicion]
    return modaAgrupada

def medianaAgrupada(dataframe_clases):
    marca_clase=np.array(dataframe_clases['Marca de clase'])
    posicion=int(len(dataframe_clases)/2)
    mediana=marca_clase[posicion-1]+marca_clase[posicion]
    mediana=mediana/2
    return round(mediana,2)

def varianzaAgrupada(variable,media,numero_clases,dataframe_clases):
    marca_clase=np.array(dataframe_clases['Marca de clase'])
    frecuencia=np.array(dataframe_clases['Absoluta'])
    multiplicacion=[]
    for i in range(numero_clases):
        mult=pow(marca_clase[i],2)*frecuencia[i]
        multiplicacion.append(mult)
    suma=np.sum(multiplicacion)
    media=pow(media,2)
    varianza_agrupada=(suma-(len(variable)*media))/(len(variable)-1)
    return round(varianza_agrupada,2)

# dataframe cualitativos
def cualitativos_df(variable):
    a_f=0 
    g_c=0
    v_s=0
    n_e=0
    i_c=0
    r_j=0
    d_f=0
    u_j=0
    a_s=0
    nin=0
    for i in range(len(variable)):
        if variable[i]=='Star Wars: Episodio I - La amenaza fantasma':
            a_f=a_f+1
        if variable[i]=='Star Wars: Episodio II - La guerra de los clones':
            g_c=g_c+1
        if variable[i]=='Star Wars: Episodio III - La venganza de los Sith':
            v_s=v_s+1
        if variable[i]=='Star Wars: Episodio IV - Una nueva esperanza':
            n_e=n_e+1
        if variable[i]=='Star Wars: Episodio V - El Imperio contraataca':
            i_c=i_c+1
        if variable[i]=='Star Wars: Episode VI - El retorno del Jedi':
            r_j=r_j+1
        if variable[i]=='Star Wars: Episodio VII - El despertar de la Fuerza':
            d_f=d_f+1
        if variable[i]=='Star Wars: Episodio VIII - Los últimos Jedi':
            u_j=u_j+1
        if variable[i]=='Star Wars: Episodio IX - El ascenso de Skywalker':
            a_s=a_s+1
        if variable[i]=='Ninguna':
            nin=nin+1
    nombre_peliculas=['La amenaza fantasma','La guerra de los clones','La venganza de los Sith',
    'Una nueva esperanza','El Imperio contraataca','El retorno del Jedi','El despertar de la Fuerza',
    'Los últimos Jedi','El ascenso de Skywalker','Ninguna']
    frecAbsoluta_Cualitativa=[a_f,g_c,v_s,n_e,i_c,r_j,d_f,u_j,a_s,nin]
    frecRelativa_Cualitativa=[]
    for i in range(len(frecAbsoluta_Cualitativa)):
        porcentaje=(frecAbsoluta_Cualitativa[i]*100)/len(variable)
        frecRelativa_Cualitativa.append(porcentaje)
    
    nombre_peliculas=pd.DataFrame(np.array(nombre_peliculas),columns=['Peliculas'])
    frecAbsoluta_Cualitativa=pd.DataFrame(np.array(frecAbsoluta_Cualitativa),columns=['frecAbsoluta'])
    frecRelativa_Cualitativa=pd.DataFrame(np.array(frecRelativa_Cualitativa),columns=['frecRelativa'])
    dataframeCualitativa=pd.concat([nombre_peliculas,frecAbsoluta_Cualitativa,frecRelativa_Cualitativa],axis=1)
    return dataframeCualitativa
    
#datos cualitativos
dfCualitativos=cualitativos_df(cualitativos)
print(dfCualitativos)
#datos continuos
rangoContinuas=rango(continuas)
numClases_continuas=numeroClases(continuas)
dataframeContinuas= Clases(rangoContinuas,numClases_continuas,continuas)
mediaAgrup= mediaAgrupada(continuas,numClases_continuas,dataframeContinuas)
medianaAgrup=medianaAgrupada(dataframeContinuas)
modaAgrup=modaAgrupada(dataframeContinuas)
varAgrupada=varianzaAgrupada(continuas,mediaAgrup,numClases_continuas,dataframeContinuas)
desEstandar=desvEstandar(varAgrupada)
sesgo_Continuas=sesgo(mediaAgrup,medianaAgrup,modaAgrup)
print(dataframeContinuas)
mtc_agrup=[mediaAgrup,np.NAN,np.NAN,medianaAgrup,modaAgrup,varAgrupada,desEstandar,
        sesgo_Continuas]

#discretas
media_discreta_A=mediaAritmetica(discretas)
media_discreta_G=mediaGeometrica(discretas)
media_discreta_T=mediaTruncada(discretas)
mediana_discreta=mediana(discretas)
moda_discreta=moda(discretas)
varianza_discreta=varianza(discretas)
desEstandar_discreta=desvEstandar(varianza_discreta)
sesgo_discretas=sesgo(media_discreta_A,mediana_discreta,moda_discreta)
mtc_discretas=[media_discreta_A,media_discreta_G,media_discreta_T,mediana_discreta,
                moda_discreta,varianza_discreta,desEstandar_discreta,sesgo_discretas]
rango_discretas=rango(discretas)
numClases_discretas=numeroClases(discretas)
dataframeDiscretas= Clases(rango_discretas,numClases_discretas,discretas)
frecAbsoluta_Discreta=pd.DataFrame(np.array(dataframeDiscretas['Absoluta']),columns=['Absoluta'])
frecRelativa_Discreta=pd.DataFrame(np.array(dataframeDiscretas['Relativa']),columns=['Relativa'])
marca_discretas=pd.DataFrame(np.array(dataframeDiscretas['Marca de clase']),columns=['Peliculas'])
dataframeDiscretas=pd.concat([marca_discretas,frecAbsoluta_Discreta,frecRelativa_Discreta],axis=1)
print(dataframeDiscretas)

#MTC agrupadas/no agrupadas
mtc_array=[mtc_agrup,mtc_discretas]
mtc_dataframe=pd.DataFrame(mtc_array,columns=['MediaAritmetica','MediaGeometrica','mediaTruncada',
                                                'mediana','moda','varianza','desvEstandar','sesgo']).rename(
                                                    index={0:'Continuas',1:'Discretas'}
                                                )
print(mtc_dataframe)

#diagramas

def graficaPoligono(dataframe):
    grafPoli=plt.plot(dataframe['Marca de clase'],dataframe['Absoluta'])
    plt.show()

def graficaBarras(dataframe):
    grafBarra=plt.bar(dataframe['Peliculas'],dataframe['Absoluta'])
    plt.show()

def pastel(dataframe):
    plt.pie(dataframe['frecRelativa'],
        labels=dataframe['Peliculas'],
        autopct='%1.1f%%')
    plt.show()


#tkinter

label1=tk.Label(raiz,text='PERSONAS QUE HAYAN VISTO STAR WARS',font=(200))
label1.place(x=600,y=40)
label2=tk.Label(raiz,text='Variable Continua',font=(60))
label2.place(x=300,y=80)
label3=tk.Label(raiz,text='Variable Discreta',font=(60))
label3.place(x=750,y=80)
label4=tk.Label(raiz,text='Variable Cualitativa',font=(60))
label4.place(x=1200,y=80)
label5=tk.Label(raiz,text='Medidas de tendencia central y dispersion',font=(60))
label5.place(x=300,y=450)

tk.Button(raiz, text="Grafica de poligono", command=lambda:graficaPoligono(dataframeContinuas)).place(x=300,y=350)
tk.Button(raiz, text="Grafica de barras", command=lambda:graficaBarras(dataframeDiscretas)).place(x=750,y=350)
tk.Button(raiz, text="Grafica de pastel", command=lambda:pastel(dfCualitativos)).place(x=1200,y=350)
table1 = Text(raiz)
table1.insert(INSERT,dataframeContinuas.to_string())
table1.pack()
table1.place(x=5, y=130,height=225, width=670)
table2 = Text(raiz)
table2.insert(INSERT,dataframeDiscretas.to_string())
table2.pack()
table2.place(x=650, y=130, height=200)
table3 = Text(raiz)
table3.insert(INSERT,dfCualitativos.to_string())
table3.pack()
table3.place(x=1020, y=130, height=200,)
table4 = Text(raiz)
table4.insert(INSERT,mtc_dataframe.to_string())
table4.pack()
table4.place(x=300, y=500, height=50,width=1000)
raiz.mainloop()




