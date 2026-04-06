# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

"""
=====================================================================
IMPORTACIONES
=====================================================================
"""

import os
import pandas as pd
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


"""
=====================================================================
SUBPROGRAMAS UTILIZADOS
=====================================================================
"""

def leer_archivo_df(nombre):
    """
    Lee archivos de sismos y retorna un Dataframe construido por los datos procesados.
    
    Parámetros:
    nombre (str): nombre del archivo dentro de la carpeta de "Archivos"
    
    Retorna:
    Dataframe: contiene latitud, longitud, magnitud, profundidad, fecha(año, mes día),
    hora y momento sismico
    """
    ruta = os.path.join("Archivos", nombre)

    # listas para almacenar datos
    lat, lon, year, month, day, mag, prof, hora, minuto, momento = [], [], [], [], [], [], [], [], [], []

    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")

            print(len(partes))
            
            # validar cantidad de columnas
            if len(partes) < 9:
                continue
            
            try:
                lat_val = float(partes[0])
                lon_val = float(partes[1])
                year_val = float(partes[2])
                month_val = float(partes[3])
                day_val = float(partes[4])
                mag_val = float(partes[5])
                prof_val = float(partes[6])
                hora_val = int(partes[7])
                minutos_val = int(partes[8])
                
                # calcular momento sismico
                mommento_val = calcularMomentoSismico(mag_val)
                 
                # guardar datos
                lat.append(lat_val)
                lon.append(lon_val)
                year.append(year_val)
                month.append(month_val)
                day.append(day_val)
                mag.append(mag_val)
                prof.append(prof_val)
                hora.append(hora_val)
                minuto.append(minutos_val)
                momento.append(mommento_val)
                

            except:
                continue
    
    # crear Dataframe
    df = pd.DataFrame({
        "lat": lat,
        "lon": lon,
        "prof": prof,
        "mag": mag,
        "momento": momento,
        "year": year,
        "month": month,
        "day": day,
        "hora": hora,
        "minuto": minuto
        
    })

    return df

def calcularMomentoSismico(mag_val):
    """
    Calcula el momento sismico dependiendo del valor de la magnitud.
    
    Parámetros:
    mag_val(float): el valor de la magnitud obtenido mediante los archivos
    
    Retorna:
    momento sismico(float)
    """
    # se obtiene el logaritmo del evento
    log_event = 1.5*(mag_val + 10.73)
    
    # y luego a 10 se eleva en el logaritmo del evento obtenido anteriormente
    momento_sismico = 10**(log_event)
    
    return momento_sismico

def graficarIntensidad(df):
    """
    Crea un grafico de lineas de intensidad a parir de la magnitud
    
    Parámetros:
    df (dataframe): el dataframe formado tras el proceso de archivos
    """
    df = df.sort_values(by="mag")#ordena los valores por magnitud
    
    plt.figure()
    plt.plot(df["mag"], df["momento"])
    
    plt.xlabel("Magnitud")
    plt.ylabel("Intensidad (escala log)")
    plt.title("Intensidad de Sismo vs Magnitud")
    
    plt.yscale("log")  # 🔥 clave
    plt.grid()
    
    plt.savefig("intensidad_sismos.jpg")
    plt.show()
    
def graficarPastel(df):
    """
    Crea un grafico pastel de porcentajes
    
    Parámetros:
    df (dataframe): el dataframe formado tras el proceso de archivos
    """
    # filtra años
    df_filtrado = df[df["year"].isin([2014, 2015, 2016, 2017])]
    
    # contar eventos por año
    conteo = df_filtrado["year"].value_counts().sort_index()
    
    # gráfico de pastel
    plt.figure()
    plt.pie(conteo, labels=conteo.index, autopct="%1.1f%%")
    
    plt.title("Porcentaje de sismos por año (2014-2017)")
    plt.savefig("grafico_pastel.jpg")
    plt.show()
    
def grafico_3d_sismos(df):
    """
    Crea un grafico de dispersion 3D agrupados por año
    
    Parámetros:
    df (dataframe): el dataframe formado tras el proceso de archivos
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # agrupar por año
    for year in df["year"].unique():
        df_year = df[df["year"] == year]

        ax.scatter(
            df_year["lon"],
            df_year["lat"],
            df_year["year"],
            label=str(year)
        )

    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_zlabel("Año")

    plt.title("Dispersión 3D de sismos agrupados por año")
    plt.savefig("grafico_dispersion3D.jpg")
    plt.legend()

    plt.show()
    
"""
=====================================================================
BLOQUE PRINCIPAL
=====================================================================
"""
df_total = pd.DataFrame()  # DataFrame vacío
    
#ITEM 1
while True:
    nombre = input("Ingrese el nombre del archivo (o CIERRE): ")

    #ITEM 2
    if nombre.upper() == "CIERRE":
        print("Programa finalizado.")
        break

    try:
        df = leer_archivo_df(nombre)

        df_total = pd.concat([df_total, df], ignore_index=True)

        # Mostrar magnitud y año
        print(df[["mag", "year"]])

    except FileNotFoundError:
        print("❌ El archivo no existe en la carpeta Archivos.")
        
 
"""
=====================================================================
RESULTADOS
=====================================================================
"""       
#ITEM 3 
print("Total de eventos:", len(df_total))
#ITEM 4
momento_total = df_total["momento"].sum()
#ITEM 5
print("Momento sísmico total:", momento_total)
#ITEM 6
graficarIntensidad(df_total)
#ITEM 7
graficarPastel(df_total)
#ITEM 8
grafico_3d_sismos(df_total)

