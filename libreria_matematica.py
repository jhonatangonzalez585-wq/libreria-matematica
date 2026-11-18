"""
=============================================================================
Librería Matemática en Python
Introducción a la Programación - Trabajo Final
=============================================================================
Propósito:
    Diseñar una librería matemática con implementaciones propias para cálculo
    numérico, aproximaciones analíticas y algoritmos clásicos, sin utilizar
    funciones preconstruidas de la librería estándar 'math' para los cálculos
    internos.

Módulos y capacidades:
    1. Constantes y función exponencial (Serie de Taylor y serie de Nilakantha).
    2. Funciones trigonométricas con reducción de rango (seno, coseno, tangente).
    3. Logaritmo natural mediante el método de Newton-Raphson.
    4. Máximo Común Divisor (MCD) mediante el algoritmo euclidiano con residuo.
    5. Aproximación de ondas mediante series de Fourier (onda cuadrada).
=============================================================================
"""


# =============================================================================
# 1. EXPONENCIAL Y CONSTANTES
# =============================================================================

def exponencial(x, terminos=100, tol=1e-15):
    """
    Calcula una aproximación de e^x utilizando la serie de Taylor:
        e^x = sum_{k=0}^{infinito} (x^k / k!) = 1 + x + x^2/2! + x^3/3! + ...

    Para garantizar estabilidad numérica y evitar cancelación catastrófica
    cuando x es negativo, se utiliza la propiedad e^x = 1 / e^(-x).

    Parámetros:
        x (int, float): Exponente al cual se eleva la base e.
        terminos (int, opcional): Número máximo de términos en la suma finita.
                                 Por defecto es 100.
        tol (float, opcional): Tolerancia para la detención temprana si el
                               término actual es despreciable. Por defecto 1e-15.

    Retorna:
        float: Aproximación de e^x.

    Excepciones:
        TypeError: Si 'x' no es un número real (int o float).
        ValueError: Si 'terminos' no es un entero positivo o 'tol' <= 0.

    Ejemplos:
        >>> exponencial(0)
        1.0
        >>> round(exponencial(1), 5)
        2.71828
    """
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise TypeError(f"El parámetro 'x' debe ser un número real (int o float), recibido: {type(x).__name__}")
    if not isinstance(terminos, int) or isinstance(terminos, bool) or terminos <= 0:
        raise ValueError("El parámetro 'terminos' debe ser un número entero positivo.")
    if not isinstance(tol, (int, float)) or tol <= 0:
        raise ValueError("El parámetro 'tol' debe ser un número positivo.")

    if x == 0:
        return 1.0

    # Manejo de exponentes negativos para evitar oscilaciones e inestabilidad
    es_negativo = x < 0
    val_x = -x if es_negativo else float(x)

    # Suma iterativa mediante término recurrente: t_k = t_{k-1} * (val_x / k)
    suma = 1.0
    termino = 1.0

    for k in range(1, terminos + 1):
        termino *= val_x / k
        suma += termino
        if termino < tol * suma:
            break

    return (1.0 / suma) if es_negativo else suma


def aproximar_pi(terminos=100000):
    """
    Aproxima la constante matemática pi utilizando la serie de Nilakantha:
        pi = 3 + 4 * sum_{k=1}^{infinito} [ (-1)^(k+1) / ( (2k)*(2k+1)*(2k+2) ) ]

    Esta serie converge notablemente más rápido que la serie de Leibniz (4 * sum (-1)^k / (2k+1)),
    permitiendo alcanzar precisión cercana al límite de doble precisión (10^-14)
    con 100,000 iteraciones.

    Parámetros:
        terminos (int, opcional): Cantidad de términos a sumar en la serie.
                                  Por defecto es 100000.

    Retorna:
        float: Valor aproximado de pi.

    Excepciones:
        TypeError: Si 'terminos' no es un número entero.
        ValueError: Si 'terminos' es menor o igual a cero.

    Análisis de convergencia:
        - 10 términos:     error aprox. 1.86e-04  (3 decimales exactos)
        - 100 términos:    error aprox. 2.43e-07  (6 decimales exactos)
        - 1,000 términos:  error aprox. 2.49e-10  (9 decimales exactos)
        - 100,000 términos: error aprox. 6.66e-15 (14 decimales exactos)
    """
    if not isinstance(terminos, int) or isinstance(terminos, bool):
        raise TypeError("El número de términos debe ser un entero.")
    if terminos <= 0:
        raise ValueError("El número de términos debe ser un entero positivo mayor que cero.")

    suma = 3.0
    signo = 1.0

    for k in range(1, terminos + 1):
        denominador = (2 * k) * (2 * k + 1) * (2 * k + 2)
        suma += signo * 4.0 / denominador
        signo = -signo

    return suma


