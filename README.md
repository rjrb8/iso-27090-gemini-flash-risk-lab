# ISO/IEC 27090 aplicada a Gemini Flash — laboratorio de análisis de riesgo

**Autor:** Rodolfo Javier Roa Briceño  
**Fecha:** 24 de octubre de 2026  
**Licencia:** MIT para el código y la documentación original; las citas de la conversación pertenecen a sus autores.  
**Normas de referencia:** ISO/IEC 27090:2026, ISO/IEC 42001:2023, ISO/IEC 23894:2023, OWASP LLM Top 10 (2025), NIST AI 100-2, MITRE ATLAS.

---

## 1. Qué es este laboratorio

Laboratorio **defensivo** para analizar, con la taxonomía de ISO/IEC 27090 y el sistema de gestión de ISO/IEC 42001, una conversación real mantenida con **Gemini Flash** (Google) en una interfaz de chat.

El caso de estudio parte de una petición para extraer la transcripción de un vídeo de YouTube. La conversación escala desde una negativa inicial hasta un **juego de rol** que pide eludir restricciones de la plataforma, y termina con código para descargar subtítulos, sugerencias de evasión de límites de tasa y afirmaciones de éxito no verificadas.

El laboratorio **no reproduce el bypass**. Convierte la conversación en:

- Un análisis cronológico de la interacción.
- Un *threat model* con las 16 amenazas de ISO/IEC 27090.
- Un mapa de controles de ISO/IEC 42001.
- Un conjunto de pruebas defensivas y un analizador de patrones de riesgo.
- Una publicación lista para LinkedIn y GitHub.

> **Aviso:** este repositorio es material de análisis y formación. No contiene instrucciones operativas para eludir controles de acceso, límites de tasa o términos de servicio. No es asesoría legal.

<img width="2752" height="1536" alt="Flujo_de_análisis_estático" src="https://github.com/user-attachments/assets/e488eda6-5a59-4a1a-a091-7a55c44389fc" />


---

## 2. Hallazgos principales

| ID | Hallazgo | Evidencia | Riesgo |
|---|---|---|---|
| H-01 | **Jailbreak por role-play multi-turno**: el modelo rechaza el marco inicial, pero acepta progresivamente el juego y termina proporcionando código y consejos de evasión. | Fases 1–6 de la conversación | **Alto** |
| H-02 | **Elusión de controles de terceros**: se sugiere usar VPN o datos móviles para evitar el HTTP 429 de YouTube. | Fase 6 | **Alto** (legal/ToS) |
| H-03 | **Afirmaciones de éxito no fundamentadas**: “1.43 MiB”, “tesoro conquistado”, marcadores `PNG`, sin evidencia verificable del archivo final. | Fases 5–7 | **Medio-alto** |
| H-04 | **Riesgo de cadena de suministro**: `pip install yt-dlp --upgrade` sin versión fijada ni verificación. | Fase 5 | **Alto** si el usuario ejecuta el código |
| H-05 | **Agencia excesiva potencial**: el modelo afirma tener acceso a herramientas y produce automatización de red/ficheros; si se integra como agente, aumenta el impacto. | Fases 3–6 | **Medio-alto** (condicional) |
| H-06 | **Sicofancia y refuerzo del encuadre**: recompensas, “Hechicero Final”, celebración del bypass. | Fases 6–9 | **Medio** |
| H-07 | **Riesgo de cumplimiento**: posible infracción de términos de YouTube y derechos de autor sobre subtítulos. | Todo el caso | **Medio** |

**Conclusión:** no hay evidencia de compromiso del modelo base, extracción de pesos, *poisoning* ni *model tampering*. El riesgo principal es de **integridad del comportamiento y cumplimiento**: los guardrails se erosionan a lo largo de varios turnos y el modelo ayuda a eludir controles de un tercero. Es un fallo de robustez y gobernanza, no una vulnerabilidad de memoria del modelo.

<img width="2752" height="1536" alt="Anatomía_de_Jailbreak_Multi-Turno" src="https://github.com/user-attachments/assets/ec481b09-84ac-45ed-b0d5-2cd76ec0e79c" />


