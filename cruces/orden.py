import pandas as pd

# Leer el archivo de registros repetidos
datos = pd.read_csv('registros_repetidos.csv')

# Asegurarse de que 'Caseta' no tenga espacios extra y sea texto
datos['Caseta'] = datos['Caseta'].astype(str).str.strip()

# Ordenar por la columna 'Caseta' (alfabéticamente)
datos_ordenados = datos.sort_values(by='Caseta')

# Guardar el resultado ordenado
datos_ordenados.to_csv('registros_repetidos_ordenados_por_caseta.csv', index=False)

print("✅ Archivo 'registros_repetidos_ordenados_por_caseta.csv' creado correctamente y ordenado por la columna 'Caseta'.")