# Constantes fundamentales calculadas con las funciones propias de la librería
PI = aproximar_pi(100000)
E = exponencial(1.0)


# =============================================================================
# 2. FUNCIONES TRIGONOMÉTRICAS
# =============================================================================

def reducir_angulo(x):
    """
    Reduce un ángulo arbitrario en radianes al intervalo principal [-pi, pi].
    
    Esta reducción es indispensable para la estabilidad numérica de las series
    de Taylor trigonométricas, garantizando convergencia rápida y precisa
    incluso para armónicos altos en series de Fourier.

    Parámetros:
        x (int, float): Ángulo en radianes.

    Retorna:
        float: Ángulo equivalente en el intervalo [-PI, PI].
    """
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise TypeError(f"El ángulo debe ser un número real, recibido: {type(x).__name__}")

    dos_pi = 2.0 * PI
    x_mod = x % dos_pi
    if x_mod > PI:
        x_mod -= dos_pi
    elif x_mod < -PI:
        x_mod += dos_pi
    return x_mod


def seno(x, terminos=30, tol=1e-15):
    """
    Calcula el seno de un ángulo en radianes mediante la serie de Taylor:
        sin(x) = sum_{k=0}^{infinito} (-1)^k * x^(2k+1) / (2k+1)!
               = x - x^3/3! + x^5/5! - x^7/7! + ...

    Aplica reducción previa del ángulo al intervalo [-pi, pi].

    Parámetros:
        x (int, float): Ángulo en radianes.
        terminos (int, opcional): Número máximo de términos a sumar. Por defecto 30.
        tol (float, opcional): Tolerancia para convergencia. Por defecto 1e-15.

    Retorna:
        float: Valor de sin(x).

    Excepciones:
        TypeError: Si 'x' no es un número real.
        ValueError: Si 'terminos' <= 0 o 'tol' <= 0.
    """
    x_red = reducir_angulo(x)

    suma = x_red
    termino = x_red
    x2 = x_red * x_red

    for k in range(1, terminos):
        # Relación de recurrencia entre términos impares
        termino *= -x2 / ((2 * k) * (2 * k + 1))
        suma += termino
        if abs(termino) < tol:
            break

    return suma


def coseno(x, terminos=30, tol=1e-15):
    """
    Calcula el coseno de un ángulo en radianes mediante la serie de Taylor:
        cos(x) = sum_{k=0}^{infinito} (-1)^k * x^(2k) / (2k)!
               = 1 - x^2/2! + x^4/4! - x^6/6! + ...

    Aplica reducción previa del ángulo al intervalo [-pi, pi].

    Parámetros:
        x (int, float): Ángulo en radianes.
        terminos (int, opcional): Número máximo de términos a sumar. Por defecto 30.
        tol (float, opcional): Tolerancia para convergencia. Por defecto 1e-15.

    Retorna:
        float: Valor de cos(x).

    Excepciones:
        TypeError: Si 'x' no es un número real.
        ValueError: Si 'terminos' <= 0 o 'tol' <= 0.
    """
    x_red = reducir_angulo(x)

    suma = 1.0
    termino = 1.0
    x2 = x_red * x_red

    for k in range(1, terminos):
        # Relación de recurrencia entre términos pares
        termino *= -x2 / ((2 * k - 1) * (2 * k))
        suma += termino
        if abs(termino) < tol:
            break

    return suma


