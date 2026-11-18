# Librería Matemática en Python - Trabajo Final

**Asignatura:** Introducción a la Programación  
**Fecha límite de entrega:** 24 de noviembre de 2026  
**Lenguaje:** Python 3 (3.8+)  

---

## 1. Propósito del Proyecto

Diseñar e implementar una librería matemática propia (`libreria_matematica.py`) que pueda ser importada desde otros programas de Python para realizar cálculos numéricos fundamentales. 

El proyecto demuestra la aplicación rigurosa de:
- Definición y documentación de funciones (siguiendo directrices PEP 257).
- Estructuras condicionales y ciclos iterativos eficientes con relaciones de recurrencia.
- Validación de tipos y rangos de entrada con manejo explícito de excepciones (`TypeError`, `ValueError`, `ZeroDivisionError`, `RuntimeError`).
- Reutilización de código entre módulos internos.
- Verificación exhaustiva de cálculos numéricos frente a casos teóricos y funciones de referencia del módulo estándar `math`.

---

## 2. Estructura del Repositorio

```text
libreria_matematica/
├── libreria_matematica.py   # Módulo principal con todas las funciones matemáticas
├── pruebas.py               # Suite de pruebas automatizadas y reportes de error
├── README.md                # Documentación técnica, métodos y comparativas
└── .gitignore               # Archivos excluidos del control de versiones
```

---

## 3. Instrucciones de Ejecución

### Requisitos previos
- Disponer de Python 3 instalado en el sistema (versión 3.8 o superior).
- No se requieren librerías externas de terceros (solo la biblioteca estándar de Python).

### Cómo ejecutar la suite de pruebas
Abra una terminal o consola de comandos en el directorio del proyecto y ejecute:

```bash
python pruebas.py
```

### Cómo usar la librería en un programa propio
Puede importar el módulo directamente en cualquier script de Python:

```python
import libreria_matematica as lm

# 1. Constantes y exponencial
print("Constante e :", lm.E)
print("Constante pi:", lm.PI)
print("e^2.5       :", lm.exponencial(2.5))

# 2. Funciones trigonométricas
print("sen(pi/6)   :", lm.seno(lm.PI / 6))
print("cos(pi/3)   :", lm.coseno(lm.PI / 3))
print("tan(pi/4)   :", lm.tangente(lm.PI / 4))

# 3. Logaritmo natural
print("ln(2)       :", lm.logaritmo_natural(2))

# 4. Máximo común divisor
print("MCD(48, 18) :", lm.mcd(48, 18))

# 5. Serie de Fourier (Onda cuadrada)
print("S_15(pi/2)  :", lm.serie_fourier_cuadrada(lm.PI / 2, N=15))
```

---

## 4. Métodos Matemáticos Utilizados

### 4.1. Exponencial y Constantes

