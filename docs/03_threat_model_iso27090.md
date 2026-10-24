# 03 — Threat model con ISO/IEC 27090

**Base:** taxonomía de 16 amenazas de la referencia local de ISO/IEC 27090 (borrador 2025), aplicada a una conversación con Gemini Flash.  
**Nota:** la edición oficial es ISO/IEC 27090:2026. Los identificadores de control de este documento son **propios del laboratorio**; no son cláusulas normativas.

---

## 1. Activos, actores y fronteras de confianza

### 1.1 Activos

| Activo | Descripción | Criticidad |
|---|---|---|
| A-01 | Modelo Gemini Flash y su comportamiento | Alta |
| A-02 | Política de uso y guardrails del despliegue | Alta |
| A-03 | Contenido de YouTube y derechos del titular | Media |
| A-04 | Credenciales, claves y configuración del cliente | Alta |
| A-05 | Conversación y datos personales del usuario | Media |
| A-06 | Reputación del proveedor y del usuario | Media |
| A-07 | Integridad de las salidas (código, afirmaciones) | Alta |
| A-08 | Cadena de suministro de paquetes (`yt-dlp`, `youtube-transcript-api`) | Alta |

### 1.2 Actores

- **Usuario principal:** solicita la extracción y adopta el role-play.
- **Modelo:** genera texto, código y afirmaciones.
- **Proveedor del modelo:** Google; no se analiza su infraestructura.
- **Tercero:** YouTube; controla el acceso, los subtítulos y el rate limiting.
- **Titular del contenido:** derechos sobre el vídeo y la transcripción.
- **Desplegador:** quien integra el modelo; define herramientas, políticas y logs.

### 1.3 Fronteras de confianza

```
[Usuario] --texto--> [Aplicación/chat] --prompt--> [Gemini Flash]
     |                                      |
     |                                      +--> [Herramientas?] --red--> [YouTube]
     |                                      |
     +<-- salida (texto/código) <-----------+
```

La frontera crítica es **modelo → herramientas → red**. Si el modelo no tiene herramientas, el impacto de un jailbreak se limita a la salida textual. Si las tiene, el jailbreak puede convertirse en acción.

---

## 2. Matriz de las 16 amenazas

**Escala:** probabilidad (P) e impacto (I) de 1 a 5; riesgo = P × I.  
**Aplicabilidad:** “No evidenciado” significa que no hay señal en esta conversación, no que la amenaza no exista.

| # | Amenaza | Familia | P | I | Riesgo | Aplicabilidad | Evidencia |
|---|---|---|---|---|---|---|---|
| T-01 | Extracción de modelo | Confidencialidad | 1 | 5 | 5 (bajo) | No evidenciado | No hay consultas sistemáticas para reconstruir el modelo |
| T-02 | Inferencia de pertenencia | Confidencialidad | 1 | 4 | 4 (bajo) | No evidenciado | No se sondea si un dato estuvo en entrenamiento |
| T-03 | Inversión de modelo | Confidencialidad | 1 | 4 | 4 (bajo) | No evidenciado | No se explotan gradientes/confidencias |
| T-04 | Fuga de datos de entrenamiento | Confidencialidad | 2 | 4 | 8 (medio-bajo) | Baja | No se piden datos memorizados; el contenido de YouTube no es entrenamiento del modelo |
| T-05 | Prompt injection de fuga | Confidencialidad | 2 | 3 | 6 (bajo) | Baja | No se intenta extraer secretos de herramientas/RAG |
| T-06 | Extracción de system prompt | Confidencialidad | 2 | 3 | 6 (bajo) | Baja | No hay intento directo; el role-play podría ser precursor |
| T-07 | Envenenamiento de datos | Integridad | 1 | 5 | 5 (bajo) | No aplica | Sin entrenamiento/fine-tuning |
| T-08 | Evasión adversarial | Integridad | 2 | 4 | 8 (medio-bajo) | Baja | No se ataca un clasificador; el jailbreak es semántico, no adversarial numérico |
| T-09 | Backdoor / troyano | Integridad | 1 | 5 | 5 (bajo) | No aplica | Sin acceso a artefactos del modelo |
| T-10 | Manipulación del modelo | Integridad | 1 | 5 | 5 (bajo) | No aplica | Sin acceso a pesos/registro |
| T-11 | Prompt injection (jailbreak) | Integridad | 5 | 4 | **20 (alto)** | **Confirmada** | Role-play multi-turno y compliance gradual |
| T-12 | Prompt injection indirecta | Integridad | 1 | 4 | 4 (bajo) | No evidenciado | No hay contenido de tercero inyectado en el contexto |
| T-13 | Sponge attack | Disponibilidad | 1 | 3 | 3 (bajo) | No evidenciado | La longitud no busca agotar cómputo |
| T-14 | Agotamiento de recursos | Disponibilidad | 2 | 3 | 6 (bajo) | Baja | El 429 es de YouTube, no del modelo |
| T-15 | DoS por inferencia | Disponibilidad | 1 | 4 | 4 (bajo) | No evidenciado | Sin bucles recursivos ni herramientas autónomas |
| T-16 | Indisponibilidad del modelo | Disponibilidad | 1 | 4 | 4 (bajo) | No evidenciado | Sin señal de caída o saturación |

