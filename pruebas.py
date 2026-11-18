"""
=============================================================================
Suite de Pruebas y Verificación - Librería Matemática
Introducción a la Programación - Trabajo Final
=============================================================================
Propósito:
    Importar 'libreria_matematica' y verificar rigurosamente cada una de sus
    operaciones frente a valores teóricos y funciones de referencia del
    módulo estándar 'math'.

Casos evaluados:
    1. Exponencial y constantes: e^0, e^1, pi (análisis de términos y error).
    2. Trigonometría: sin(pi/6), cos(0), tan(pi/4) y manejo de tan(pi/2).
    3. Logaritmo natural: ln(1), ln(2), intervalo [0.5, 2.0], manejo de ln(0).
    4. Máximo común divisor: mcd(48, 18), mcd(-15, 0), mcd(0, 0), negativos.
    5. Serie de Fourier: onda cuadrada en x = pi/2, x = 3*pi/2 y x = 0.1
       para N = 1, 5 y 15, con tabla comparativa y gráfico en consola.
=============================================================================
"""

import math
import libreria_matematica as lm


# =============================================================================
# UTILIDADES DE REPORTE Y FORMATEO
# =============================================================================

def imprimir_titulo(titulo):
    ancho = 78
    print("\n" + "=" * ancho)
    print(f" {titulo.upper()} ".center(ancho, "="))
    print("=" * ancho)


def imprimir_subtitulo(subtitulo):
    print(f"\n--- {subtitulo} ---")


def registrar_resultado(descripcion, obtenido, referencia, tolerancia=1e-5):
    """
    Compara un valor obtenido con una referencia y reporta el error absoluto.
    Retorna True si la prueba pasa dentro de la tolerancia.
    """
    error_abs = abs(obtenido - referencia)
    pasa = error_abs <= tolerancia
    estado = "[OK]" if pasa else "[FALLO]"
    print(f"{estado} {descripcion}")
    print(f"     Calculado : {obtenido:18.10f}")
    print(f"     Referencia: {referencia:18.10f}")
    print(f"     Error Abs : {error_abs:18.2e}  (Tol: {tolerancia:.1e})")
    return pasa


# =============================================================================
# 1. PRUEBAS: EXPONENCIAL Y CONSTANTES
# =============================================================================

def probar_exponencial_y_constantes():
    imprimir_titulo("1. Exponencial y Constantes")
    pruebas_ok = 0
    total = 0

    # Caso e^0 = 1
    total += 1
    if registrar_resultado("Exponencial en x = 0 (e^0 = 1.0)", lm.exponencial(0), math.exp(0), 1e-15):
        pruebas_ok += 1

    # Caso e^1 ~ 2.71828
    total += 1
    if registrar_resultado("Constante e evaluada en x = 1 (e^1)", lm.exponencial(1), math.exp(1), 1e-12):
        pruebas_ok += 1

    # Caso e^(-2) para comprobar estabilidad de exponentes negativos
    total += 1
    if registrar_resultado("Exponente negativo e^(-2)", lm.exponencial(-2), math.exp(-2), 1e-12):
        pruebas_ok += 1

    # Constante PI aproximada con la serie de Nilakantha
    total += 1
    if registrar_resultado("Constante PI (Nilakantha, 100,000 términos)", lm.PI, math.pi, 1e-12):
        pruebas_ok += 1

    # Tabla de convergencia de PI según el número de términos
    imprimir_subtitulo("Convergencia de pi según número de términos (Nilakantha)")
    print(f"{'Términos':>10} | {'Valor Calculado':>18} | {'Valor math.pi':>18} | {'Error Absoluto':>14}")
    print("-" * 68)
    for term in [10, 50, 100, 500, 1000, 10000, 100000]:
        val = lm.aproximar_pi(term)
        err = abs(val - math.pi)
        print(f"{term:10d} | {val:18.14f} | {math.pi:18.14f} | {err:14.2e}")

    # Validación de errores de tipo y valor
    imprimir_subtitulo("Validación de entradas inválidas")
    try:
        lm.exponencial("invalido")
        print("[FALLO] No detectó tipo no numérico en exponencial.")
    except TypeError:
        print("[OK] Detectó correctamente TypeError en exponencial(str).")
        pruebas_ok += 1
    total += 1

    return pruebas_ok, total


