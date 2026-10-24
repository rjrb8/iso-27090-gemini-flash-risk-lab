# 04 — Controles y gobernanza con ISO/IEC 42001

**Base:** ISO/IEC 42001:2023, cláusulas 4–10 y controles del Anexo A.  
**Alcance:** despliegue de Gemini Flash en una interfaz de chat, con un caso de jailbreak multi-turno y elusión de controles de terceros.  
**Nota:** este documento es un **análisis de brechas**, no una declaración de conformidad. La conformidad requiere auditoría, evidencia y un AIMS completo.

---

## 1. Contexto del AIMS

| Elemento | Descripción |
|---|---|
| Organización | Desplegador del modelo (no el proveedor) |
| Sistema de IA | Gemini Flash en chat |
| Uso previsto | Asistencia conversacional y generación de contenido |
| Uso no previsto | Elusión de controles de acceso, rate limits o ToS; extracción no autorizada |
| Partes interesadas | Usuarios, proveedor, titulares de contenido, reguladores |
| Requisitos | Seguridad, legalidad, transparencia, supervisión humana |

---

## 2. Cláusulas del sistema de gestión

| Cláusula | Requisito | Estado observado | Brecha / acción |
|---|---|---|---|
| 4.1 | Comprensión del contexto | No evidenciado | Documentar contexto, partes interesadas y requisitos legales |
| 4.2 | Partes interesadas | No evidenciado | Identificar usuarios, proveedor, titulares y reguladores |
| 4.3 | Alcance del AIMS | No evidenciado | Definir alcance, límites y dependencias |
| 4.4 | Sistema de gestión | No evidenciado | Establecer AIMS y procesos |
| 5.1 | Liderazgo | No evidenciado | Asignar responsabilidad ejecutiva |
| 5.2 | Política de IA | **Parcial** | Falta política explícita anti-elusión y de uso aceptable |
| 5.3 | Roles y autoridades | No evidenciado | Definir roles de producto, seguridad, legal y datos |
| 6.1.2 | Evaluación de riesgo de IA | **Parcial** | Este laboratorio es un insumo; falta proceso formal |
| 6.1.3 | Tratamiento y SoA | **Parcial** | Este documento propone controles; falta SoA firmada |
| 6.1.4 | Evaluación de impacto (AISIA) | No evidenciado | Evaluar impacto individual/societal y derechos |
| 6.2 | Objetivos de IA | No evidenciado | Definir métricas de seguridad y robustez |
| 7.2 | Competencia | No evidenciado | Formar a operadores en riesgos de IA |
| 7.4 | Comunicación | No evidenciado | Canal para reportar abusos/fallos |
| 8.2 | Evaluación de riesgo | **Parcial** | Falta integración en el ciclo de vida |
| 8.3 | Tratamiento de riesgo | **Parcial** | Falta implementación y verificación |
| 8.4 | Evaluación de impacto | No evidenciado | Ejecutar AISIA |
| 9.1 | Monitorización y medición | No evidenciado | Métricas de jailbreak, rechazo, falsos positivos |
| 9.2 | Auditoría interna | No evidenciado | Programa de auditoría |
| 9.3 | Revisión por la dirección | No evidenciado | Revisión periódica |
| 10.1 | No conformidad y acción correctiva | No evidenciado | Proceso de CAPA |
| 10.2 | Mejora continua | No evidenciado | Ciclo de mejora |

---

## 3. Anexo A — controles relevantes

### A.2 Políticas relacionadas con la IA

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.2.2 Política de IA | Debe prohibir la elusión de controles y el uso no autorizado | Parcial | Redactar política de uso aceptable y anti-elusión |
| A.2.3 Alineación con objetivos | La seguridad debe ser objetivo medible | No evidenciado | Métricas de robustez y cumplimiento |

### A.3 Organización interna

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.3.2 Asignación de roles | Responsable de seguridad de IA, legal, datos | No evidenciado | Definir RACI |
| A.3.3 Reporte de preocupaciones | Canal para abusos y fallos | No evidenciado | Crear canal y proceso |
| A.3.4 Documentación de decisiones | Trazabilidad de cambios de política | No evidenciado | Registrar decisiones y excepciones |

### A.4 Recursos para sistemas de IA

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.4.2 Documentación de recursos | Inventario de modelos, herramientas, datos | No evidenciado | ML-BOM y inventario |
| A.4.3 Datos | Calidad, procedencia y licencias | Parcial | Revisar licencias de contenido de terceros |

### A.5 Evaluación de impactos

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.5.2 Proceso AISIA | Evaluar impacto individual y societal | No evidenciado | Ejecutar AISIA del caso |
| A.5.3 Impacto en individuos/grupos | Privacidad, derechos de autor, usuarios | Parcial | Documentar y mitigar |
| A.5.4 Impacto societal | Desinformación, normalización de bypass | Parcial | Evaluar y comunicar |