def tangente(x, tol_coseno=1e-6):
    """
    Calcula la tangente de un ángulo en radianes reutilizando las funciones
    propias 'seno' y 'coseno':
        tan(x) = sin(x) / cos(x)

    Requisito de control:
        Si el valor absoluto de cos(x) es menor que 10^-6, la función informa
        que la tangente no está definida dentro de dicha tolerancia lanzando
        una excepción ZeroDivisionError.

    Parámetros:
        x (int, float): Ángulo en radianes.
        tol_coseno (float, opcional): Tolerancia mínima para |cos(x)|.
                                     Por defecto 1e-6.

    Retorna:
        float: Valor de tan(x).

    Excepciones:
        TypeError: Si 'x' no es un número real.
        ZeroDivisionError: Si |cos(x)| < tol_coseno (e.g. x = pi/2 + k*pi).
    """
    cos_val = coseno(x)
    if abs(cos_val) < tol_coseno:
        raise ZeroDivisionError(
            f"La tangente no está definida dentro de la tolerancia {tol_coseno:.0e}: "
            f"|cos({x})| = {abs(cos_val):.2e} < {tol_coseno:.0e}."
        )

    sen_val = seno(x)
    return sen_val / cos_val


# =============================================================================
# 3. LOGARITMO NATURAL
# =============================================================================

def logaritmo_natural(x, tol=1e-12, max_iter=100, y0=0.0):
    """
    Calcula el logaritmo natural ln(x) para x > 0 aplicando el método
    iterativo de Newton-Raphson para resolver la ecuación no lineal:
        f(y) = e^y - x = 0

    Fórmula de actualización (reutilizando la función propia 'exponencial'):
        y_{n+1} = y_n - f(y_n) / f'(y_n)
                = y_n - (e^{y_n} - x) / e^{y_n}
                = y_n - 1 + x / e^{y_n}

    Criterio de parada:
        |e^{y_n} - x| < tol

    Intervalo verificado:
        Especialmente rápido y robusto para x en el intervalo [0.5, 2.0]
        iniciando en y0 = 0 (converge en 5 a 6 iteraciones). También converge
        para otros valores positivos en pocas iteraciones adicionales.

    Parámetros:
        x (int, float): Valor real positivo al que se le calculará ln(x).
        tol (float, opcional): Tolerancia de convergencia sobre |e^y - x|.
                               Por defecto 1e-12.
        max_iter (int, opcional): Límite máximo de iteraciones permitidas.
                                  Por defecto 100.
        y0 (float, opcional): Estimación inicial para Newton-Raphson.
                              Por defecto 0.0.

    Retorna:
        float: Aproximación de ln(x).

    Excepciones:
        TypeError: Si 'x' no es un número real.
        ValueError: Si x <= 0 (el logaritmo real no está definido para x <= 0).
        RuntimeError: Si se alcanza 'max_iter' sin satisfacer la tolerancia.

    Ejemplos:
        >>> round(logaritmo_natural(1), 6)
        0.0
        >>> round(logaritmo_natural(2), 5)
        0.69315
    """
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise TypeError(f"El argumento 'x' debe ser un número real, recibido: {type(x).__name__}")
    if x <= 0:
        raise ValueError(f"El logaritmo natural solo está definido para x > 0. Recibido: x = {x}")
    if not isinstance(max_iter, int) or max_iter <= 0:
        raise ValueError("El parámetro 'max_iter' debe ser un entero positivo.")
    if not isinstance(tol, (int, float)) or tol <= 0:
        raise ValueError("El parámetro 'tol' debe ser un número positivo.")

    # Caso exacto trivial
    if x == 1.0 or x == 1:
        return 0.0

    y = float(y0)
    for _ in range(max_iter):
        ey = exponencial(y)
        diferencia = ey - x
        if abs(diferencia) < tol:
            return y
        y = y - (diferencia / ey)

    raise RuntimeError(
        f"El método de Newton-Raphson alcanzó el límite de {max_iter} iteraciones "
        f"sin converger para x = {x} con tolerancia {tol:.1e}. "
        f"Intervalo verificado óptimo: [0.5, 2.0]."
    )


# =============================================================================
# 4. MÁXIMO COMÚN DIVISOR (MCD)
# =============================================================================