# =============================================================================
# 2. PRUEBAS: FUNCIONES TRIGONOMÉTRICAS
# =============================================================================

def probar_trigonometria():
    imprimir_titulo("2. Funciones Trigonométricas")
    pruebas_ok = 0
    total = 0

    # sin(pi/6) = 0.5
    total += 1
    if registrar_resultado("seno(pi/6) -> esperado 0.5", lm.seno(lm.PI / 6.0), math.sin(math.pi / 6.0), 1e-12):
        pruebas_ok += 1

    # cos(0) = 1.0
    total += 1
    if registrar_resultado("coseno(0) -> esperado 1.0", lm.coseno(0.0), math.cos(0.0), 1e-15):
        pruebas_ok += 1

    # tan(pi/4) = 1.0
    total += 1
    if registrar_resultado("tangente(pi/4) -> esperado 1.0", lm.tangente(lm.PI / 4.0), math.tan(math.pi / 4.0), 1e-12):
        pruebas_ok += 1

    # Verificación de reducción de argumento para ángulos grandes (armónicos altos)
    total += 1
    angulo_grande = 50.0 * lm.PI + (lm.PI / 6.0)
    ref_grande = math.sin(50.0 * math.pi + (math.pi / 6.0))
    if registrar_resultado("seno(50*pi + pi/6) con reducción de ángulo", lm.seno(angulo_grande), ref_grande, 1e-12):
        pruebas_ok += 1

    # Verificación de tangente no definida en x = pi/2 (|cos| < 10^-6)
    imprimir_subtitulo("Caso frontera de tangente en x = pi/2")
    total += 1
    try:
        lm.tangente(lm.PI / 2.0)
        print("[FALLO] tangente(pi/2) no lanzó la excepción esperada.")
    except ZeroDivisionError as e:
        print(f"[OK] tangente(pi/2) identificó correctamente la indeterminación:")
        print(f"     Mensaje: {e}")
        pruebas_ok += 1

    return pruebas_ok, total


# =============================================================================
# 3. PRUEBAS: LOGARITMO NATURAL
# =============================================================================

def probar_logaritmo_natural():
    imprimir_titulo("3. Logaritmo Natural (Newton-Raphson)")
    pruebas_ok = 0
    total = 0

    # ln(1) = 0
    total += 1
    if registrar_resultado("logaritmo_natural(1) -> esperado 0.0", lm.logaritmo_natural(1.0), 0.0, 1e-15):
        pruebas_ok += 1

    # ln(2) ~ 0.69315
    total += 1
    if registrar_resultado("logaritmo_natural(2) -> esperado ~0.69315", lm.logaritmo_natural(2.0), math.log(2.0), 1e-10):
        pruebas_ok += 1

    # ln(e) = 1.0
    total += 1
    if registrar_resultado("logaritmo_natural(E) -> esperado 1.0", lm.logaritmo_natural(lm.E), 1.0, 1e-10):
        pruebas_ok += 1

    # Barrido en el intervalo sugerido [0.5, 2.0]
    imprimir_subtitulo("Verificación del intervalo sugerido [0.5, 2.0] con y0 = 0")
    print(f"{'x':>8} | {'ln(x) Calculado':>18} | {'math.log(x)':>18} | {'Error Absoluto':>14}")
    print("-" * 64)
    intervalo_test = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
    todos_ok = True
    for x_val in intervalo_test:
        calc = lm.logaritmo_natural(x_val)
        ref = math.log(x_val)
        err = abs(calc - ref)
        if err > 1e-10:
            todos_ok = False
        print(f"{x_val:8.2f} | {calc:18.12f} | {ref:18.12f} | {err:14.2e}")
    total += 1
    if todos_ok:
        print("[OK] Todas las entradas del intervalo [0.5, 2.0] convergieron con alta precisión.")
        pruebas_ok += 1

    # Manejo de ln(0) y números negativos (x <= 0)
    imprimir_subtitulo("Casos frontera: rechazo de x <= 0")
    total += 1
    try:
        lm.logaritmo_natural(0)
        print("[FALLO] No se rechazó x = 0.")
    except ValueError as e:
        print(f"[OK] Rechazo exitoso de x = 0: '{e}'")
        pruebas_ok += 1

    total += 1
    try:
        lm.logaritmo_natural(-5.0)
        print("[FALLO] No se rechazó x = -5.0.")
    except ValueError as e:
        print(f"[OK] Rechazo exitoso de x < 0: '{e}'")
        pruebas_ok += 1

    return pruebas_ok, total


