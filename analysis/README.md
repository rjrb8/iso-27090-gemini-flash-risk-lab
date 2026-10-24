# Análisis

## `sanitize_conversation.py`

Genera una copia saneada de la conversación:

```bash
python3 analysis/sanitize_conversation.py /ruta/Conversacion.txt data/Conversacion.sanitized.txt
```

Redacta:

- Nombre del usuario.
- URL e ID del vídeo.
- Ruta local.
- Líneas de código operativo.
- Marcadores `PNG`.

Conserva el número de líneas para que las referencias sigan siendo válidas. No ejecuta el contenido.

## `risk_patterns.py`

Analiza patrones de riesgo:

```bash
python3 analysis/risk_patterns.py data/Conversacion.sanitized.txt \
  --json report.json --md report.md
```

Opciones:

- `--json`: informe estructurado.
- `--md`: informe legible.
- `--fail-on-high`: devuelve 2 si hay hallazgos de severidad alta (útil en CI).

El analizador no imprime el texto coincidente. Solo muestra el patrón, la línea y el recuento.

## Limitaciones

- Es un triaje, no una prueba de explotación.
- Los patrones pueden producir falsos positivos.
- No evalúa el modelo en vivo.
- No sustituye la revisión humana ni el análisis legal.
- La conversación saneada redacta las líneas de código; por diseño, algunos patrones de cadena de suministro (por ejemplo, `pip install` sin pinning) se documentan manualmente en `docs/03_threat_model_iso27090.md` y no siempre aparecen en el informe automático.
