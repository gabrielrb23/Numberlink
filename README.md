# 🧩 Numberlink Solver & Manual Player

Este proyecto implementa un **juego Numberlink** que puede jugarse en
modo manual o resolverse automáticamente mediante un algoritmo de
backtracking con heurísticas.

Permite cargar tableros desde archivos de texto y ejecutar el programa
pasando argumentos por línea de comandos.

------------------------------------------------------------------------

## 🚀 Ejecución

El proyecto requiere **Python 3.8 o superior**.

### **Ejecutar el programa**

El programa recibe **dos argumentos**:

1.  **Archivo del tablero**
2.  **Modo de ejecución**
    -   `resolver` → intenta resolver el Numberlink automáticamente
    -   `jugar` → modo interactivo donde tú conectas los símbolos

#### 👉 Ejecutar en modo *resolver*

``` bash
python main.py test-files\numberlink_00.txt resolver
```

#### 👉 Ejecutar en modo *jugar*

``` bash
python main.py test-files\numberlink_00.txt jugar
```

------------------------------------------------------------------------

## 📁 Estructura del tablero

Cada archivo de tablero tiene el siguiente formato:
-   Cada **símbolo no vacío debe aparecer exactamente dos veces** (los
    puntos a conectar).
-   Los espacios representan celdas vacías.

Ejemplo de archivo válido:

    5 5
    A   A
      B  
      B  
      C  
    C    

------------------------------------------------------------------------

## 🎮 Modos de juego

### 🧠 **Modo automático (`resolver`)**

El algoritmo: - Usa heurísticas de distancia Manhattan. - Explora
caminos mediante DFS con ordenamiento tipo A\*. - Valida que los pares
restantes sigan siendo alcanzables. - Comprueba el full-cover si está
activado.

### ✋ **Modo manual (`jugar`)**

-   Escribes el nombre del símbolo que quieres conectar.
-   El programa te pedirá paso a paso coordenadas: ejemplo → `2,3`
-   Solo puedes moverte en 4 direcciones.
-   Puedes cancelar con `x`.

------------------------------------------------------------------------

## 📦 Estructura del proyecto

    .
    ├── board.py         # Lógica del tablero, solver y modo manual
    ├── main.py          # Punto de entrada
    ├── numberlink_00.txt (ejemplo)
    └── README.md

------------------------------------------------------------------------

## 🛠 Requisitos

-   Python 3.8+
-   No requiere librerías externas

------------------------------------------------------------------------