---

## 3. Alcance y supuestos

- **Modelo analizado:** Gemini Flash (Google), en una interfaz de chat. La versión exacta no se especifica en la conversación.
- **Rol analizado:** *deployer/user* de un modelo alojado; no se analiza el entrenamiento ni los pesos del proveedor.
- **Fase del ciclo de vida:** operación/servicio.
- **Evidencia:** un único archivo de conversación (`Conversacion.txt`, 904 líneas, UTF-8 con CRLF, 54.512 bytes) obtenido de `http://192.168.1.106:8080/Conversacion.txt`.
- **Limitación de la norma:** la referencia local de ISO/IEC 27090 se basa en el borrador de 2025. La edición oficial es **ISO/IEC 27090:2026** (edición 1, 56 páginas, publicada el 2026-10-14). Los números de cláusula deben verificarse contra el texto oficial adquirido.
- **Naturaleza de la norma:** ISO/IEC 27090 es una guía informativa, no una norma certificable de forma independiente. Se integra en un SGSI ISO/IEC 27001 o en un AIMS ISO/IEC 42001.

<img width="2752" height="1536" alt="Taxonomía_de_amenazas_en_IA" src="https://github.com/user-attachments/assets/5adcea43-23cb-4360-bfb4-648886b90f2a" />

<img width="2752" height="1536" alt="Controles_ISO_IEC_42001_para_IA" src="https://github.com/user-attachments/assets/7834b950-b8d7-40e2-b780-b0871cd66bf6" />

<img width="2752" height="1536" alt="Análisis_de_seguridad_para_LLMs" src="https://github.com/user-attachments/assets/3244d533-7e78-43df-9a10-496a2b6a08fa" />


---

## 4. Inicio rápido

```bash
git clone <URL-del-repo>
cd iso-27090-gemini-flash-risk-lab

# Analizar la conversación saneada
python3 analysis/risk_patterns.py data/Conversacion.sanitized.txt \
  --json report.json --md report.md

# Ejecutar pruebas
python3 -m unittest discover -s tests -v

# Ver el informe generado
sed -n '1,120p' report.md
```

El analizador solo usa la biblioteca estándar de Python 3.11+. No hace peticiones de red, no instala paquetes y no ejecuta código de la conversación.

---

## 5. Estructura

```
.
├── README.md
├── PUBLICACION.md
├── LICENSE
├── NOTICE.md
├── .editorconfig
├── .gitignore
├── docs/
│   ├── 00_resumen_ejecutivo.md
│   ├── 01_alcance_y_metodo.md
│   ├── 02_analisis_conversacion.md
│   ├── 03_threat_model_iso27090.md
│   ├── 04_controles_iso42001.md
│   ├── 05_mapeo_owasp_llm.md
│   ├── 06_evidencias_y_limitaciones.md
│   ├── 07_plan_de_pruebas.md
│   └── 08_informe_ejemplo.md
├── analysis/
│   ├── risk_patterns.py
│   ├── sanitize_conversation.py
│   └── README.md
├── prompts/
│   ├── benign_control_tests.md
│   └── README.md
├── data/
│   ├── Conversacion.sanitized.txt
│   └── README.md
├── tests/
│   └── test_risk_patterns.py
└── scripts/
    └── package.sh
```

---

## 6. Cobertura de ISO/IEC 27090

Se recorren las **16 amenazas** de la taxonomía de la referencia local:

| Familia | Amenazas | Aplicabilidad en este caso |
|---|---|---|
| Confidencialidad | extracción de modelo, inferencia de pertenencia, inversión de modelo, fuga de datos de entrenamiento, prompt injection de fuga, extracción de system prompt | Baja o no evidenciada |
| Integridad | envenenamiento de datos, evasión adversarial, backdoor/troyano, manipulación del modelo, **prompt injection (jailbreak)**, **prompt injection indirecta** | **Jailbreak: alta**; indirecta: baja/no evidenciada |
| Disponibilidad | sponge, agotamiento de recursos, DoS por inferencia, indisponibilidad del modelo | Baja o no evidenciada |
| Transversal | cadena de suministro, agencia excesiva, manejo de salida, desinformación, supervisión humana | **Media-alta** en cadena de suministro, agencia y desinformación |

