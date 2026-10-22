Hola, Codex. Quiero instalar en este ordenador un flujo para montar reels verticales (Instagram/TikTok) a partir de vídeos hablados a cámara. Estás abierto en la carpeta `reels-saltimvanki`, que contiene:

- `AGENTS.md`: cómo debes trabajar en este proyecto (léelo primero).
- `skills/reel-editor/`: la habilidad completa (`SKILL.md`, guía de estilo, estilos, plantillas y scripts en Python).
- `scripts/setup-video-tools.sh`: instala FFmpeg, HyperFrames, yt-dlp, whisper.cpp con el modelo de Whisper en español, y OpenCV.

Hazlo paso a paso y explícame cada paso en español sencillo. No soy programadora.

1. **Detecta mi sistema operativo.**
   - **Windows**: el flujo funciona dentro de WSL2 con Ubuntu. Comprueba si lo tengo (`wsl -l -v`). Si no, dime cómo instalarlo (`wsl --install -d Ubuntu`, como administradora, y reiniciar). Después copia esta carpeta a mi carpeta personal de Ubuntu (`~/reels-saltimvanki`) y trabaja siempre desde ahí.
   - **macOS**: usa Homebrew. Si no lo tengo, instálalo, y también las herramientas de línea de comandos de Xcode (`xcode-select --install`).
   - **Linux**: sigue directamente.
2. **Prerrequisitos**: Node.js 20 o superior (con nvm si no está, o si está pero es más antiguo), Python 3.10 o superior con pip, git, cmake y un compilador de C/C++.
3. **Ejecuta `bash scripts/setup-video-tools.sh`.** Si falla, lee el error, corrígelo y vuelve a ejecutarlo hasta que al final muestre las versiones de FFmpeg, yt-dlp, HyperFrames, whisper.cpp y la ruta del modelo de español. Asegúrate de que `~/.local/bin` está en mi PATH de forma permanente (en `~/.zshrc` o `~/.bashrc`).
4. **Comprueba todo** con `hyperframes doctor`. Tienen que salir bien FFmpeg, FFprobe, Chrome y whisper-cpp. Si falta Chrome, ejecuta `hyperframes browser ensure`. Ignora Docker, TTS y MusicGen, que son opcionales.
5. **Instala la habilidad para ti.** Si tu versión de Codex admite skills, copia `skills/reel-editor` a tu carpeta de skills (por ejemplo, `~/.codex/skills/reel-editor`), para que la uses cuando te pida montar un reel. En cualquier caso, mantén el `AGENTS.md` en la raíz de este proyecto.
6. **Prueba de verdad.** Pídeme un vídeo vertical corto mío hablando a cámara (10–20 segundos) y monta un reel de prueba siguiendo `skills/reel-editor/SKILL.md`, con el estilo `pop-atrevido` o `dorado-editorial`:
   1. `prepare.py`.
   2. Revisar la transcripción conmigo.
   3. Rellenar un `project.json` sencillo: gancho, subtítulos con alguna palabra clave y cierre con mi nombre.
   4. `finish.py --snap` para revisar fotogramas.
   5. `finish.py` para renderizar.

   Ábreme el `final.mp4` al terminar.
7. **Resumen final**: una tabla con cada herramienta, su versión y si funciona, más lo que haya fallado y cómo arreglarlo. Explícame también en 5 líneas cómo pedirte un reel nuevo a partir de ahora.

**Reglas:**
- Pídeme permiso antes de cualquier instalación que necesite contraseña de administrador.
- Si tu entorno no tiene acceso a internet, dímelo para que te lo active. La instalación descarga unos 3 GB: navegador Chrome para renderizar, modelo de Whisper de 466 MB y paquetes.
- No borres ni modifiques archivos fuera de esta carpeta, salvo los de instalación de herramientas y mi archivo de configuración del terminal para el PATH.