# =============================================================================
# 4. PRUEBAS: MÁXIMO COMÚN DIVISOR (MCD)
# =============================================================================

def probar_mcd():
    imprimir_titulo("4. Máximo Común Divisor (MCD)")
    pruebas_ok = 0
    total = 0

    casos = [
        ("mcd(48, 18) esperado 6", 48, 18, 6),
        ("mcd(-15, 0) esperado 15 (argumento cero y negativo)", -15, 0, 15),
        ("mcd(0, -15) esperado 15", 0, -15, 15),
        ("mcd(0, 0) esperado 0 (convención)", 0, 0, 0),
        ("mcd(-24, -36) esperado 12 (ambos negativos)", -24, -36, 12),
        ("mcd(101, 103) esperado 1 (coprimos)", 101, 103, 1),
    ]

    for desc, a, b, esperado in casos:
        total += 1
        res = lm.mcd(a, b)
        ref = math.gcd(a, b)
        if res == esperado and res == ref:
            print(f"[OK] {desc} -> Obtenido: {res} | Referencia math.gcd: {ref}")
            pruebas_ok += 1
        else:
            print(f"[FALLO] {desc} -> Obtenido: {res} | Esperado: {esperado}")

    # Validación de tipos inválidos
    imprimir_subtitulo("Validación de tipos inválidos en MCD")
    total += 1
    try:
        lm.mcd(3.5, 7)
        print("[FALLO] mcd permitió número flotante.")
    except TypeError:
        print("[OK] Detectó correctamente que 3.5 no es un entero.")
        pruebas_ok += 1

    total += 1
    try:
        lm.mcd(True, 10)
        print("[FALLO] mcd permitió booleano.")
    except TypeError:
        print("[OK] Detectó correctamente que True es booleano y no entero puro.")
        pruebas_ok += 1

    return pruebas_ok, total


# =============================================================================
# 5. PRUEBAS: SERIE DE FOURIER DE ONDA CUADRADA
# =============================================================================

def probar_serie_fourier():
    imprimir_titulo("5. Aproximación con Serie de Fourier (Onda Cuadrada)")
    pruebas_ok = 0
    total = 0

    puntos_evaluacion = [
        ("pi / 2", lm.PI / 2.0, 1.0),
        ("3*pi / 2", 3.0 * lm.PI / 2.0, -1.0),
        ("0.1 (cercano a 0)", 0.1, 1.0)
    ]
    valores_N = [1, 5, 15]

    print("\nTABLA COMPARATIVA DE SUMAS PARCIALES S_N(x):")
    print("=" * 82)
    encabezado = f"{'Punto x':>18} | {'x (rad)':>8} | {'Teórico':>8} | {'N':>4} | {'S_N(x)':>10} | {'Error Abs':>10}"
    print(encabezado)
    print("-" * 82)

    for etiqueta, x_val, v_teorico in puntos_evaluacion:
        for N in valores_N:
            s_n = lm.serie_fourier_cuadrada(x_val, N)
            err = abs(s_n - v_teorico)
            print(f"{etiqueta:>18} | {x_val:8.4f} | {v_teorico:8.1f} | {N:4d} | {s_n:10.5f} | {err:10.5f}")

    # Verificación de que el error decrece en x = pi/2 al aumentar N
    err_N1 = abs(lm.serie_fourier_cuadrada(lm.PI / 2.0, 1) - 1.0)
    err_N5 = abs(lm.serie_fourier_cuadrada(lm.PI / 2.0, 5) - 1.0)
    err_N15 = abs(lm.serie_fourier_cuadrada(lm.PI / 2.0, 15) - 1.0)

    total += 1
    if err_N15 < err_N5 < err_N1:
        print("\n[OK] En x = pi/2, el error decrece monotónicamente al aumentar N (de 1 a 5 y a 15).")
        pruebas_ok += 1
    else:
        print("\n[FALLO] El error en pi/2 no decreció con N.")

    total += 1
    # En 3*pi/2
    err_3pi_1 = abs(lm.serie_fourier_cuadrada(3.0 * lm.PI / 2.0, 1) - (-1.0))
    err_3pi_15 = abs(lm.serie_fourier_cuadrada(3.0 * lm.PI / 2.0, 15) - (-1.0))
    if err_3pi_15 < err_3pi_1:
        print("[OK] En x = 3*pi/2, la aproximación converge con alta precisión hacia -1.0.")
        pruebas_ok += 1

    # Explicación del comportamiento cerca de discontinuidades (Gibbs)
    print("\n--- ANÁLISIS DEL COMPORTAMIENTO CERCA DE x = 0 (Fenómeno de Gibbs) ---")
    print("En x = 0.1 (cerca del salto de discontinuidad de la onda cuadrada en x = 0):")
    print(f"  - Para N = 1 : S_1(0.1)  = {lm.serie_fourier_cuadrada(0.1, 1):.5f} (transición suave)")
    print(f"  - Para N = 5 : S_5(0.1)  = {lm.serie_fourier_cuadrada(0.1, 5):.5f} (mayor pendiente)")
    print(f"  - Para N = 15: S_15(0.1) = {lm.serie_fourier_cuadrada(0.1, 15):.5f} (sobreimpulso de Gibbs)")
    print("Nota: Alrededor de x = 0 hay una discontinuidad tipo salto (-1 a +1).")
    print("La serie de Fourier genera oscilaciones (ringing) cerca de la esquina con")
    print("un sobreimpulso asintótico de aproximadamente 9% (fenómeno de Gibbs).")

    # Gráfico ASCII opcional de la señal reconstruida en un periodo completo
    graficar_ascii_fourier()

    return pruebas_ok, total


