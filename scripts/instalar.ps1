# Instala el kit de vídeo de Saltimvanki en Windows (winget).
# Uso (PowerShell): powershell -ExecutionPolicy Bypass -File scripts\instalar.ps1
$ErrorActionPreference = "Stop"

$Base    = Join-Path $HOME ".saltimvanki"
$Modelos = Join-Path $Base "modelos"
$Whisper = Join-Path $Base "whisper"
$Modelo  = if ($env:WHISPER_MODELO) { $env:WHISPER_MODELO } else { "small" }

winget install -e --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
winget install -e --id yt-dlp.yt-dlp --accept-source-agreements --accept-package-agreements
winget install -e --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")

npm install -g hyperframes

# whisper.cpp: binarios oficiales de la última versión en GitHub
New-Item -ItemType Directory -Force -Path $Whisper, $Modelos | Out-Null
if (-not (Get-ChildItem $Whisper -Recurse -Filter "whisper-cli.exe" -ErrorAction SilentlyContinue)) {
  $release = Invoke-RestMethod "https://api.github.com/repos/ggml-org/whisper.cpp/releases/latest"
  $asset   = $release.assets | Where-Object { $_.name -eq "whisper-bin-x64.zip" } | Select-Object -First 1
  $zip     = Join-Path $env:TEMP "whisper-bin-x64.zip"
  Invoke-WebRequest $asset.browser_download_url -OutFile $zip
  Expand-Archive $zip -DestinationPath $Whisper -Force
}
$bin = (Get-ChildItem $Whisper -Recurse -Filter "whisper-cli.exe" | Select-Object -First 1).DirectoryName
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$bin*") {
  [Environment]::SetEnvironmentVariable("Path", "$userPath;$bin", "User")
}
$env:Path += ";$bin"

$destino = Join-Path $Modelos "ggml-$Modelo.bin"
if (-not (Test-Path $destino)) {
  Invoke-WebRequest "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-$Modelo.bin" -OutFile $destino
}

ffmpeg -version | Select-Object -First 1
yt-dlp --version
npx hyperframes --version
whisper-cli --help | Out-Null; if ($?) { "whisper OK" }
"Modelo: $destino"
