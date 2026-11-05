# Cadenas de Markov: Simulación de estados climáticos

Proyecto académico desarrollado para el curso de **Matemática Discreta** de la Universidad Peruana de Ciencias Aplicadas (UPC), sección 3638, durante el ciclo 2025-01.

## Descripción del proyecto

Este proyecto implementa una simulación de cadenas de Markov para representar la evolución de diferentes condiciones climáticas a lo largo de un periodo de 20 a 40 días.

Se consideran cuatro estados climáticos:

- **NU:** Nublado.
- **P:** Parcialmente nublado.
- **PS:** Parcialmente soleado.
- **SO:** Soleado.

A partir de la secuencia de estados generada, el programa identifica y contabiliza las transiciones entre las condiciones climáticas. Posteriormente, utiliza estos datos para construir una **matriz de transición estocástica**, que permite analizar las probabilidades de cambio entre los distintos estados.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `Cadenas_Markov.py` | Aplicación desarrollada en Python con interfaz gráfica mediante Tkinter, que permite ejecutar y visualizar la simulación. |
| `INFORME-DEL-PROYECTO_MATE_DISCRETA.pdf` | Documento académico que contiene el desarrollo y el informe del proyecto correspondiente a la semana 3. |

## Tecnologías utilizadas

- **Python 3:** Lenguaje de programación utilizado para desarrollar la simulación.
- **Tkinter:** Biblioteca utilizada para implementar la interfaz gráfica.

## Requisitos

- Tener instalado Python 3.
- Contar con Tkinter, incluido generalmente en las instalaciones estándar de Python.

## Cómo ejecutar el proyecto

1. Clona o descarga este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta el siguiente comando:

```bash
python Cadenas_Markov.py
```

La aplicación abrirá una interfaz gráfica desde la cual podrás ejecutar y visualizar la simulación de los estados climáticos.

## Propósito académico

El proyecto tiene como finalidad aplicar los conceptos de cadenas de Markov y matrices estocásticas mediante un caso práctico de simulación, reforzando la comprensión de las transiciones entre estados y el análisis de probabilidades.
