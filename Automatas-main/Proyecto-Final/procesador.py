import pandas as pd
import re

def procesador_datos(archivo_csv, fecha_inicio, fecha_fin, rango_abierto):
    # Lee el archivo CSV 
    df = pd.read_csv(archivo_csv, sep=';')
    # Patrones regulares para verificar archivo 
    patron_fecha = r'^(0[1-9]|[1-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/\d{4} ([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
    patron_id_conexion = r'^[a-z0-9]{16}$'
    patron_usuario = r'^[a-zA-Z0-9_-]{3,16}$'
    patron_sesion = r'^\d+.\d+$'
    patron_mac = r'\b([0-9A-F]{2}([-][0-9A-F]{2}){5}:UM)\b'
    patron_cliente = r'\b([0-9A-F]{2}([-][0-9A-F]{2}){5})\b'

    # Convierte las columnas a cadenas antes de aplicar las expresiones regulares
    df['Session Time'] = df['Session Time'].astype(str)
    df['Input Octects'] = df['Input Octects'].astype(str)
    df['Output Octects'] = df['Output Octects'].astype(str)

    # Aplica todos los filtros
    df = df[df['ID Conexion unico'].str.match(patron_id_conexion, na=False) &
            df['Usuario'].str.match(patron_usuario, na=False) &
            df['Inicio de Conexion'].str.match(patron_fecha, na=False) &
            df['Fin de Conexio'].str.match(patron_fecha, na=False) &
            df['Session Time'].str.match(patron_sesion, na=False) &
            df['Input Octects'].str.match(patron_sesion, na=False) &
            df['Output Octects'].str.match(patron_sesion, na=False) &
            df['MAC AP'].str.match(patron_mac, na=False) &
            df['MAC Cliente'].str.match(patron_cliente, na=False)]

    feriados = ['2019-08-31', '2019-10-01', '2019-09-30', '2019-09-29']
    # Convierte las columnas de fecha al formato deseado
    df['Inicio de Conexion'] = pd.to_datetime(df['Inicio de Conexion'], format='%d/%m/%Y %H:%M') 
    df['Fin de Conexio'] = pd.to_datetime(df['Fin de Conexio'], format='%d/%m/%Y %H:%M' )

    # Define el rango de fechas que deseas extraer
    fecha_inicio = pd.Timestamp(fecha_inicio)
    fecha_fin = pd.Timestamp(fecha_fin)
    
    if rango_abierto:
        # Filtra las filas dentro del rango de fechas (inicio y fin de conexión) Rango abierto
        df_fin = df[(df['Fin de Conexio'] >= fecha_inicio) & (df['Fin de Conexio'] <= fecha_fin)]
        df_inicio = df[(df['Inicio de Conexion'] >= fecha_inicio) & (df['Inicio de Conexion'] <= fecha_fin)]

        # Combina los resultados de ambas filtraciones para obtener todas las conexiones rango abierto
        df_resultado = pd.concat([df_fin, df_inicio])
    else:
        # Rango cerrado    
        df_resultado = df[(df['Inicio de Conexion'] >= fecha_inicio) & (df['Fin de Conexio'] <= fecha_fin)]

    # Filtra los días feriados (sábados, domingos y feriados) en el inicio y fin de sesión
    dias_feriados = df_resultado['Inicio de Conexion'].dt.strftime('%Y-%m-%d').isin(feriados)
    df_resultado = df_resultado[(df_resultado['Inicio de Conexion'].dt.dayofweek.isin([5, 6]) | df_resultado['Fin de Conexio'].dt.dayofweek.isin([5, 6])) | dias_feriados]

    # Elimina duplicados en función de las columnas relevantes 
    df_resultado = df_resultado.drop_duplicates(subset='ID Conexion unico')

    # Convierte las columnas de fecha al formato deseado
    df_resultado['Fin de Conexio'] = df_resultado['Fin de Conexio'].dt.strftime('%d/%m/%Y %H:%M')
    df_resultado['Inicio de Conexion'] = df_resultado['Inicio de Conexion'].dt.strftime('%d/%m/%Y %H:%M')

    # Guarda el resultado en un nuevo archivo CSV con el formato de fecha deseado
    df_resultado.to_csv('datos_filtrados.csv', sep=';', index=False)

