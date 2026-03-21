param(
    [Parameter(Mandatory = $true)]
    [string]$Query,

    [Parameter(Mandatory = $true)]
    [string]$PapersRoot,

    [int]$Top = 50,

    [string]$OutputPath,

    [switch]$NotesOnly
)

$ErrorActionPreference = "Stop"

function Get-RelativePathCompat {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BasePath,

        [Parameter(Mandatory = $true)]
        [string]$TargetPath
    )

    $baseFull = [System.IO.Path]::GetFullPath($BasePath)
    if (-not $baseFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $baseFull += [System.IO.Path]::DirectorySeparatorChar
    }

    $targetFull = [System.IO.Path]::GetFullPath($TargetPath)
    $baseUri = New-Object System.Uri($baseFull)
    $targetUri = New-Object System.Uri($targetFull)
    $relativeUri = $baseUri.MakeRelativeUri($targetUri)
    return [System.Uri]::UnescapeDataString($relativeUri.ToString()) -replace "/", [System.IO.Path]::DirectorySeparatorChar
}

if (-not (Get-Command rg -ErrorAction SilentlyContinue)) {
    throw "ripgrep (rg) is required but was not found in PATH."
}

$resolvedRoot = (Resolve-Path $PapersRoot).Path

$globs = @(
    "notes.md",
    "metadata.md",
    "bib.txt",
    "links.txt"
)

if (-not $NotesOnly) {
    $globs += @(
        "src/**/*.tex",
        "src/**/*.md",
        "src/**/*.txt",
        "src/**/*.bib",
        "src/**/*.bbl"
    )
}

$rgArgs = @(
    "--json",
    "--ignore-case",
    "--hidden",
    "--no-messages"
)

foreach ($glob in $globs) {
    $rgArgs += @("--glob", $glob)
}

$rgArgs += @("--", $Query, $resolvedRoot)

$rawEvents = & rg @rgArgs

$matches = New-Object System.Collections.Generic.List[object]

foreach ($line in $rawEvents) {
    if ([string]::IsNullOrWhiteSpace($line)) {
        continue
    }

    $event = $line | ConvertFrom-Json
    if ($event.type -ne "match") {
        continue
    }

    $path = $event.data.path.text
    $relativePath = Get-RelativePathCompat -BasePath $resolvedRoot -TargetPath $path
    $parts = $relativePath -split "[/\\]"
    $paperId = if ($parts.Length -gt 0) { $parts[0] } else { "unknown-paper" }
    $text = $event.data.lines.text -replace "\s+", " "
    $text = $text.Trim()

    $matches.Add([PSCustomObject]@{
        PaperId      = $paperId
        RelativePath = $relativePath
        LineNumber   = [int]$event.data.line_number
        Snippet      = $text
    })
}

$selected = $matches | Select-Object -First $Top

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# Corpus Search Results")
$lines.Add("")
$lines.Add("- Query: ``$Query``")
$lines.Add("- Papers root: ``$resolvedRoot``")
$lines.Add("- Search mode: " + ($(if ($NotesOnly) { "notes-and-metadata-only" } else { "notes-metadata-and-full-text" })))
$lines.Add("- Total matches captured: " + $selected.Count)
$lines.Add("")

if ($selected.Count -eq 0) {
    $lines.Add("No matches found.")
}
else {
    $grouped = $selected | Group-Object PaperId
    foreach ($group in $grouped) {
        $lines.Add("## " + $group.Name)
        $lines.Add("")
        foreach ($match in $group.Group) {
            $lines.Add("- ``" + $match.RelativePath + ":" + $match.LineNumber + "`` " + $match.Snippet)
        }
        $lines.Add("")
    }
}

$result = $lines -join [Environment]::NewLine

if ($OutputPath) {
    $outputDir = Split-Path -Parent $OutputPath
    if ($outputDir) {
        New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    }
    Set-Content -Path $OutputPath -Value $result -Encoding UTF8
}

$result
