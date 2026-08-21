# Configuración de GitHub Actions

El repositorio queda preparado para generar el briefing con OpenAI, buscar noticias en la web, validar el JSON, crear una versión HTML legible, enviarla por correo y conservar el JSON como artefacto durante 30 días.

## Lo que debe hacer manualmente el responsable de GitHub

1. Revisar esta rama y fusionarla a `main`. GitHub solo ejecuta automáticamente los eventos `schedule` de workflows presentes en la rama predeterminada.
2. En GitHub, abrir **Settings → Secrets and variables → Actions**.
3. Crear estos **Repository secrets**:
   - `OPENAI_API_KEY`: clave de un proyecto de OpenAI API con facturación habilitada.
   - `EMAIL_USERNAME`: cuenta Gmail desde la cual se envía (dirección completa).
   - `EMAIL_PASSWORD`: contraseña de aplicación de 16 caracteres de esa cuenta de Google. No usar la contraseña normal ni guardarla en un archivo del repositorio.
   - `EMAIL_TO`: dirección destinataria completa, confirmada y sin espacios.
4. Crear estas **Repository variables**:
   - `DAILY_SEND_HOUR`: hora local de envío, entero de `0` a `23` (por ejemplo, `8`).
   - `TIME_ZONE`: `America/Argentina/Buenos_Aires`.
   - `OPENAI_MODEL`: `gpt-5.4-mini` (se puede cambiar sin editar código).
   - `WINDOW_HOURS`: `36`.
5. Abrir **Actions → Argentina Daily Intelligence → Run workflow** en `main`.
6. Hacer primero una prueba con **Enviar el resultado por correo = false**. Descargar y revisar el artefacto JSON.
7. Repetir la prueba con **Enviar el resultado por correo = true** y confirmar recepción y carpeta de correo no deseado.

## Consideraciones importantes

- La programación de GitHub Actions no garantiza el minuto exacto; puede demorarse algunos minutos cuando hay alta demanda.
- El workflow se despierta al minuto 7 de cada hora. El script solo genera y envía cuando esa hora coincide con `DAILY_SEND_HOUR` en `TIME_ZONE`; cambiar la hora no requiere editar YAML.
- Una ejecución manual ignora `DAILY_SEND_HOUR`, para permitir pruebas en cualquier momento.
- OpenAI API y la búsqueda web pueden generar consumo facturable. El modelo queda configurable para controlar calidad y costo.
- El emisor está preparado directamente para Gmail mediante `smtp.gmail.com` con STARTTLS; no hay que configurar servidor, puerto ni remitente.
- Gmail no permite autenticar este tipo de conexión SMTP con la contraseña normal. En la misma cuenta de Google hay que activar la verificación en dos pasos y crear una [contraseña de aplicación](https://myaccount.google.com/apppasswords). No hace falta crear otra cuenta.
- Los secretos nunca se imprimen ni se almacenan en los artefactos.

## Diagnóstico rápido

- `Falta ... OPENAI_API_KEY`: no se creó el secreto o está vacío.
- `HTTP 401` de OpenAI: clave inválida o revocada.
- `HTTP 429` de OpenAI: límite de uso, crédito o facturación.
- `SMTPAuthenticationError`: comprobar que `EMAIL_USERNAME` sea la dirección Gmail completa y que `EMAIL_PASSWORD` contenga una contraseña de aplicación vigente, no la contraseña normal.
- No se ejecuta diariamente: confirmar que el workflow fue fusionado a `main` y que Actions está habilitado en el repositorio.
