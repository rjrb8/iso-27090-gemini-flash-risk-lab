# 01 — Alcance, método y supuestos

## 1. Objetivo

Evaluar, con ISO/IEC 27090:2026 e ISO/IEC 42001:2023, si la conversación analizada contiene **elementos de riesgo de seguridad** para un despliegue de **Gemini Flash** y determinar qué controles deberían existir para prevenirlos, detectarlos y responder a ellos.

El objetivo no es demostrar que Gemini Flash sea inseguro, sino identificar **qué comportamiento observable** activa qué amenaza de la taxonomía y qué evidencia falta para concluir.

---

## 2. Sistema en alcance

| Elemento | Descripción |
|---|---|
| Modelo | Gemini Flash (Google), versión no especificada |
| Canal | Interfaz de chat / API conversacional |
| Rol analizado | *Deployer* y *user* de un modelo alojado |
| Fase del ciclo de vida | Operación / servicio |
| Entradas | Texto del usuario, URL de YouTube, instrucciones de role-play |
| Salidas | Texto, código Python, comandos, afirmaciones de éxito |
| Herramientas | Inciertas; el modelo afirma acceso a YouTube, pero no se aporta evidencia |
| Datos | Conversación, nombre de usuario, ruta local, URL/ID de vídeo |
| Infraestructura | Proveedor (Google) + cliente; no se analiza la infraestructura interna |

**Fuera de alcance:** entrenamiento, fine-tuning, pesos, registro de modelos, infraestructura de Google, seguridad de YouTube, cumplimiento legal definitivo, otros usuarios o conversaciones.

---

## 3. Evidencia

- **Archivo:** `Conversacion.txt`.
- **Tamaño:** 54.512 bytes, 904 líneas.
- **Codificación:** UTF-8, con terminadores CRLF.
- **Origen:** `http://192.168.1.106:8080/Conversacion.txt`.
- **Integridad:** se calculó el hash del archivo descargado; el laboratorio incluye una versión saneada, no el original.
- **Redacciones:** nombre del usuario, URL/ID del vídeo, ruta local y bloques de código operativo.
- **Evidencia no disponible:** archivo `.md` final, capturas `PNG`, `system prompt`, configuración de herramientas, versión exacta del modelo, logs del proveedor.

> La ausencia de evidencia no equivale a evidencia de ausencia. Las conclusiones se limitan a lo observable.

---

## 4. Método

### 4.1 Fases

1. **Lectura integral** de la conversación y segmentación en fases.
2. **Extracción de patrones** de riesgo (role-play, evasión, ejecución, éxito no verificado, datos sensibles).
3. **Threat modeling** con las 16 amenazas de ISO/IEC 27090, organizadas por CIA y ciclo de vida.
4. **Evaluación de aplicabilidad** de cada amenaza: evidencia, probabilidad, impacto, riesgo.
5. **Selección de controles** de las familias de ISO/IEC 27090 y del Anexo A de ISO/IEC 42001.
6. **Mapeo complementario** a OWASP LLM Top 10, NIST AI 100-2 y MITRE ATLAS.
7. **Declaración de riesgo residual** y plan de tratamiento.
8. **Diseño de pruebas defensivas** y analizador reproducible.

### 4.2 Escala de riesgo

| Nivel | Criterio |
|---|---|
| **Crítico** | Compromiso del modelo o del proveedor, ejecución arbitraria, fuga masiva de datos |
| **Alto** | Elusión de controles, cadena de suministro, daño legal/reputacional relevante |
| **Medio** | Desinformación, supervisión insuficiente, impacto limitado y corregible |
| **Bajo** | Impacto menor, evidencia débil o control existente |
| **No evidenciado** | No hay señal en la conversación; no se puede evaluar |

La escala es **cualitativa**. No se calcula CVSS porque el caso no es una vulnerabilidad de software con vector explotable medible.

### 4.3 Criterios de imparcialidad

- Separar **observación** (lo que dice el archivo) de **inferencia** (lo que podría ocurrir en un despliegue).
- No atribuir al modelo base fallos que pertenecen al despliegue, al usuario o a un tercero.
- No confundir una **recomendación de código** con una **ejecución real**.
- No confundir una **afirmación del modelo** con **evidencia verificada**.
- Declarar la limitación de la edición de ISO/IEC 27090 usada.

---

## 5. Supuestos

1. El modelo es Gemini Flash en una interfaz de chat; la versión exacta no se especifica.
2. El modelo **no tiene** acceso real a YouTube en este despliegue, o no lo demuestra. Las afirmaciones de acceso son no verificadas.
3. El usuario es el principal de la conversación y actúa por iniciativa propia.
4. No hay un tercero malicioso inyectando contenido en el contexto (no hay evidencia de prompt injection indirecta).
5. El código proporcionado no fue ejecutado por el modelo; el usuario decide si lo ejecuta.
6. La conversación es un **único caso** y no una campaña de red teaming representativa.

---

## 6. Limitaciones

- **Norma:** la referencia local de ISO/IEC 27090 está basada en el borrador 2025. La edición oficial es ISO/IEC 27090:2026 (edición 1, 56 páginas, 2026-10-14). Los números de cláusula y anexos deben verificarse contra el texto oficial.
- **Naturaleza:** ISO/IEC 27090 es una guía informativa; no certifica por sí sola. ISO/IEC 42001 es el sistema de gestión certificable.
- **Muestra:** una conversación no permite medir la tasa de jailbreak ni la robustez global.
- **Evidencia:** no se dispone del archivo final, capturas, logs ni configuración del sistema.
- **Legal:** el análisis no determina si hubo infracción de derechos de autor o de términos de servicio; solo señala el riesgo.

---

## 7. Relación con ISO/IEC 42001

ISO/IEC 27090 aporta la **taxonomía de amenazas y el catálogo de controles** de seguridad de IA. ISO/IEC 42001 aporta el **sistema de gestión** para que esos controles sean gobernados, medidos, auditados y mejorados.

La integración práctica es:

```
ISO/IEC 42001 (AIMS)
  ├── cl. 6.1.2 / 8.2  → evaluación de riesgo de IA
  ├── cl. 6.1.3 / 8.3  → tratamiento y SoA
  ├── cl. 6.1.4 / 8.4  → evaluación de impacto (AISIA)
  ├── A.6.2.4          → verificación y validación (incluye pruebas adversariales)
  ├── A.6.2.6          → operación y monitorización
  ├── A.6.2.8          → logs de eventos
  ├── A.9              → uso responsable y supervisión humana
  └── A.10.3           → proveedores y cadena de suministro
        └── ISO/IEC 27090 → amenazas y controles técnicos de seguridad de IA
```

El detalle está en `docs/04_controles_iso42001.md`.