def graficar_ascii_fourier():
    """Genera una visualización gráfica simple en consola de S_15(x) frente a la onda cuadrada."""
    print("\n--- GRÁFICA ASCII DE S_15(x) vs ONDA CUADRADA EN [0, 2*pi] ---")
    alto_lineas = 11
    pasos_x = 35
    print(" +1.5 |" + " " * pasos_x)
    print(" +1.0 |" + "-" * (pasos_x // 2) + "   (Onda Cuadrada Teórica)")
    for i in range(pasos_x + 1):
        x = (i / pasos_x) * (2.0 * lm.PI)
        s15 = lm.serie_fourier_cuadrada(x, 15)
        # Mapear valor [-1.3, +1.3] a una barra de texto
        nivel = int((s15 + 1.3) / 2.6 * 40)
        nivel = max(0, min(40, nivel))
        barra = " " * nivel + "*"
        if i % 5 == 0:
            print(f"x={x:4.2f} |{barra} (val: {s15:+.2f})")
    print(" -1.0 |" + " " * (pasos_x // 2) + "-" * (pasos_x // 2))
    print(" -1.5 |" + " " * pasos_x)


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def ejecutar_todas_las_pruebas():
    print("=" * 78)
    print(" EJECUCIÓN DEL BANCO DE PRUEBAS - LIBRERÍA MATEMÁTICA EN PYTHON ".center(78))
    print("=" * 78)

    ok1, tot1 = probar_exponencial_y_constantes()
    ok2, tot2 = probar_trigonometria()
    ok3, tot3 = probar_logaritmo_natural()
    ok4, tot4 = probar_mcd()
    ok5, tot5 = probar_serie_fourier()

    total_ok = ok1 + ok2 + ok3 + ok4 + ok5
    gran_total = tot1 + tot2 + tot3 + tot4 + tot5

    imprimir_titulo("Resumen General de Resultados")
    print(f"Total de pruebas ejecutadas: {gran_total}")
    print(f"Pruebas aprobadas          : {total_ok}")
    print(f"Pruebas fallidas           : {gran_total - total_ok}")
    porcentaje = (total_ok / gran_total) * 100
    print(f"Porcentaje de éxito        : {porcentaje:.1f}%")

    if total_ok == gran_total:
        print("\n>>> ¡TODAS LAS PRUEBAS PASARON SATISFACTORIAMENTE! <<<")
    else:
        print("\n>>> ADVERTENCIA: ALGUNAS PRUEBAS FALLARON <<<")


if __name__ == "__main__":
    ejecutar_todas_las_pruebas()
