# Herramienta de análisis de riesgos TI basada en MAGERIT v3

**Trabajo de Fin de Grado — Grado en Ingeniería Informática**  
Universidad Internacional de La Rioja (UNIR)  
Autor: Diego Díaz Sánchez  
Director: Juan Manuel González Calleros  

---

## Descripción

Aplicación web desarrollada en Python/Flask que implementa el proceso 
de análisis y gestión de riesgos en sistemas de información siguiendo 
la metodología MAGERIT v3 del Centro Criptológico Nacional.

La herramienta permite a los responsables TI de una organización:
- Registrar y valorar activos de información (dimensiones ACIDT)
- Asociar amenazas del catálogo MAGERIT a cada activo
- Calcular automáticamente el riesgo inherente y residual
- Gestionar salvaguardas y medir su eficacia
- Visualizar el estado del análisis en un dashboard

Desarrollada como componente práctico del TFG:  
*"Diseño y validación de un plan de contingencia TI para entornos 
productivos basado en MAGERIT v3"*

---

## Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Backend | Python 3.8+, Flask 2.x |
| ORM | Flask-SQLAlchemy |
| Base de datos | SQLite |
| Frontend | HTML5, CSS3, Jinja2 |
| Autenticación | Flask-Login |

---

## Estructura del proyecto
