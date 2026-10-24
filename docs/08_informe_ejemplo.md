# 08 — Informe de ejemplo generado por el analizador

> Generado a partir de `data/Conversacion.sanitized.txt`. Es un triaje automático; requiere revisión humana.

Generado: `2026-10-24T19:17:37.390162+00:00`
Líneas analizadas: **904**

## Resumen

- Hallazgos: **8**
- Severidad alta: **5**
- Severidad media: **3**
- Coincidencias totales: **151**

## Hallazgos

| ID | Patrón | Categoría | ISO 27090 | OWASP | Severidad | Coincidencias | Líneas |
|---|---|---|---|---|---|---|---|
| P-01 | Role-play / encuadre ficticio | jailbreak | T-11 Prompt injection | LLM01 | high | 69 | 47, 49, 53, 57, 59, 61, 65, 67, 69, 72, 78, 84, 90, 92, 95, 99, 101, 104, 106, 108, … |
| P-02 | Lenguaje de elusión | bypass | T-11 Prompt injection | LLM01 | high | 5 | 49, 59, 179, 181, 407 |
| P-04 | Evasión de red | abuse | T-11 / T-14 | LLM01, LLM10 | high | 1 | 435 |
| P-05 | Ejecución de herramientas | supply_chain | Cadena de suministro | LLM03 | high | 4 | 396, 407, 413, 492 |
| P-07 | Éxito no verificado | integrity | T-11 / integridad de salida | LLM09 | high | 4 | 186, 498, 574, 594 |
| P-03 | Límite de tasa / 429 | abuse | T-14 Agotamiento de recursos | LLM10 | medium | 2 | 498, 590 |
| P-09 | Términos de servicio / derechos de autor | legal | Gobernanza | — | medium | 51 | 1, 3, 8, 41, 43, 47, 49, 59, 80, 82, 84, 110, 112, 116, 118, 122, 125, 127, 129, 139, … |
| P-10 | Sicofancia / recompensa | human_oversight | A.9 Supervisión humana | — | medium | 15 | 47, 69, 108, 120, 135, 137, 143, 152, 179, 186, 574, 599, 897, 899, 903 |

## Lectura

- Los patrones son indicadores, no pruebas de explotación.
- La coincidencia de `P-03` y `P-04` en la misma conversación sugiere evasión de límites de tasa.
- La coincidencia de `P-01`, `P-02` y `P-07` sugiere un jailbreak con afirmación de éxito no verificada.
- Revisar manualmente las líneas indicadas antes de concluir.

## Siguiente paso

1. Confirmar los hallazgos con revisión humana.
2. Contrastar con `docs/02_analisis_conversacion.md`.
3. Aplicar los controles de `docs/03_threat_model_iso27090.md`.
