import tkinter as tk
from tkinter import filedialog
from procesador import procesador_datos
import re
import pandas as pd 

# Expresión regular para validar la fecha
fecha_regex = r"\d{4}/\d{2}/\d{2} \d{1,2}:\d{2}"

# Declara rango_abierto_var como una variable global
rango_abierto_var = None

def procesar():
    global rango_abierto_var  #Inicializa variable global

    archivo_csv = entry_csv.get()
    fecha_inicio = entry_fecha_inicio.get()
    fecha_fin = entry_fecha_fin.get()
    rango_abierto = rango_abierto_var.get()

    if not re.match(fecha_regex, fecha_inicio) or not re.match(fecha_regex, fecha_fin):
        resultado_label.config(text="Error: Formato de fecha inválido")
    else:
        fecha_inicio = fecha_inicio.replace("/", "-")
        fecha_fin = fecha_fin.replace("/", "-")

        try:
            procesador_datos(archivo_csv, fecha_inicio, fecha_fin, rango_abierto)
            resultado_label.config(text="Procesamiento completado")
        except Exception as e:
            resultado_label.config(text=f"Error: {str(e)}")

def cargar_datos():
    archivo_csv = "datos_filtrados.csv"  
    try:
        df = pd.read_csv(archivo_csv)
        datos_text.config(state="normal")
        datos_text.delete(1.0, tk.END)
        datos_text.insert(tk.END, df.to_string(index=False))
        datos_text.config(state="disabled")
        resultado_label.config(text="Datos cargados correctamente")
    except Exception as e:
        resultado_label.config(text=f"Error al cargar los datos: {str(e)}")

def seleccionar_archivo():
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    entry_csv.delete(0, tk.END)
    entry_csv.insert(0, archivo_csv)

ventana = tk.Tk()
ventana.title("Procesador de Datos")

csv_label = tk.Label(ventana, text="Archivo CSV:")
csv_label.pack()
entry_csv = tk.Entry(ventana)
entry_csv.pack()
seleccionar_button = tk.Button(ventana, text="Seleccionar archivo", bg="blue", fg="white", command=seleccionar_archivo)
seleccionar_button.pack()

fecha_inicio_label = tk.Label(ventana, text="Fecha de inicio (aaaa/mm/dd hh:mm):")
fecha_inicio_label.pack()
entry_fecha_inicio = tk.Entry(ventana)
entry_fecha_inicio.pack()

fecha_fin_label = tk.Label(ventana, text="Fecha de fin (aaaa/mm/dd hh:mm):")
fecha_fin_label.pack()
entry_fecha_fin = tk.Entry(ventana)
entry_fecha_fin.pack()

# Manejo de rangos (cerrado predeterminado)
rango_abierto_var = tk.BooleanVar(value=False)
rango_abierto_checkbutton = tk.Checkbutton(ventana, text="Rango Abierto", variable=rango_abierto_var)
rango_abierto_checkbutton.pack()

procesar_button = tk.Button(ventana, text="Procesar", bg="green", fg="white", command=procesar)
procesar_button.pack()

datos_text = tk.Text(ventana, height=40, width=140, state="disabled")
datos_text.pack()

# Barras de desplazamiento vertical y horizontal
scrollbar_y = tk.Scrollbar(ventana, command=datos_text.yview)
scrollbar_y.pack(side="right", fill="y")
scrollbar_x = tk.Scrollbar(ventana, command=datos_text.xview, orient="horizontal")
scrollbar_x.pack(side="bottom", fill="x")

datos_text.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

cargar_datos_button = tk.Button(ventana, text="Cargar Datos", bg="red", fg="white",command=cargar_datos)
cargar_datos_button.pack()

resultado_label = tk.Label(ventana, text="")
resultado_label.pack()

ventana.mainloop()
