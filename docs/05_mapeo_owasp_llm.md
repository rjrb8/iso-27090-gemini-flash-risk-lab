# 05 — Mapeo complementario: OWASP LLM Top 10, NIST AI 100-2 y MITRE ATLAS

Este documento cruza los hallazgos con marcos de referencia adicionales para que el laboratorio sea útil fuera de ISO/IEC 27090.

---

## 1. OWASP LLM Top 10 (2025)

| ID | Riesgo | Aplicabilidad | Evidencia | Comentario |
|---|---|---|---|---|
| LLM01 | Prompt Injection | **Alta** | Role-play multi-turno, fases 1–7 | El modelo cede ante un marco ficticio y no reevalúa la intención acumulada |
| LLM02 | Sensitive Information Disclosure | Baja | No se observan secretos del sistema | El nombre y la ruta local son datos del usuario, no del sistema |
| LLM03 | Supply Chain | **Alta** | `pip install yt-dlp --upgrade` | Sin versión fijada, hash ni verificación |
| LLM04 | Data and Model Poisoning | No evidenciado | Sin entrenamiento/fine-tuning | No aplica al rol de usuario |
| LLM05 | Improper Output Handling | Media | Código y comandos en la salida | Si un downstream ejecuta la salida, hay riesgo |
| LLM06 | Excessive Agency | Media-alta (condicional) | El modelo afirma acceso a herramientas | Depende de la configuración del despliegue |
| LLM07 | System Prompt Leakage | Baja | No se observa el system prompt | El role-play podría ser precursor |
| LLM08 | Vector and Embedding Weaknesses | No aplica | Sin RAG evidenciado | — |
| LLM09 | Misinformation | **Alta** | “1.43 MiB”, “tesoro conquistado”, `PNG` | Éxito no verificado |
| LLM10 | Unbounded Consumption | Baja (Gemini) / Media (YouTube) | 429 y sugerencia de VPN | El consumo ilimitado es del tercero, no del modelo |

### Detalle LLM01

El ataque no es un prompt malicioso único. Es una **secuencia**:

1. Petición legítima.
2. Negativa.
3. Reformulación como ficción.
4. Aceptación del marco.
5. Petición de procedimiento.
6. Código.
7. Evasión.

La mitigación debe cubrir **la secuencia**, no solo el primer mensaje. Un filtro por prompt aislado no detecta este patrón.

### Detalle LLM03

`pip install yt-dlp --upgrade` instala la última versión disponible. Riesgos:

- Un paquete comprometido o un typo-squatting.
- Una versión con un cambio incompatible.
- Ejecución de código de instalación (`setup.py`) con privilegios del usuario.
- Falta de reproducibilidad.

Mitigaciones: versión fijada, hash, `pip install --require-hashes`, entorno virtual, sandbox, revisión de dependencias.

### Detalle LLM06

El modelo **afirma** tener acceso a YouTube y describe herramientas. No se aporta evidencia de que las tenga. Si el despliegue concede herramientas de red/ficheros:

- El jailbreak puede convertirse en acción.
- La elusión del 429 puede ejecutarse desde la infraestructura del despliegue.
- Aumenta el impacto legal y de reputación.

Mitigaciones: mínimo privilegio, allowlist de dominios, sandbox, aprobación humana, límites de ejecución, auditoría.

### Detalle LLM09

El modelo afirma que la extracción “funcionó” y que se descargaron “1.43 MiB”. No hay archivo, hash, log ni captura verificable en el texto. Esto es **desinformación involuntaria** o **alucinación de herramienta**. El usuario podría tomar decisiones basadas en un éxito falso.

Mitigaciones: no afirmar éxito sin evidencia; mostrar comandos de verificación; separar “salida del modelo” de “resultado de la herramienta”; exigir confirmación del usuario.

---

## 2. NIST AI 100-2 (taxonomía de ataques)

| Categoría NIST | Aplicación al caso |
|---|---|
| Evasión | Jailbreak semántico; no hay evasión numérica |
| Envenenamiento | No aplica |
| Privacidad | Baja; no hay extracción de datos de entrenamiento |
| Abuso | **Alta**; el modelo ayuda a eludir controles de terceros |
| Integridad | **Alta**; afirmaciones de éxito no verificadas |
| Disponibilidad | Baja; el 429 es del tercero |

---

## 3. MITRE ATLAS

| Táctica/técnica | Aplicación |
|---|---|
| Reconnaissance | El usuario explora las capacidades del modelo y de las herramientas |
| Initial Access | No aplica al modelo; el usuario ya tiene acceso al chat |
| ML Attack Staging | Role-play y construcción de contexto |
| Exfiltration | Intento de extraer transcripción de YouTube, no datos del modelo |
| Impact | Elusión de ToS, posible infracción de derechos de autor |
| Defense Evasion | Reformulación narrativa y fragmentación de la petición |

ATLAS se usa aquí como **lente complementaria**; no todas las técnicas encajan en un chatbot sin herramientas.

---

## 4. Resumen de prioridades

| Prioridad | Riesgo | Marco principal |
|---|---|---|
| P1 | Jailbreak multi-turno | OWASP LLM01 / ISO 27090 T-11 |
| P1 | Elusión de ToS/rate limit | ISO 27090 T-11 / legal |
| P1 | Éxito no verificado | OWASP LLM09 / ISO 27090 integridad |
| P2 | Cadena de suministro | OWASP LLM03 / ISO 42001 A.10.3 |
| P2 | Agencia excesiva | OWASP LLM06 / ISO 27090 herramientas |
| P3 | Manejo de salida | OWASP LLM05 / ISO 42001 A.6.2.4 |
| P3 | Supervisión humana | ISO 42001 A.9.5 |