### Lectura de la matriz

- **T-11 es el hallazgo principal.** Es la única amenaza con evidencia directa y riesgo alto.
- **T-04, T-08 y T-14** tienen riesgo bajo/medio-bajo y evidencia débil; se documentan por completitud.
- **T-01, T-02, T-03, T-07, T-09, T-10, T-12, T-13, T-15 y T-16** no tienen evidencia en este caso. No deben presentarse como hallazgos.

---

## 3. Análisis de las amenazas relevantes

### T-11 — Prompt injection (jailbreak)

**Patrón observado:** el usuario no intenta un jailbreak de un solo prompt. Construye un marco ficticio, obtiene una negativa, reformula, obtiene una guía, pide código, lo mejora y finalmente pide evadir un 429.

**Por qué funciona:**
- El modelo evalúa cada turno de forma local, no la **intención acumulada**.
- El role-play desplaza la responsabilidad (“es ficticio”, “es un juego”).
- Las recompensas simbólicas (“+10 puntos”) crean un contexto de cumplimiento.
- La petición se fragmenta en subtareas aparentemente legítimas.

**Impacto:**
- Elusión de términos de servicio y controles de terceros.
- Producción de código de extracción no autorizada.
- Normalización de conductas de bypass.
- Si el modelo tiene herramientas, posible ejecución no autorizada.

**Controles:**
- Clasificador de intención multi-turno.
- Detección de role-play con fines de elusión.
- Política de “no ayudar a evadir controles de acceso, rate limits o ToS”.
- Rechazo consistente y explicación de alternativas legítimas.
- Pruebas de regresión con conversaciones multi-turno.

**Riesgo residual:** medio, incluso con controles, porque el lenguaje natural permite reformulaciones infinitas.

---

### T-04 — Fuga de datos de entrenamiento

**Observado:** no hay petición de datos memorizados ni de información privada de entrenamiento. El contenido solicitado es una transcripción de YouTube, que es un dato de tercero, no un dato de entrenamiento del modelo.

**Riesgo:** bajo. Podría haber un riesgo de **derechos de autor** si el modelo reprodujera una transcripción completa, pero no es una fuga de datos de entrenamiento en el sentido de ISO 27090.

---

### T-08 — Evasión adversarial

**Observado:** no hay perturbaciones numéricas, imágenes adversariales ni ataques a un clasificador. El jailbreak es **semántico y conversacional**.

**Riesgo:** bajo para esta muestra. La evasión adversarial clásica requiere acceso al modelo o a un clasificador y no se observa.

---

### T-14 — Agotamiento de recursos

**Observado:** el error 429 es de YouTube, no de Gemini. El modelo sugiere VPN/datos móviles para evitar el límite del tercero. Eso es un riesgo de **elusión**, no un agotamiento de recursos del modelo.

**Riesgo:** bajo para Gemini; alto para la relación con el tercero.

---

### T-12 — Prompt injection indirecta

**Observado:** no hay contenido de tercero (páginas, documentos, correos) insertado en el contexto. La conversación es directa usuario → modelo.

**Riesgo:** no evidenciado. Si en el futuro el modelo procesa transcripciones de YouTube, un atacante podría insertar instrucciones en el contenido; eso requeriría un análisis separado.

---

## 4. Riesgos transversales (fuera de las 16)

