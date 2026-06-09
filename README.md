# Respuestas teóricas — BookShare Hub

## Pregunta A: Ciclo TDD (Red–Green–Refactor)

TDD significa escribir primero la prueba y luego el código. El ciclo tiene 3 pasos:

**Red (Rojo):** Escribes una prueba para una función que aún no existe. La corres y falla porque el código no está hecho todavía. Ejemplo: escribes `test_crear_usuario()` antes de tener el endpoint `/api/usuarios/`.

**Green (Verde):** Escribes el mínimo código necesario para que la prueba pase. No importa si es perfecto, solo que funcione. Ejemplo: creas el endpoint `/api/usuarios/` con lo básico.

**Refactor:** Mejoras el código sin cambiar su comportamiento. Las pruebas siguen pasando pero el código queda más limpio y organizado. Ejemplo: mueves la lógica del endpoint a `services.py`.

Este ciclo se repite por cada nueva funcionalidad que agregas a la API.

---

## Pregunta B: Importancia del entorno virtual

Si trabajas sin entorno virtual, instalas todas las librerías directamente en Python del sistema. Esto causa varios problemas:

1. **Conflictos de versiones:** Si un proyecto necesita FastAPI 0.95 y otro necesita FastAPI 0.110, no pueden coexistir en el sistema. Con entorno virtual cada proyecto tiene sus propias versiones.

2. **Contaminación del sistema:** Las librerías de un proyecto afectan a todos los demás proyectos y al sistema operativo.

3. **Reproducibilidad en equipo:** Sin entorno virtual, cada desarrollador puede tener versiones diferentes y el proyecto funciona en una máquina pero no en otra. Con `requirements.txt` y entorno virtual todos instalan exactamente lo mismo.

Para BookShare Hub el entorno virtual garantiza que SQLModel, FastAPI y Pydantic tengan las versiones correctas sin afectar otros proyectos del equipo.

---

## Pregunta C: Validaciones en modelos vs endpoints

**Centralizadas en modelos Pydantic/SQLModel (mejor opción):**

Cuando defines `rating: int = Field(..., ge=1, le=5)` en el modelo, esa regla se aplica automáticamente en todo el sistema, en el POST, en el PUT, en los tests, en todas partes. Si mañana quieres cambiar el rango a 1-10, lo cambias en un solo lugar.

**Distribuidas en endpoints o servicios:**

Si validas el rating dentro de cada endpoint por separado, puedes olvidarte de validarlo en alguno. Eso genera inconsistencias: el POST valida pero el PUT no, y alguien puede guardar un rating de 10 por el PUT sin que nadie lo detecte.

**Conclusión:** centralizar en los modelos garantiza coherencia, evita repetir código y reduce la probabilidad de errores. Es la práctica recomendada en aplicaciones FastAPI con SQLModel.
