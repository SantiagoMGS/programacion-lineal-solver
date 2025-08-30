# Aplicación de Programación Lineal - 2 Variables

## Descripción

Esta aplicación en Python permite resolver problemas de programación lineal de 2 variables de forma gráfica e interactiva. Calcula automáticamente los puntos de corte, identifica los vértices de la región factible y determina la solución óptima.

## Características Principales

- ✅ Interfaz gráfica intuitiva con tkinter
- ✅ Entrada de datos flexible para función objetivo y restricciones
- ✅ Soporte para maximización y minimización
- ✅ Diferentes tipos de inecuaciones (≤, ≥, =)
- ✅ Cálculo automático de puntos de corte e intersecciones
- ✅ Identificación de vértices de la región factible
- ✅ Graficación automática de la solución con matplotlib
- ✅ Evaluación de la función objetivo en todos los vértices
- ✅ Determinación del punto y valor óptimo
- ✅ Interpretación detallada de los resultados

## Instalación

### Prerequisitos

- Python 3.8 o superior (se recomienda Python 3.10 o 3.11)

### Instalación de dependencias

**Opción 1 - Usando requirements.txt (recomendado):**

```bash
pip install -r requirements.txt
```

**Opción 2 - Instalación individual (si hay problemas con Python 3.13):**

```bash
pip install matplotlib numpy sympy
```

**Opción 3 - Para Python 3.13 (si persisten los errores):**

```bash
pip install --upgrade pip setuptools
pip install matplotlib numpy sympy
```

**Nota:** tkinter viene incluido por defecto en la mayoría de las instalaciones de Python.

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Interfaz de Usuario

#### Panel Izquierdo - Entrada de Datos

1. **Función Objetivo:**

   - Selecciona el tipo de optimización (maximizar/minimizar)
   - Ingresa los coeficientes de X₁ y X₂

2. **Restricciones:**

   - Ingresa los coeficientes de cada restricción
   - Selecciona el tipo de inecuación (≤, ≥, =)
   - Especifica el término independiente
   - Usa "Agregar Restricción" para más restricciones
   - Usa "Eliminar Última" para quitar restricciones

3. **Resolver:**
   - Haz clic en "RESOLVER PROBLEMA" para obtener la solución

#### Panel Derecho - Resultados

1. **Gráfico:**

   - Visualización de todas las restricciones
   - Región factible sombreada
   - Vértices marcados con coordenadas
   - Punto óptimo destacado con estrella roja
   - Línea de la función objetivo

2. **Resultados Textuales:**
   - Formulación del problema
   - Todos los puntos de corte calculados
   - Vértices de la región factible
   - Evaluación de la función objetivo en cada vértice
   - Solución óptima con interpretación

## Ejemplo: Startup de Software

La aplicación viene preconfigurada con el ejemplo de la startup:

**Problema:**

- **Variables:** A1 (apps de productividad), A2 (apps de entretenimiento)
- **Función Objetivo:** Maximizar Z = 250·A1 + 300·A2
- **Restricciones:**
  - Desarrollo: 20·A1 + 15·A2 ≤ 600 horas
  - Pruebas: 10·A1 + 15·A2 ≤ 450 horas
  - A1 ≥ 0, A2 ≥ 0

**Solución Esperada:**

- Punto óptimo: A1 = 15, A2 = 20
- Ganancia máxima: Z = $9,750 semanales

## Funcionalidades Técnicas

### Algoritmos Implementados

1. **Cálculo de Intersecciones:** Resuelve sistemas de ecuaciones 2x2 para encontrar todos los puntos de corte
2. **Verificación de Factibilidad:** Evalúa cada punto contra todas las restricciones
3. **Método Gráfico:** Implementa el método simplex gráfico para 2 variables
4. **Evaluación Sistemática:** Evalúa la función objetivo en todos los vértices factibles

### Características Avanzadas

- Manejo robusto de errores numéricos
- Conversión automática de restricciones ≥ a formato estándar
- Detección automática de soluciones no factibles
- Redondeo inteligente para evitar errores de precisión
- Graficación adaptativa según los datos

## Estructura de Archivos

```
invproy/
├── main.py           # Aplicación principal
├── requirements.txt  # Dependencias de Python
└── README.md        # Este archivo
```

## Troubleshooting

### Error: "No se encontraron vértices factibles"

- Verifica que las restricciones no sean contradictorias
- Asegúrate de que existe una región factible válida

### Error en datos ingresados

- Verifica que todos los campos numéricos contengan valores válidos
- Los coeficientes pueden ser negativos, pero deben ser números

### Gráfico no se visualiza correctamente

- Intenta ajustar los valores para que estén en un rango razonable
- Verifica que tkinter y matplotlib estén instalados correctamente

## Contribuciones

Este proyecto está diseñado como una herramienta educativa para el aprendizaje de programación lineal. Las mejoras y sugerencias son bienvenidas.
