import time
import matplotlib.pyplot as plt
from p2 import job_scheduling, generate_jobs

def realizar_experimentos_tareas():
    tamanos = [100, 500, 1000, 5000]
    tiempos = []
    beneficios_totales = []
    porcentajes = []

    for n in tamanos:
        # 1. Generar la entrada de tareas
        tareas = generate_jobs(n, seed=42)
        
        # 2. Medir el tiempo (10 repeticiones sobre la MISMA entrada)
        tiempo_total = 0
        for _ in range(10):
            inicio = time.perf_counter()
            schedule, total_profit = job_scheduling(tareas)
            fin = time.perf_counter()
            tiempo_total += (fin - inicio)
        
        tiempo_medio = tiempo_total / 10
        tiempos.append(tiempo_medio)
        
        # 3. Guardar el beneficio total (lo devuelve directamente la función)
        beneficios_totales.append(total_profit)
        
        # 4. Calcular el porcentaje de tareas seleccionadas
        # schedule tiene longitud max_deadline y contiene la tarea o None en los huecos vacíos
        num_seleccionadas = sum(1 for hueco in schedule if hueco is not None)
        porcentajes.append((num_seleccionadas / n) * 100)

    # Gráfica 1: Número de tareas vs Tiempo
    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, tiempos, marker='o', linestyle='-', color='b')
    plt.title('Tiempo de ejecución vs Número de tareas')
    plt.xlabel('Número de tareas (N)')
    plt.ylabel('Tiempo medio (s)')
    plt.grid(True)
    plt.savefig('grafica_tareas_tiempo.png')
    plt.close()

    # Gráfica 2: Número de tareas vs Beneficio total
    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, beneficios_totales, marker='s', linestyle='-', color='g')
    plt.title('Beneficio total vs Número de tareas')
    plt.xlabel('Número de tareas (N)')
    plt.ylabel('Beneficio total')
    plt.grid(True)
    plt.savefig('grafica_tareas_beneficio.png')
    plt.close()

    # Gráfica 3: Número de tareas vs Porcentaje seleccionado
    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, porcentajes, marker='^', linestyle='-', color='r')
    plt.title('Porcentaje de selección vs Número de tareas')
    plt.xlabel('Número de tareas (N)')
    plt.ylabel('Porcentaje seleccionado (%)')
    plt.grid(True)
    plt.savefig('grafica_tareas_porcentaje.png')
    plt.close()

if __name__ == "__main__":
    realizar_experimentos_tareas()