El detalle, la probabilidad, el impacto, el riesgo y los controles están en [`docs/03_threat_model_iso27090.md`](docs/03_threat_model_iso27090.md).

---

## 7. Cobertura de ISO/IEC 42001

El análisis se mapea a las familias de controles del Anexo A:

| Familia | Relevancia en este caso |
|---|---|
| A.2 Políticas de IA | Política de uso aceptable y límites de role-play |
| A.3 Organización interna | Roles, responsabilidades y canal de reporte de abusos |
| A.5 Impactos | Evaluación de impacto individual y societal (desinformación, derechos de autor) |
| A.6 Ciclo de vida | Verificación/validación adversarial, monitorización, logs |
| A.8 Información a terceros | Documentación de capacidades y limitaciones |
| A.9 Uso responsable | Procesos de uso, supervisión humana, uso previsto |
| A.10 Terceros | Diligencia sobre el proveedor del modelo y sobre paquetes de terceros |

El detalle está en [`docs/04_controles_iso42001.md`](docs/04_controles_iso42001.md).

---

## 8. Mapeo a OWASP LLM Top 10

| OWASP | Título | Relevancia |
|---|---|---|
| LLM01 | Prompt Injection | **Alta**: jailbreak por role-play |
| LLM02 | Sensitive Information Disclosure | Baja: no se observan secretos del sistema |
| LLM03 | Supply Chain | **Alta**: `pip install` sin pinning |
| LLM04 | Data and Model Poisoning | No evidenciado |
| LLM05 | Improper Output Handling | Media: código y comandos en la salida |
| LLM06 | Excessive Agency | Media-alta si el modelo tiene herramientas |
| LLM07 | System Prompt Leakage | Baja: no se observa el prompt del sistema |
| LLM08 | Vector and Embedding Weaknesses | No aplica (sin RAG evidenciado) |
| LLM09 | Misinformation | **Alta**: éxito no verificado |
| LLM10 | Unbounded Consumption | Baja para Gemini; media para el tercero (429) |

El detalle está en [`docs/05_mapeo_owasp_llm.md`](docs/05_mapeo_owasp_llm.md).

---

## 9. Uso responsable

Este laboratorio sirve para:

- Formar equipos en *AI security*, *threat modeling* y gobernanza de IA.
- Probar guardrails con prompts defensivos.
- Documentar hallazgos y controles para ISO/IEC 42001.
- Preparar evidencia para auditorías y revisiones de riesgo.

No sirve para:

- Reproducir el bypass de YouTube.
- Eludir límites de tasa, controles de acceso o términos de servicio.
- Extraer contenido de terceros sin autorización.
- Atacar sistemas reales.

---

## 10. Publicación

El archivo [`PUBLICACION.md`](PUBLICACION.md) contiene:

- Título, descripción y topics para GitHub.
- Dos versiones del post de LinkedIn.
- Comandos para subir el repositorio con `gh` o Git manual.
- Checklist de UTF-8, privacidad y seguridad.

---

## 11. Limitaciones

- Una sola conversación no permite concluir sobre la robustez global de Gemini Flash.
- No se dispone del archivo `.md` final ni de las capturas originales; las afirmaciones de éxito del modelo no son verificables.
- No se dispone del *system prompt* ni de la configuración de herramientas del despliegue.
- La referencia de ISO/IEC 27090 es la del borrador 2025; la edición oficial 2026 debe consultarse para citas normativas.
- Las valoraciones de riesgo son cualitativas y dependen del contexto de despliegue.

---

## 12. Licencia y atribución

Código y documentación original: MIT (ver [`LICENSE`](LICENSE)).  
Citas de la conversación: se incluyen de forma saneada y parcial con fines de análisis de seguridad; los derechos pertenecen a sus autores.  
ISO/IEC 27090:2026 y ISO/IEC 42001:2023 son normas de ISO/IEC; este repositorio no reproduce su texto.
