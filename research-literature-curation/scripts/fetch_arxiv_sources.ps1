param(
  [Parameter(Mandatory = $true)]
  [string]$PapersRoot,

  [int]$DelaySeconds = 2
)

$ProgressPreference = "SilentlyContinue"

function Get-ArxivIdFromMetadata {
  param([string]$MetadataPath)
  $line = Get-Content $MetadataPath | Where-Object { $_ -match '^- id:' } | Select-Object -First 1
  if (-not $line) {
    return $null
  }
  return ($line -replace '^- id:\s*', '').Trim()
}

$paperDirs = Get-ChildItem -Directory $PapersRoot
$downloaded = 0

foreach ($dir in $paperDirs) {
  $metadataPath = Join-Path $dir.FullName 'metadata.md'
  if (-not (Test-Path $metadataPath)) {
    continue
  }

  $arxivId = Get-ArxivIdFromMetadata -MetadataPath $metadataPath
  if (-not $arxivId) {
    continue
  }

  $srcTar = Join-Path $dir.FullName 'source.tar'
  $srcDir = Join-Path $dir.FullName 'src'
  if ((Test-Path $srcTar) -and (Test-Path $srcDir)) {
    continue
  }

  $srcUrl = "https://arxiv.org/e-print/$arxivId"
  try {
    Invoke-WebRequest -UseBasicParsing $srcUrl -OutFile $srcTar
    New-Item -ItemType Directory -Force $srcDir | Out-Null
    tar -xf $srcTar -C $srcDir
    $downloaded += 1
    Start-Sleep -Seconds $DelaySeconds
  } catch {
    Set-Content -Path (Join-Path $dir.FullName 'source_fetch_error.txt') -Value $_.Exception.Message -Encoding utf8
  }
}

Write-Output ("Downloaded and extracted {0} paper sources in {1}" -f $downloaded, $PapersRoot)
