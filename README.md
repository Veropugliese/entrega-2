# Contrato de agente — Agente Argentina, Daily Intelligence

## Qué construí
El contrato completo (system prompt + user prompt) para que un agente de IA genere, todos los días, un briefing ejecutivo de Argentina: panorama nacional (economía, política con consecuencia concreta, empresas, PyMEs, consumo, agro) más una búsqueda específica y obligatoria en Córdoba, Tucumán y Santiago del Estero. No es el sistema de software completo — es la pieza de "contrato de prompt" que define identidad, reglas y formato del agente, pensada para que después se pueda enchufar a un pipeline real (búsqueda → normalización → deduplicación → scoring → análisis → reporte) sin reescribir el contrato.

La consigna pedía que la salida fuera estructurada y comparable entre corridas, así que el formato por defecto es un **JSON con schema fijo** (mismas claves todos los días), no markdown libre. Además de las noticias, el JSON expone las decisiones intermedias del agente: qué fuentes falló, qué se descartó y por qué, y qué duplicados se agruparon — para que quede visible que hay un proceso de evaluación, no solo redacción.

Archivos de esta entrega:
- [`system_prompt.md`](system_prompt.md) — identidad, contexto, pipeline de decisión, restricciones y el schema JSON de salida.
- [`user_prompt.md`](user_prompt.md) — la plantilla del pedido diario (fecha, ventana temporal, fuentes disponibles o material pegado).
- [`ejemplos/corrida_2026-08-20.json`](ejemplos/corrida_2026-08-20.json) y [`ejemplos/corrida_2026-08-21.json`](ejemplos/corrida_2026-08-21.json) — dos corridas ficticias con el mismo schema, para mostrar en concreto qué significa "comparable entre corridas".
- [`ejemplos/corrida_real_2026-08-21.json`](ejemplos/corrida_real_2026-08-21.json) — una corrida real: se ejecutó el contrato con búsqueda web real (no datos inventados) para el 21/08/2026, siguiendo el mismo pipeline (buscar → descartar → deduplicar → clasificar → puntuar → generar). Prueba que el contrato funciona con noticias reales y mismo schema.

## Cómo se lo pedí
1. Pegué un boceto grande (ya trabajado con otra IA) de un sistema de dos agentes de noticias (Argentina diario + Global semanal), con arquitectura de software completa, y al final agregué la consigna real de la materia: elegir una tarea recurrente y escribir su contrato (system + user prompt) cubriendo rol, contexto, tarea, restricciones, formato y ejemplos, con salida estructurada y comparable entre corridas.
2. Como el pedido mezclaba dos cosas de tamaño muy distinto, pregunté explícitamente qué parte era la entrega real. Me confirmó: *"lo último es la consigna de lo que tengo que hacer, o sea esa es la salida, lo primero es un gran boceto ya iterado con otra IA [...] analiza lo primero teniendo en cuenta lo segundo y responde acorde, si tenés dudas o recomendaciones, planteálas."*
3. Propuse elegir un solo agente (Argentina Daily, por ser diario y estar bien acotado) en vez de los dos, con el Global como posible próximo paso. El usuario confirmó: *"esta bien, coincido que es mejor hacer un solo agente, y armas el Argentina Daily únicamente, lo otro lo dejamos para cuando ya esté este, si me sirve armo el otro"*, y remarcó que el foco de esta implementación tenía que ser el requisito de salida estructurada y comparable entre corridas.

## Qué funciona
- El system prompt cubre explícitamente las 6 piezas pedidas (rol, contexto, tarea, restricciones, formato, ejemplos), cada una en su propia sección numerada.
- El formato de salida es JSON con un schema fijo: verifiqué con PowerShell que los dos archivos de ejemplo tienen exactamente las mismas claves de nivel superior, en `metadata_corrida` y en cada ítem de `noticias` — es decir, dos corridas reales generadas con este contrato serían diffables campo a campo.
- El contrato deja explícito el comportamiento agéntico pedido por la consigna original: el agente tiene que decidir qué descartar (`noticias_descartadas`), qué es duplicado (`grupos_duplicados`), y qué fuentes contrastar (`fuentes_contrastadas`) — no es una sola llamada que redacta texto libre.
- Cubre las reglas específicas del boceto original que tenían sentido para el contrato: cobertura obligatoria de Córdoba/Tucumán/Santiago del Estero sin forzar contenido si no hay novedades, distinción hecho/declaración/análisis/opinión/rumor, URL directa al artículo (nunca la home), y continuidad si una fuente falla.
- La plantilla de `user_prompt.md` contempla dos escenarios reales de uso: con herramientas de búsqueda activas, o pegando manualmente el material recolectado (útil si se prueba el contrato en un chat sin acceso a internet).

## Qué falta o qué falló
- Los dos primeros ejemplos de salida (`corrida_2026-08-20.json`, `corrida_2026-08-21.json`) son ficticios y están marcados como tales (`"aviso"` en cada JSON) — sirven solo para mostrar el schema.
- El tercer ejemplo (`corrida_real_2026-08-21.json`) sí se generó ejecutando el contrato con búsqueda web real. Ahí se ve el comportamiento agéntico funcionando con datos de verdad: descartó una noticia de Tucumán por estar fuera de la ventana de 24-36h, agrupó 4 medios que cubrían la misma marcha como un solo evento, y no incluyó ninguna noticia de Santiago del Estero porque lo único que encontró ese día fue clima y deportes (sin forzar contenido).
- No se implementó el pipeline de software del boceto original (proveedores, deduplicación automática, scoring programático, etc.) — esta entrega es el contrato de prompt; la corrida real de arriba se hizo a mano en una sesión de chat con herramientas de búsqueda, no con un programa corriendo solo.
- El Agente Global (semanal, geopolítica/mercados/IA/tecnología) queda completamente afuera de esta entrega, tal como se acordó.

## Qué aprendí
*(Nota: esta sección la tenés que completar/ajustar vos con tu propia reflexión — dejo un borrador a partir de lo charlado, para que lo edites.)*

Entendí que la parte más difícil de "darle un contrato" a un agente no es escribir el rol o el tono, sino decidir qué decisiones intermedias tienen que quedar visibles en la salida — si el formato solo mostrara las noticias finales, no se podría distinguir un agente que realmente evalúa y descarta de uno que simplemente redacta lo primero que encuentra. También aprendí que "salida comparable entre corridas" es un requisito de diseño, no de redacción: obliga a fijar un schema (mismas claves siempre, aunque estén vacías) en vez de dejar que el formato varíe según lo que haya para contar ese día.

## Posible evolución futura
- Armar el mismo tipo de contrato para el Agente Global — Weekly Intelligence (geopolítica, economía mundial, mercados, IA, tecnología), reutilizando esta misma estructura de archivos.
- Conectar el contrato a un pipeline real (búsqueda, normalización, deduplicación, scoring) como el descripto en el boceto original.
- Agregar un renderer que convierta el JSON de salida a Markdown/HTML para lectura humana, sin tocar el contrato del agente (separación entre generación de datos y presentación).
