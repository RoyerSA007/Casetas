import pandas as pd

# Leer el archivo generado previamente
datos = pd.read_csv('resultado_filtrado.csv')

# Asegurar que todos los campos clave estén limpios
for campo in ['Caseta', 'Carril']:
    datos[campo] = datos[campo].astype(str).str.strip()

# Agrupar por Tag, No.Economico, Caseta y Carril y contar repeticiones
grupo = datos.groupby(['Caseta', 'Carril']).size().reset_index(name='Repeticiones')

# Filtrar los que se repiten más de una vez
duplicados = grupo[grupo['Repeticiones'] > 1]

# Hacer merge con los datos originales para obtener los registros completos
resultado_duplicados = datos.merge(
    duplicados[['Caseta', 'Carril']],
    on=['Caseta', 'Carril']
)

# Guardar el resultado en un nuevo archivo
resultado_duplicados.to_csv('registros_repetidos.csv', index=False)

print("✅ Archivo 'registros_repetidos.csv' creado con los registros duplicados según Caseta y Carril.")
