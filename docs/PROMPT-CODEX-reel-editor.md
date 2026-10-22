Hola, Codex. Quiero instalar en mi ordenador **Windows** un flujo para montar reels verticales (Instagram/TikTok) a partir de vídeos hablados a cámara. Estás abierto en la carpeta `reels-saltimvanki` (en Documentos), que contiene:

- `AGENTS.md`: cómo debes trabajar en este proyecto (léelo primero).
- `skills/reel-editor/`: la habilidad completa (`SKILL.md`, guía de estilo, estilos, plantillas y scripts en Python).
- `scripts/setup-video-tools.sh`: instala FFmpeg, HyperFrames con su Chrome, yt-dlp, whisper.cpp con el modelo de Whisper en español, y OpenCV.

El flujo funciona dentro de **WSL2 con Ubuntu**. Hazlo paso a paso, explicándome cada paso en español sencillo. No soy programadora: cuando yo tenga que hacer algo, dime exactamente dónde hacer clic o qué escribir.

1. **WSL.** Comprueba en PowerShell si tengo WSL2 con Ubuntu (`wsl -l -v`).
   - Si no lo tengo, guíame para abrir PowerShell **como administradora** y ejecutar `wsl --install -d Ubuntu`.
   - Después tengo que reiniciar y crear mi usuario y contraseña de Ubuntu. Espérame y retoma desde aquí.
   - Comprueba que es la versión 2 y que Ubuntu arranca.
2. **Copia el proyecto a Ubuntu.** Copia esta carpeta a mi carpeta personal de Ubuntu, `~/reels-saltimvanki`, y trabaja siempre desde ahí. Es mucho más rápido que trabajar sobre `/mnt/c`. Si estás en PowerShell, ejecuta los comandos con `wsl -d Ubuntu -- bash -lc "cd ~/reels-saltimvanki && ..."`.
3. **Node.js.** Dentro de Ubuntu, instala Node.js 22 con nvm: el que trae Ubuntu es demasiado antiguo. Déjalo cargado por defecto en `~/.bashrc`.
4. **Herramientas.** Dentro de Ubuntu, ejecuta `bash scripts/setup-video-tools.sh`.
   - Me pedirá la contraseña de Ubuntu para instalar paquetes: avísame antes.
   - Si falla, lee el error, corrígelo y repite hasta que al final muestre las versiones de FFmpeg, yt-dlp, HyperFrames, whisper.cpp y la ruta del modelo de español.
   - Añade `~/.local/bin` a mi PATH en `~/.bashrc`.
5. **Comprobación.** Ejecuta `hyperframes doctor`. Tienen que salir bien FFmpeg, FFprobe, Chrome y whisper-cpp. Ignora Docker, TTS y MusicGen, que son opcionales.
6. **Carpetas de Windows.** Crea `C:\Users\<mi usuario>\Videos\Reels\Entrada` y `C:\Users\<mi usuario>\Videos\Reels\Terminados`. Desde Ubuntu están en `/mnt/c/Users/<mi usuario>/Videos/Reels/...`. Yo dejaré mis vídeos en Entrada y tú me dejarás los reels y los guiones en Terminados.
7. **Instala la habilidad para ti.** Si tu versión de Codex admite skills, copia `skills/reel-editor` a tu carpeta de skills (por ejemplo, `~/.codex/skills/reel-editor`), para que la uses cuando te pida montar un reel. En cualquier caso, mantén `AGENTS.md` en la raíz del proyecto.
8. **Prueba de verdad.** Pídeme que deje en `Entrada` un vídeo vertical corto mío hablando a cámara (10–20 segundos). Monta un reel de prueba siguiendo `skills/reel-editor/SKILL.md`, con el estilo `pop-atrevido` o `dorado-editorial`:
   1. `prepare.py`.
   2. Revisar la transcripción conmigo.
   3. Hacer un guion visual en HTML y enseñármelo.
   4. Rellenar un `project.json` sencillo: gancho, subtítulos con alguna palabra clave y cierre con mi nombre.
   5. `finish.py --snap` para revisar fotogramas.
   6. `finish.py` para renderizar.

   Copia el `final.mp4` a `Terminados` y ábremelo con `explorer.exe`.
9. **Resumen final**: una tabla con cada herramienta, su versión y si funciona, más lo que haya fallado y cómo arreglarlo. Explícame también en 5 líneas cómo pedirte un reel nuevo a partir de ahora.

**Reglas:**
- Pídeme permiso antes de cualquier paso que necesite permisos de administrador o mi contraseña.
- Si tu entorno no tiene acceso a internet o no te deja ejecutar comandos, dímelo para que te lo active. La instalación descarga unos 3 GB: Ubuntu, Chrome para renderizar, el modelo de Whisper de 466 MB y paquetes.
- No borres ni modifiques archivos fuera de esta carpeta, de `~/reels-saltimvanki` y de las carpetas `Videos\Reels`, salvo lo necesario para instalar las herramientas y el PATH.