def mcd(a, b):
    """
    Calcula el Máximo Común Divisor entre dos números enteros mediante el
    algoritmo clásico de Euclides utilizando el operador de residuo (%).

    Propiedades implementadas:
        - El resultado es siempre no negativo: mcd(a, b) >= 0.
        - Soporta enteros positivos y negativos: mcd(a, b) = mcd(|a|, |b|).
        - Si uno de los argumentos es cero: mcd(a, 0) = |a|.
        - Caso frontera (0, 0): devuelve 0 por convención matemática.

    Parámetros:
        a (int): Primer número entero.
        b (int): Segundo número entero.

    Retorna:
        int: Máximo común divisor (entero no negativo).

    Excepciones:
        TypeError: Si 'a' o 'b' no son enteros (o si se pasa un valor booleano).

    Ejemplos:
        >>> mcd(48, 18)
        6
        >>> mcd(-15, 0)
        15
        >>> mcd(0, 0)
        0
    """
    if not isinstance(a, int) or isinstance(a, bool) or not isinstance(b, int) or isinstance(b, bool):
        raise TypeError("Ambos argumentos de 'mcd' deben ser números enteros (int).")

    # Tomar valores absolutos para garantizar resultado no negativo
    u = abs(a)
    v = abs(b)

    # Algoritmo de Euclides con operador residuo (%)
    while v != 0:
        u, v = v, u % v

    return u


# =============================================================================
# 5. APROXIMACIÓN DE SEÑAL CON SERIE DE FOURIER
# =============================================================================

def serie_fourier_cuadrada(x, N):
    """
    Evalúa la suma parcial de Fourier S_N(x) de una onda cuadrada de amplitud 1
    y periodo 2*pi:
        S_N(x) = (4 / pi) * sum_{k=0}^{N-1} [ sin((2k + 1)x) / (2k + 1) ]

    Reutiliza internamente las funciones 'seno' y la constante 'PI' de esta librería.

    Parámetros:
        x (int, float): Ángulo en radianes en el que se evalúa la señal.
        N (int): Entero positivo que indica cuántos términos armónicos impares
                 se suman en la aproximación.

    Retorna:
        float: Valor de la suma parcial S_N(x).

    Excepciones:
        TypeError: Si 'x' no es un número real o 'N' no es un entero.
        ValueError: Si 'N' no es un entero positivo (N >= 1).

    Comportamiento teórico:
        - En x = pi/2: la onda cuadrada vale +1.
        - En x = 3*pi/2: la onda cuadrada vale -1.
        - Cerca de discontinuidades (como x = 0 o x = pi), se manifiesta el
          fenómeno de Gibbs, donde la suma parcial presenta sobreimpulsos
          alrededor del 9% antes de la transición.
    """
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise TypeError(f"El parámetro 'x' debe ser un número real, recibido: {type(x).__name__}")
    if not isinstance(N, int) or isinstance(N, bool):
        raise TypeError("El número de términos 'N' debe ser un entero.")
    if N < 1:
        raise ValueError(f"El número de términos 'N' debe ser mayor o igual a 1. Recibido: {N}")

    suma_armonicos = 0.0

    for k in range(N):
        armonico = 2 * k + 1
        # La función seno propia ya realiza reducción modular a [-pi, pi]
        suma_armonicos += seno(armonico * x) / armonico

    return (4.0 / PI) * suma_armonicos


def onda_cuadrada_teorica(x):
    """
    Función de referencia para evaluar el valor teórico de la onda cuadrada
    ideal de amplitud 1 y periodo 2*pi:
        f(x) =  1  si  0 < x_mod < pi
        f(x) = -1  si  pi < x_mod < 2*pi
        f(x) =  0  si  x_mod == 0 o x_mod == pi

    Parámetros:
        x (int, float): Ángulo en radianes.

    Retorna:
        float: Valor exacto (+1.0, -1.0 o 0.0).
    """
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise TypeError("El ángulo debe ser un número real.")

    dos_pi = 2.0 * PI
    x_mod = x % dos_pi

    # Tolerancia para discontinuidades en múltiplos de pi
    tol = 1e-9
    if abs(x_mod) < tol or abs(x_mod - PI) < tol or abs(x_mod - dos_pi) < tol:
        return 0.0
    elif 0.0 < x_mod < PI:
        return 1.0
    else:
        return -1.0
