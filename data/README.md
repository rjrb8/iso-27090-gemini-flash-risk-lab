# Datos

## `Conversacion.sanitized.txt`

Versión saneada de la conversación analizada. Conserva la numeración de líneas del original para que las referencias de `docs/02_analisis_conversacion.md` sigan siendo válidas.

### Original

| Campo | Valor |
|---|---|
| Nombre | `Conversacion.txt` |
| Tamaño | 54.512 bytes |
| Líneas | 904 |
| Codificación | UTF-8 |
| SHA-256 | `4f1057a0c4fb409970017aa98673cc66e748984f0554d54764638600bbb55e03` |
| Origen | `http://192.168.1.106:8080/Conversacion.txt` |

El original **no se incluye** en el repositorio. Contiene un nombre de usuario, una URL/ID de vídeo y código operativo.

### Redacciones

- `[USUARIO]`: nombre.
- `[VIDEO_REDACTADO]`: URL/ID del vídeo.
- `[RUTA_LOCAL]`: ruta del equipo del usuario.
- `[CODIGO_REDACTADO]`: línea de código operativo.
- `[CAPTURA_REFERENCIADA]`: marcador de captura.

### Regeneración

```bash
python3 analysis/sanitize_conversation.py /ruta/Conversacion.txt data/Conversacion.sanitized.txt
```

### Advertencia

La versión saneada sigue siendo un caso de estudio. No debe usarse para reproducir el bypass ni para extraer contenido de terceros.
