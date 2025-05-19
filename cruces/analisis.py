# TR223     IMDM27383500
# IMDM30057656..     263
# TR245 - Tlajomulco de Zu - Leon, Guanajuato
# TR255 - Tlalnepantla, Edo. de M -Coatzacoalcos, Veracruz

import pandas as pd

# Cargar los 3 archivos CSV
archivo1 = pd.read_csv('cruces (1).csv')
archivo2 = pd.read_csv('cruces (2).csv')
archivo3 = pd.read_csv('cruces (3).csv')

# Combinar archivos
datos_combinados = pd.concat([archivo1, archivo2, archivo3], ignore_index=True)

# Limpiar espacios y asegurarse que todo sea string
datos_combinados['Tag'] = datos_combinados['Tag'].astype(str).str.strip()
datos_combinados['No.Economico'] = datos_combinados['No.Economico'].astype(str).str.strip()

# Ingresar datos de búsqueda
print("Ingresa los pares de Tag y No.Economico que deseas buscar. Escribe 'fin' para terminar.")
busquedas = []

while True:
    tag = input("Tag: ").strip()
    if tag.lower() == 'fin':
        break
    no_eco = input("No.Economico: ").strip()
    if no_eco.lower() == 'fin':
        break
    busquedas.append((tag, no_eco))

# Filtrar coincidencias
filtrados = pd.DataFrame()

for tag, no_eco in busquedas:
    coincidencias = datos_combinados[
        (datos_combinados['Tag'] == tag) & (datos_combinados['No.Economico'] == no_eco)
    ]
    filtrados = pd.concat([filtrados, coincidencias], ignore_index=True)

# Verifica si hay resultados antes de guardar
if not filtrados.empty:
    filtrados.to_csv('resultado_filtrado.csv', index=False)
    print("✅ Archivo 'resultado_filtrado.csv' creado con los registros seleccionados.")
else:
    print("⚠ No se encontraron coincidencias con los datos ingresados.")