### A.6 Ciclo de vida del sistema de IA

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.6.2.2 Requisitos | Requisitos de seguridad y legalidad | Parcial | Incluir anti-elusión y ToS |
| A.6.2.3 Diseño | Diseño de guardrails multi-turno | Parcial | Diseñar detección de intención acumulada |
| A.6.2.4 Verificación y validación | Pruebas adversariales y regresión | **Brecha** | Implementar batería multi-turno |
| A.6.2.5 Despliegue | Configuración segura de herramientas | No evidenciado | Sandbox, allowlist, mínimo privilegio |
| A.6.2.6 Operación y monitorización | Detección de abuso y drift | **Brecha** | Monitorizar conversaciones y alertas |
| A.6.2.7 Revisión periódica | Revisar políticas y modelos | No evidenciado | Revisión trimestral |
| A.6.2.8 Logs de eventos | Trazabilidad y retención | Parcial | Definir qué se registra y por cuánto tiempo |

### A.7 Datos

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.7.2 Procedencia de datos | Licencias y autorización | Parcial | Revisar contenido de YouTube |
| A.7.3 Calidad de datos | Exactitud y vigencia | No aplica | — |
| A.7.4 Privacidad | Minimización y protección | Parcial | Redactar nombre/ruta en ejemplos |
| A.7.5 Seguridad de datos | Acceso y cifrado | No evidenciado | Aplicar controles del proveedor |

### A.8 Información a partes interesadas

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.8.2 Documentación del sistema | Capacidades y limitaciones | **Brecha** | Publicar guía de uso y límites |
| A.8.3 Transparencia | Informar sobre IA y limitaciones | Parcial | Añadir avisos en la interfaz |
| A.8.4 Comunicación de incidentes | Notificar fallos relevantes | No evidenciado | Definir proceso |

### A.9 Uso responsable

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.9.2 Procesos de uso responsable | Política y revisión | Parcial | Formalizar uso aceptable |
| A.9.3 Objetivos de uso responsable | Métricas de abuso | No evidenciado | Definir KPIs |
| A.9.4 Uso previsto | Limitar role-play y extracción | **Brecha** | Actualizar términos y guías |
| A.9.5 Supervisión humana | Revisión de salidas de alto riesgo | **Brecha** | Human-in-the-loop para código/acciones |

### A.10 Relaciones con terceros

| Control | Relevancia | Estado | Acción |
|---|---|---|---|
| A.10.2 Proveedores | Diligencia del proveedor del modelo | No evidenciado | Revisar documentación de Google |
| A.10.3 Responsabilidades de terceros | Paquetes y servicios | **Brecha** | Pinning, hash, SBOM, sandbox |
| A.10.4 Clientes | Términos y responsabilidades | Parcial | Actualizar ToS y guías |

---

## 4. Declaración de aplicabilidad (resumen)

| Control | Aplica | Justificación | Estado |
|---|---|---|---|
| A.2.2 | Sí | Política anti-elusión | Parcial |
| A.3.2 | Sí | Roles de seguridad/legal | No evidenciado |
| A.5.2 | Sí | Impacto del bypass y derechos de autor | No evidenciado |
| A.6.2.4 | Sí | Pruebas adversariales multi-turno | Brecha |
| A.6.2.6 | Sí | Monitorización de abuso | Brecha |
| A.6.2.8 | Sí | Logs y retención | Parcial |
| A.8.2 | Sí | Documentar límites | Brecha |
| A.9.4 | Sí | Uso previsto y role-play | Brecha |
| A.9.5 | Sí | Supervisión humana | Brecha |
| A.10.3 | Sí | Cadena de suministro | Brecha |
| A.7.3 | No | No se entrenan datos | N/A |

---

## 5. Hoja de ruta

### 0–30 días

1. Política de uso aceptable con prohibición expresa de elusión.
2. Guía de respuesta para solicitudes de bypass.
3. Verificación de éxito antes de afirmar resultados.
4. Revisión de dependencias y pinning.

### 30–90 días

5. Batería de pruebas multi-turno y métricas.
6. Monitorización y alertas.
7. AISIA del caso.
8. Actualización de términos y avisos.

### 90–180 días

9. SoA y auditoría interna.
10. Revisión por la dirección.
11. Plan de respuesta a incidentes de IA.
12. Mejora continua y reentrenamiento del personal.

---

## 6. Conclusión

El caso no evidencia un AIMS completo. Evidencia una **brecha de control** en la intersección de:

- Política de uso (A.2.2, A.9.4).
- Verificación adversarial (A.6.2.4).
- Monitorización (A.6.2.6).
- Supervisión humana (A.9.5).
- Cadena de suministro (A.10.3).

La organización debería tratar estas brechas como **no conformidades potenciales** y documentar acciones correctivas, no como un fallo aislado del modelo.
