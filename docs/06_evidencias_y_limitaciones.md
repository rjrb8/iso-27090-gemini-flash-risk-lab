# 06 — Evidencias, cadena de custodia y limitaciones

## 1. Evidencia primaria

| Elemento | Valor |
|---|---|
| Archivo | `Conversacion.txt` |
| Tamaño | 54.512 bytes |
| Líneas | 904 |
| Codificación | UTF-8 |
| Fin de línea | CRLF |
| Origen | `http://192.168.1.106:8080/Conversacion.txt` |
| Fecha de descarga | 24 de octubre de 2026 |
| Hash del original | Ver `data/README.md` (no se incluye el original) |
| Versión incluida | `data/Conversacion.sanitized.txt` |

### Redacciones aplicadas

- Nombre del usuario → `[USUARIO]`.
- URL e ID del vídeo → `[VIDEO_REDACTADO]`.
- Ruta local → `[RUTA_LOCAL]`.
- Bloques de código operativo → `[CODIGO_REDACTADO]`.
- Marcadores de captura → `[CAPTURA_REFERENCIADA]`.

La versión saneada conserva la numeración de líneas para que las referencias del análisis sigan siendo válidas.

---

## 2. Qué se puede afirmar

- El modelo rechazó el role-play en el primer turno (líneas 49–51).
- El modelo aceptó después un marco narrativo y proporcionó guía procedimental.
- El modelo entregó código de extracción y una versión corregida.
- El modelo sugirió VPN/datos móviles ante un 429.
- El modelo afirmó éxito y tamaño de archivo sin evidencia verificable.
- El modelo usó recompensas y lenguaje de validación (“Hechicero Final”).

## 3. Qué no se puede afirmar

- Que el modelo tenga acceso real a YouTube.
- Que la extracción se haya ejecutado.
- Que el archivo `1.43 MiB` exista.
- Que las capturas `PNG` sean auténticas.
- Que Gemini Flash sea inseguro de forma general.
- Que haya habido una infracción de derechos de autor o de ToS; solo hay riesgo.
- Que el modelo haya sido comprometido, envenenado o manipulado.

---

## 4. Cadena de custodia

1. El archivo se obtuvo del servidor indicado por el usuario.
2. Se calculó el hash y se conservó una copia fuera del repositorio.
3. Se generó una versión saneada con `analysis/sanitize_conversation.py`.
4. La versión saneada se revisó manualmente para evitar código operativo.
5. El repositorio no incluye el original ni las capturas.

> Si se necesita evidencia forense, conservar el original con hash, fecha, hora y control de acceso; no confiar solo en la copia saneada.

---

## 5. Limitaciones

### 5.1 De la muestra

- Un solo caso.
- Un solo usuario.
- Una sola versión del modelo (no especificada).
- Sin repetición controlada.
- Sin línea base de comportamiento.

### 5.2 De la evidencia

- No hay archivo final ni capturas.
- No hay logs de herramientas.
- No hay `system prompt`.
- No hay configuración del despliegue.
- No hay confirmación del proveedor.

### 5.3 De la norma

- La referencia local de ISO/IEC 27090 es el borrador 2025.
- La edición oficial es ISO/IEC 27090:2026 (1.ª ed., 56 pp., 2026-10-14).
- ISO/IEC 27090 es una guía; no certifica por sí sola.
- Los identificadores de control de este laboratorio son propios, no cláusulas normativas.

### 5.4 Del análisis

- Las valoraciones de riesgo son cualitativas.
- No se calcula CVSS.
- No se determina responsabilidad legal.
- No se evalúa la seguridad de YouTube ni de Google.

---

## 6. Uso de la evidencia saneada

La versión saneada sirve para:

- Reproducir el análisis de patrones.
- Formar a revisores.
- Compartir el caso sin exponer nombre, URL ni código.
- Comparar con otras conversaciones.

No sirve para:

- Reconstruir el bypass.
- Verificar la autenticidad de las capturas.
- Atribuir responsabilidad legal.

---

## 7. Recomendación de conservación

- Guardar el original en almacenamiento cifrado con acceso restringido.
- Registrar hash y fecha.
- Definir retención (por ejemplo, 12 meses) y borrado seguro.
- No incluir datos personales en repositorios públicos.
- Revisar el contenido antes de cualquier publicación.
