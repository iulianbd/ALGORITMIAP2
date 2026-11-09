import time
import matplotlib.pyplot as plt
from p2 import activity_selection, generate_activities

def realizar_experimentos():
    tamanos = [100, 500, 1000, 5000]
    tiempos = []
    num_seleccionadas = []
    porcentajes = []

    for n in tamanos:
        # 1. Generar la entrada estrictamente con la misma semilla
        actividades = generate_activities(n, seed=42)
        
        # 2. Medir el tiempo (10 repeticiones sobre la MISMA entrada)
        tiempo_total = 0
        for _ in range(10):
            inicio = time.perf_counter()
            resultado = activity_selection(actividades)
            fin = time.perf_counter()
            tiempo_total += (fin - inicio)
        
        tiempo_medio = tiempo_total / 10
        tiempos.append(tiempo_medio)
        
        # 3. Extraer métricas de la última ejecución
        seleccionadas = len(resultado)
        num_seleccionadas.append(seleccionadas)
        porcentajes.append((seleccionadas / n) * 100)

    # Gráfica 1: Tiempo vs Tamaño
    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, tiempos, marker='o', linestyle='-', color='b')
    plt.title('Tiempo de ejecución vs Tamaño de entrada')
    plt.xlabel('Tamaño de entrada (N)')
    plt.ylabel('Tiempo medio (s)')
    plt.grid(True)
    plt.savefig('grafica_tiempo.png')  # Guarda la imagen en el directorio actual
    plt.close()

    # Gráfica 2: Número de actividades seleccionadas
    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, num_seleccionadas, marker='s', linestyle='-', color='g')
    plt.title('Actividades seleccionadas vs Tamaño de entrada')
    plt.xlabel('Tamaño de entrada (N)')
    plt.ylabel('Nº de actividades')
    plt.grid(True)
    plt.savefig('grafica_cantidad.png')
    plt.close()

    # Gráfica 3: Porcentaje de selección
    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, porcentajes, marker='^', linestyle='-', color='r')
    plt.title('Porcentaje de selección vs Tamaño de entrada')
    plt.xlabel('Tamaño de entrada (N)')
    plt.ylabel('Porcentaje (%)')
    plt.grid(True)
    plt.savefig('grafica_porcentaje.png')
    plt.close()

if __name__ == "__main__":
    realizar_experimentos()