#### Función $e^x$ (Serie de Taylor)
Se aproxima mediante la serie de potencias:
$$e^x = \sum_{k=0}^{\infty} \frac{x^k}{k!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots$$

- **Cálculo eficiente del término:** Para evitar el cálculo de factoriales gigantescos, se utiliza la relación de recurrencia $t_k = t_{k-1} \cdot \frac{x}{k}$.
- **Estabilidad numérica para exponentes negativos:** Para valores $x < 0$, evaluar directamente la serie alternada provoca *cancelación catastrófica*. Por ende, se implementó la identidad $e^x = \frac{1}{e^{|x|}}$.
- **Constante $e$:** Se obtiene evaluando la función propia en $x = 1$ ($e = \text{exponencial}(1.0)$), alcanzando un error absoluto menor a $4.44 \times 10^{-16}$.

#### Constante $\pi$ (Serie de Nilakantha)
Se aproxima mediante la serie acelerada de Nilakantha:
$$\pi = 3 + 4 \sum_{k=1}^{\infty} \frac{(-1)^{k+1}}{(2k)(2k+1)(2k+2)}$$

**Análisis de términos utilizados vs. precisión obtenida:**

| Términos ($k$) | Valor Aproximado | Referencia `math.pi` | Error Absoluto | Precisión / Cifras Exactas |
| :---: | :---: | :---: | :---: | :---: |
| **10** | 3.14140671849650 | 3.14159265358979 | $1.86 \times 10^{-4}$ | 3 decimales correctos |
| **50** | 3.14159076984980 | 3.14159265358979 | $1.88 \times 10^{-6}$ | 5 decimales correctos |
| **100** | 3.14159241097198 | 3.14159265358979 | $2.43 \times 10^{-7}$ | 6 decimales correctos |
| **500** | 3.14159265160176 | 3.14159265358979 | $1.99 \times 10^{-9}$ | 8 decimales correctos |
| **1,000** | 3.14159265334054 | 3.14159265358979 | $2.49 \times 10^{-10}$ | 9 decimales correctos |
| **10,000** | 3.14159265358954 | 3.14159265358979 | $2.55 \times 10^{-13}$ | 12 decimales correctos |
| **100,000** | 3.14159265358979 | 3.14159265358979 | $6.66 \times 10^{-15}$ | 14 decimales correctos (casi límite IEEE 754) |

En la librería se fijaron $100,000$ términos para definir la constante `PI`, garantizando una precisión de $\sim 6.66 \times 10^{-15}$ en milisegundos.

---

### 4.2. Funciones Trigonométricas y Reducción de Rango

- **Reducción de argumento al intervalo $[-\pi, \pi]$:** Evaluar la serie de Taylor para ángulos grandes (como los que aparecen en los armónicos altos de Fourier $(2k+1)x$) generaría divergencia o pérdida de precisión severa. Se implementó la función auxiliar `reducir_angulo(x)` que mapea cualquier $x \in \mathbb{R}$ a $[-\pi, \pi]$ mediante congruencia módulo $2\pi$.
- **Seno:**
  $$\sin(x) = \sum_{k=0}^{\infty} (-1)^k \frac{x^{2k+1}}{(2k+1)!}, \quad t_k = -t_{k-1} \cdot \frac{x^2}{(2k)(2k+1)}$$
- **Coseno:**
  $$\cos(x) = \sum_{k=0}^{\infty} (-1)^k \frac{x^{2k}}{(2k)!}, \quad t_k = -t_{k-1} \cdot \frac{x^2}{(2k-1)(2k)}$$
- **Tangente y control de indeterminaciones:** Se reutilizan las funciones anteriores calculando $\tan(x) = \frac{\sin(x)}{\cos(x)}$.
  - **Tolerancia:** Si $|\cos(x)| < 10^{-6}$, se detecta que la función no está definida dentro de dicha tolerancia y se lanza una excepción `ZeroDivisionError` documentando el valor obtenido.

---

### 4.3. Logaritmo Natural (Método de Newton-Raphson)

Para calcular $y = \ln(x)$ para $x > 0$, se resuelve numéricamente la ecuación no lineal:
$$f(y) = e^y - x = 0$$

Aplicando el esquema iterativo de Newton-Raphson con derivada $f'(y) = e^y$:
$$y_{n+1} = y_n - \frac{f(y_n)}{f'(y_n)} = y_n - \frac{e^{y_n} - x}{e^{y_n}} = y_n - 1 + \frac{x}{e^{y_n}}$$

- **Reutilización:** Se utiliza la función propia `exponencial(y)`.
- **Punto de inicio y convergencia:** Iniciando en $y_0 = 0$, para el intervalo sugerido $x \in [0.5, 2.0]$ el método exhibe convergencia cuadrática, requiriendo entre **5 y 6 iteraciones** para alcanzar la tolerancia $|e^{y_n} - x| < 10^{-12}$.
- **Casos de error:** Se rechazan valores de $x \le 0$ mediante `ValueError`. Si se supera el límite de iteraciones (`max_iter=100`) sin satisfacer la tolerancia, se genera `RuntimeError`.

---

### 4.4. Máximo Común Divisor (Algoritmo de Euclides)

Implementación del algoritmo clásico de Euclides basado en divisiones sucesivas con el operador residuo `%`:
$$\text{mcd}(a, b) = \text{mcd}(b, a \pmod b)$$

- **Signo no negativo:** Se toma el valor absoluto de ambos argumentos al inicio: $u = |a|, v = |b|$.
- **Casos de frontera verificados:**
  - $\text{mcd}(48, 18) = 6$
  - $\text{mcd}(-15, 0) = 15$ y $\text{mcd}(0, -15) = 15$
  - $\text{mcd}(0, 0) = 0$ (convención matemática adoptada)
  - $\text{mcd}(-24, -36) = 12$
  - Validación de tipos: se rechazan flotantes y booleanos con `TypeError`.

---

## 5. Aproximación de Onda Cuadrada con Serie de Fourier

La serie de Fourier para una onda cuadrada de amplitud 1 y periodo $2\pi$ está dada por:
$$S_N(x) = \frac{4}{\pi} \sum_{k=0}^{N-1} \frac{\sin((2k+1)x)}{2k+1}$$
donde $N$ representa el número de armónicos impares sumados.

### 5.1. Tabla Comparativa de Resultados

Evaluación para $N = 1, 5, 15$ en los puntos críticos $x = \frac{\pi}{2}$, $x = \frac{3\pi}{2}$ y $x = 0.1$:

| Punto $x$ | $x$ en radianes | Valor Teórico Onda | $N$ (Armónicos) | Suma Parcial $S_N(x)$ | Error Absoluto $|S_N - \text{Teórico}|$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$\pi / 2$** | $1.5708$ | $+1.0$ | **1** | $1.27324$ | $0.27324$ |
| **$\pi / 2$** | $1.5708$ | $+1.0$ | **5** | $1.06305$ | $0.06305$ |
| **$\pi / 2$** | $1.5708$ | $+1.0$ | **15** | $1.02120$ | $0.02120$ |
| **$3\pi / 2$** | $4.7124$ | $-1.0$ | **1** | $-1.27324$ | $0.27324$ |
| **$3\pi / 2$** | $4.7124$ | $-1.0$ | **5** | $-1.06305$ | $0.06305$ |
| **$3\pi / 2$** | $4.7124$ | $-1.0$ | **15** | $-1.02120$ | $0.02120$ |
| **$0.1$** *(cercano a 0)* | $0.1000$ | $+1.0$ | **1** | $0.12711$ | $0.87289$ |
| **$0.1$** *(cercano a 0)* | $0.1000$ | $+1.0$ | **5** | $0.60261$ | $0.39739$ |
| **$0.1$** *(cercano a 0)* | $0.1000$ | $+1.0$ | **15** | $1.17726$ | $0.17726$ |

---

### 5.2. Análisis del Comportamiento al Aumentar $N$

1. **En las mesetas continuas ($x = \pi/2$ y $x = 3\pi/2$):**
   - Con $N = 1$ solo se tiene la componente fundamental seno, con una amplitud inicial de $\frac{4}{\pi} \approx 1.27324$.
   - A medida que $N$ aumenta a $5$ y luego a $15$, los armónicos de orden superior cancelan progresivamente el exceso en la parte superior e inferior, haciendo que la forma de onda sea cada vez más plana en la meseta.
   - El error absoluto en $x = \pi/2$ decrece notoriamente: **$0.27324 \to 0.06305 \to 0.02120$**.

2. **Cerca del punto de discontinuidad ($x = 0.1$ y el Fenómeno de Gibbs):**
   - En $x = 0$, la onda cuadrada teórica presenta un salto discontinuo desde $-1$ hasta $+1$.
   - Para $N = 1$, la función senoidal parte suavemente de cero: $S_1(0.1) \approx 0.12711$.
   - Conforme $N$ crece ($N=5, 15$), la pendiente de transición en torno a $x=0$ se vuelve mucho más vertical (reconstruyendo el flanco de subida de la onda cuadrada).
   - Sin embargo, justo después de la discontinuidad surge un rizado u oscilación con sobreimpulso (*overshoot*): para $N = 15$, $S_{15}(0.1) \approx 1.17726$, sobrepasando el valor teórico $1.0$ en un **$17.7\%$**.
   - Este comportamiento corresponde al **fenómeno de Gibbs**: en cualquier discontinuidad de salto de una función periódica diferenciable a trozos, las sumas parciales de Fourier sobrepasan el salto en aproximadamente un $8.95\%$ respecto a la altura del salto en el límite cuando $N \to \infty$.

---

## 6. Resultados de la Suite de Pruebas

Al ejecutar `python pruebas.py`, se evalúan automáticamente los 26 casos descritos en el enunciado:
- Exponencial: $e^0 = 1$, $e^1 \approx 2.71828$, $e^{-2}$, constante $\pi$ y convergencia de Nilakantha.
- Trigonometría: $\sin(\pi/6) = 0.5$, $\cos(0) = 1$, $\tan(\pi/4) = 1$, prueba de periodicidad con $50\pi + \pi/6$, e intercepción de $\tan(\pi/2)$ con excepción.
- Logaritmo natural: $\ln(1) = 0$, $\ln(2) \approx 0.69315$, $\ln(e) = 1$, barrido completo en $[0.5, 2.0]$ y rechazo de $\ln(0)$ y $\ln(-5)$.
- MCD: $\text{mcd}(48, 18) = 6$, $\text{mcd}(-15, 0) = 15$, $\text{mcd}(0, -15) = 15$, $\text{mcd}(0, 0) = 0$, $\text{mcd}(-24, -36) = 12$, coprimos y validación de tipos.
- Fourier: Monotonía del error en $\pi/2$ y $3\pi/2$, análisis de Gibbs y gráfica ASCII de la señal reconstruida.

**Tasa de éxito obtenida:** `26 / 26 (100.0%)`.

---

## 7. Instrucciones para Publicar en GitHub

Para subir este proyecto a un repositorio propio de GitHub, siga estos pasos desde la consola de comandos en el directorio del proyecto:

1. **Inicializar el repositorio local:**
   ```bash
   git init
   ```

2. **Configurar usuario y correo (si no están configurados globalmente):**
   ```bash
   git config user.name "Su Nombre"
   git config user.email "su_correo@ejemplo.com"
   ```

3. **Agregar todos los archivos y realizar el primer commit:**
   ```bash
   git add .
   git commit -m "Entrega trabajo final: libreria matematica en Python con pruebas y documentacion"
   ```

4. **Crear el repositorio en GitHub:**
   - Ingrese a [GitHub](https://github.com/new).
   - Nombre el repositorio (por ejemplo: `libreria-matematica-python`).
   - Elija visibilidad Pública o Privada según las indicaciones de su docente.
   - **No** marque las casillas de agregar README ni .gitignore (ya los tenemos creados localmente).

5. **Vincular el repositorio remoto y subir el código:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/SU_USUARIO/libreria-matematica-python.git
   git push -u origin main
   ```
