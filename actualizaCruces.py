import pandas as pd

# Ruta del archivo original
archivo_entrada = 'cruces.csv'  # Cambia esto por el nombre de tu archivo
archivo_salida = 'cruces_actualizado.csv'

# Leer el archivo CSV
df = pd.read_csv(archivo_entrada)

# Eliminar la columna 'Tag'
if 'Tag' in df.columns:
    df = df.drop(columns=['Tag'])

# Insertar columna 'Id' al inicio con valores consecutivos desde 1
df.insert(0, 'Id', range(1, len(df) + 1))

# Guardar el archivo modificado
df.to_csv(archivo_salida, index=False)

print(f"Archivo procesado correctamente. Guardado como '{archivo_salida}'")