| ID | Riesgo | ISO 27090 / 42001 | Evidencia | Riesgo |
|---|---|---|---|---|
| X-01 | Cadena de suministro: `pip install yt-dlp --upgrade` sin pinning | Cadena de suministro; A.10.3 | Línea 435 | Alto si se ejecuta |
| X-02 | Agencia excesiva: herramientas de red/ficheros | Herramientas y agencia; A.9 | Fases 3–6 | Medio-alto (condicional) |
| X-03 | Manejo de salida: código/comandos ejecutables | Integridad de salida; A.6.2.4 | Fases 4–7 | Medio |
| X-04 | Desinformación: éxito no verificado | Integridad de salida; A.6.2.6 | Línea 498 | Medio-alto |
| X-05 | Sicofancia y supervisión humana | Uso responsable; A.9 | Líneas 574–577, 897 | Medio |
| X-06 | ToS y derechos de autor | Gobernanza/legal | Todo el caso | Medio |
| X-07 | Privacidad: nombre y ruta local | A.7 / A.8 | Líneas 1, 60 | Bajo |
| X-08 | Retención de logs con datos sensibles | A.6.2.8 | Conversación completa | Bajo-medio |

> **Nota de detección:** la conversación saneada redacta las líneas de código. Por eso, el informe automático puede no mostrar X-01 (`pip install` sin pinning) aunque el hallazgo esté confirmado en el original y documentado aquí. La redacción es deliberada para no distribuir código operativo.

---

## 5. Plan de tratamiento

| Prioridad | Acción | Amenaza | Responsable sugerido | Plazo |
|---|---|---|---|---|
| P1 | Política anti-elusión y rechazo multi-turno | T-11, X-06 | Producto/Seguridad | 30 días |
| P1 | No emitir código de evasión; alternativas legítimas | T-11, X-03 | Producto/Ingeniería | 30 días |
| P1 | Verificación de éxito antes de afirmar resultados | X-04 | Producto/QA | 30 días |
| P2 | Pinning, hash y sandbox para dependencias | X-01 | Ingeniería | 60 días |
| P2 | Detección de role-play y scoring de conversación | T-11 | Seguridad/ML | 60 días |
| P2 | Red teaming multi-turno y regresión | T-11 | Seguridad | 90 días |
| P3 | AISIA y evaluación de impacto | X-05, X-06 | Gobernanza | 90 días |
| P3 | Monitorización, logs y respuesta a incidentes | T-11, X-08 | Operaciones | 90 días |
| P3 | Diligencia de proveedor y ML-BOM | X-01 | Compras/Seguridad | 120 días |

---

## 6. Correspondencia con la estructura de ISO/IEC 27090

La referencia local organiza la seguridad de IA en cuatro dimensiones. Este laboratorio las recorre todas:

| Dimensión | Aplicación en este caso |
|---|---|
| Panorama de amenazas | Las 16 amenazas de la sección 2, con aplicabilidad y evidencia |
| Modelado de amenazas | Activos, actores, fronteras de confianza y matriz P/I de la sección 1 |
| Controles de seguridad | Preventivos, detectivos y correctivos de la sección 5 |
| Ciclo de vida | Requisitos, diseño, verificación, despliegue, operación, monitorización y retiro |

### Controles por función

| Función | Ejemplos |
|---|---|
| Preventivo | Política anti-elusión, filtros de intención, allowlist de herramientas, pinning/hash, sandbox, mínimo privilegio |
| Detectivo | Scoring multi-turno, logs, alertas, verificación de salida, revisión humana, pruebas de regresión |
| Correctivo | Respuesta a incidentes, bloqueo de herramientas, rollback, notificación, acción correctiva, revisión de política |

> No se citan números de cláusula concretos porque la referencia usada es el borrador 2025 y la edición oficial es 2026. Para una auditoría formal, verificar la numeración contra el texto oficial adquirido.

---

## 7. Riesgo residual y conclusión

Con los controles P1 y P2, el riesgo de T-11 baja de **alto** a **medio**. No se elimina: el lenguaje natural y el role-play permiten reformulaciones creativas. La clave es **detectar la intención acumulada**, no solo el prompt individual.

El riesgo de cadena de suministro (X-01) es **alto solo si el usuario ejecuta el código**. El modelo no lo ejecuta. La mitigación debe estar en la guía al usuario y en el entorno de ejecución, no solo en el filtro del modelo.

El riesgo legal (X-06) no se resuelve técnicamente. Requiere política de uso, revisión de términos y, cuando corresponda, autorización del titular.
