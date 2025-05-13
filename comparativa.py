import pandas as pd
import numpy as np

# Cargar archivos
tarifas = pd.read_csv("tarifas.csv")
cruces = pd.read_csv("cruces_actualizado.csv")

# Limpiar encabezados y contenido
tarifas.columns = tarifas.columns.str.strip()
cruces.columns = cruces.columns.str.strip()

# Asegurar consistencia en datos
tarifas["Nombre"] = tarifas["Nombre"].astype(str).str.strip().str.upper()
cruces["Caseta"] = cruces["Caseta"].astype(str).str.strip().str.upper()
cruces["Clase"] = cruces["Clase"].astype(str).str.strip()
cruces["Importe"] = cruces["Importe"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float)

# Crear tipo de camión
cruces["Camion_Tipo"] = "Camion_T" + cruces["Clase"]

# Crear una lista para almacenar los resultados
resultados = []

# Iterar por cada fila de cruces
for _, fila in cruces.iterrows():
    id_actual = fila["Id"]
    caseta = fila["Caseta"]
    clase = fila["Clase"]
    tipo = fila["Camion_Tipo"]
    importe = fila["Importe"]
    
    # Buscar posibles coincidencias en tarifas para esa caseta
    posibles_tarifas = tarifas[tarifas["Nombre"] == caseta]

    coincidencia_encontrada = False
    diferencia_detectada = False

    for _, posible in posibles_tarifas.iterrows():
        if tipo in posible:
            tarifa_esperada = posible[tipo]
            if pd.notnull(tarifa_esperada):
                try:
                    tarifa_esperada = float(str(tarifa_esperada).replace("$", "").replace(",", ""))
                    diferencia = importe - tarifa_esperada
                    if abs(diferencia) < 0.01:
                        # Coincidencia exacta
                        resultados.append({
                            "Id": id_actual,
                            "Caseta": caseta,
                            "Clase": clase,
                            "Camion_Tipo": tipo,
                            "Importe": importe,
                            "Tarifa_Esperada": tarifa_esperada,
                            "Diferencia": diferencia,
                            "Coincide": True
                        })
                        coincidencia_encontrada = True
                        break
                    else:
                        # Coincidencia por nombre y ejes, pero no precio
                        diferencia_detectada = True
                        resultados.append({
                            "Id": id_actual,
                            "Caseta": caseta,
                            "Clase": clase,
                            "Camion_Tipo": tipo,
                            "Importe": importe,
                            "Tarifa_Esperada": tarifa_esperada,
                            "Diferencia": diferencia,
                            "Coincide": False
                        })
                except ValueError:
                    pass

    if not coincidencia_encontrada and not diferencia_detectada:
        # No hubo ninguna coincidencia posible
        resultados.append({
            "Id": id_actual,
            "Caseta": caseta,
            "Clase": clase,
            "Camion_Tipo": tipo,
            "Importe": importe,
            "Tarifa_Esperada": np.nan,
            "Diferencia": np.nan,
            "Coincide": None
        })

# Convertir resultados a DataFrame
df_resultados = pd.DataFrame(resultados)

# Filtrar los distintos tipos
coincidencias_correctas = df_resultados["Coincide"] == True
errores_precio = df_resultados["Coincide"] == False
no_encontrados = df_resultados["Coincide"].isnull()

# Guardar errores y no encontrados
df_resultados[errores_precio][["Id", "Caseta", "Clase", "Camion_Tipo", "Importe", "Tarifa_Esperada", "Diferencia"]].to_csv("reporte_errores.csv", index=False)
df_resultados[no_encontrados][["Id", "Caseta", "Clase", "Camion_Tipo", "Importe"]].to_csv("reporte_no_encontrados.csv", index=False)

# Mostrar resumen
print(f"Total registros procesados: {len(cruces)}")
print(f"Coincidencias correctas: {coincidencias_correctas.sum()}")
print(f"Errores con nombre y ejes coincidentes pero precio diferente: {errores_precio.sum()} (ver 'reporte_errores.csv')")
print(f"Registros sin coincidencia alguna (ni por caseta ni por tipo): {no_encontrados.sum()} (ver 'reporte_no_encontrados.csv')")
