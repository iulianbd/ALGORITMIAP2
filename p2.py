#Utilidades para medir tiempos de ejecución y representar resultados.

from collections.abc import Callable, Iterable, Sequence
from typing import Any
import time  # Proporciona temporizadores de alta resolución.

import matplotlib.pyplot as plt  # Biblioteca utilizada para crear gráficas.

def time_measure(
    f: Callable[[Any], Any],
    dataprep: Callable[[int], Any],
    Nlist: Sequence[int],
    Nrep: int = 1000,
    Nstat: int = 100,
) -> list[tuple[float, float]]:
    """Mide el tiempo medio y la varianza de una función.

    Para cada tamaño ``n`` de ``Nlist``:

    1. Se genera un conjunto de datos mediante ``dataprep(n)``.
    2. Se ejecuta ``f(data)`` varias veces.
    3. Se repite la medición para obtener varias observaciones estadísticas.
    4. Se calcula la media y la varianza de esas observaciones.

    Args:
        f: Función que se desea medir. Debe aceptar un único argumento.
        dataprep: Función que genera los datos de prueba a partir de ``n``.
        Nlist: Secuencia de tamaños de entrada que se van a estudiar.
        Nrep: Número de ejecuciones de ``f`` en cada medición parcial.
        Nstat: Número de mediciones parciales para cada tamaño de entrada.

    Returns:
        Una lista de tuplas ``(media, varianza)``. Cada posición corresponde
        al tamaño de entrada situado en la misma posición de ``Nlist``.

    Raises:
        ValueError: Si ``Nrep`` o ``Nstat`` no son positivos.
    """
    # Validar los parámetros evita realizar mediciones sin sentido, como
    # dividir entre cero o no recoger ninguna observación.
    if Nrep <= 0 or Nstat <= 0:
        raise ValueError("Nrep y Nstat deben ser mayores que cero")

    # Esta lista almacenará un resultado para cada tamaño de entrada.
    results: list[tuple[float, float]] = []

    # Recorremos cada tamaño de entrada que queremos estudiar.
    for n in Nlist:
        # Aquí se guardará una medición media por cada repetición estadística.
        partial_times: list[float] = []

        for _ in range(Nstat):
            # Generar los datos fuera del intervalo medido evita incluir en el
            # tiempo de la función el coste de preparar la entrada.
            data: Any = dataprep(n)

            # perf_counter() es apropiado para medir intervalos de tiempo
            # porque utiliza un reloj de alta resolución.
            start_time: float = time.perf_counter()

            # Ejecutar varias veces reduce el efecto de pequeñas variaciones
            # del sistema operativo y permite obtener un tiempo medio.
            for _ in range(Nrep):
                f(data)

            end_time: float = time.perf_counter()

            # El tiempo total se convierte en tiempo medio por ejecución.
            time_per_execution: float = (end_time - start_time) / Nrep
            partial_times.append(time_per_execution)

        # Media aritmética de las mediciones parciales.
        mean_value: float = sum(partial_times) / Nstat

        # Varianza poblacional: se divide entre el número total de mediciones.
        variance_value: float = sum(
            (value - mean_value) ** 2 for value in partial_times
        ) / Nstat

        # Asociamos la media y la varianza al tamaño de entrada actual.
        results.append((mean_value, variance_value))

    return results


# Función auxiliar para generar una gráfica de una serie de datos.
def plot_single_curve(
    x: Sequence[float],
    y: Sequence[float],
    title: str = "Gráfica de datos",
    xlabel: str = "Eje X",
    ylabel: str = "Eje Y",
    label: str | None = None,
    style: str = "o-",
    color: str = "b",
    grid: bool = True,
    filename: str | None = None,
    figsize: tuple[float, float] = (8.0, 5.0),
) -> None:
    """Genera y muestra una gráfica para una única serie de datos.

    Args:
        x: Valores que se mostrarán en el eje horizontal.
        y: Valores que se mostrarán en el eje vertical.
        title: Título de la gráfica.
        xlabel: Etiqueta del eje horizontal.
        ylabel: Etiqueta del eje vertical.
        label: Texto de la leyenda. Si es ``None``, no se muestra leyenda.
        style: Formato de la línea y los marcadores, por ejemplo ``"o-"``.
        color: Color de la curva, por ejemplo ``"b"`` o ``"tab:blue"``.
        grid: Indica si se debe mostrar una cuadrícula.
        filename: Nombre del fichero de salida. Si es ``None``, no se guarda.
        figsize: Tupla ``(ancho, alto)`` expresada en pulgadas.

    Returns:
        ``None``. La función muestra la gráfica y, opcionalmente, la guarda.

    Raises:
        ValueError: Si ``x`` e ``y`` no tienen la misma longitud.
    """
    # Una curva necesita un valor x para cada valor y.
    if len(x) != len(y):
        raise ValueError("x e y deben tener la misma longitud")

    # Crear una figura nueva evita mezclar esta gráfica con otra anterior.
    plt.figure(figsize=figsize)

    # Dibujar la serie de datos con el estilo y el color solicitados.
    plt.plot(x, y, style, color=color, label=label)

    # Añadir información descriptiva facilita la interpretación de la gráfica.
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # La cuadrícula es opcional para no imponer una presentación concreta.
    if grid:
        plt.grid(True, linestyle="--", alpha=0.6)

    # Solo se muestra la leyenda cuando se ha proporcionado una etiqueta.
    if label is not None:
        plt.legend(loc="best")

    # Ajustar automáticamente los márgenes evita que se corten las etiquetas.
    plt.tight_layout()

    # Guardar la figura únicamente cuando se ha indicado un nombre de fichero.
    if filename is not None:
        # split(".") funciona en ejemplos sencillos; pathlib sería preferible
        # en programas más robustos para trabajar con extensiones de fichero.
        file_format: str = filename.rsplit(".", maxsplit=1)[-1]
        plt.savefig(filename, format=file_format, dpi=300)

    # Mostrar la figura en pantalla.
    plt.show()

# LIRAS, ns si se utilizaran las funciones time_measure y plot_single_curve para las graficas de despues, pero las he metido por si acaso.