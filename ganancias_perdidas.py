import csv

def calcular_saldo(csv_file):
    ganancia = 0.0  # Negativos (saldo favorable)
    perdida = 0.0   # Positivos (saldo desfavorable)

    with open(csv_file, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            try:
                diferencia = float(fila['Diferencia'])
                if diferencia < 0:
                    ganancia += abs(diferencia)  # Lo que se gana
                else:
                    perdida += diferencia       # Lo que se pierde
            except ValueError:
                print(f"Valor no numérico encontrado en fila: {fila}")

    saldo_neto = ganancia - perdida

    print(f"Total Ganado (negativos): {ganancia}")
    print(f"Total Perdido (positivos): {perdida}")
    print(f"Saldo Neto (ganancia - pérdida): {saldo_neto}")

# Ejecutar la función con el archivo
calcular_saldo("reporte_errores.csv")
