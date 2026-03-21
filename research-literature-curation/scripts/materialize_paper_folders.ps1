param(
  [Parameter(Mandatory = $true)]
  [string]$CandidatePoolPath,

  [Parameter(Mandatory = $true)]
  [string[]]$SelectedIds,

  [Parameter(Mandatory = $true)]
  [string]$OutputRoot
)

function New-Slug {
  param([string]$Text)
  $slug = $Text.ToLower()
  $slug = [regex]::Replace($slug, '[^a-z0-9]+', '-')
  $slug = $slug.Trim('-')
  if ([string]::IsNullOrWhiteSpace($slug)) {
    return "paper"
  }
  return $slug
}

$pool = Get-Content -Raw $CandidatePoolPath | ConvertFrom-Json
$index = @{}
foreach ($paper in $pool) {
  $index[$paper.id] = $paper
}

New-Item -ItemType Directory -Force $OutputRoot | Out-Null

foreach ($id in $SelectedIds) {
  if (-not $index.ContainsKey($id)) {
    continue
  }

  $paper = $index[$id]
  $year = ([datetime]$paper.published).Year
  $folderName = "{0}-{1}" -f (New-Slug -Text $paper.title), $year
  $folderPath = Join-Path $OutputRoot $folderName
  New-Item -ItemType Directory -Force $folderPath | Out-Null

  $metadata = @"
# Metadata

- id: $($paper.id)
- title: $($paper.title)
- year: $year
- venue: arXiv
- url: $($paper.url)
- pdf_url: $($paper.pdf_url)
- tags: $([string]::Join(', ', $paper.tags))
- search_query: $($paper.search_query)

## Summary

$($paper.summary)
"@

  $notes = @"
# Paper Note

## Metadata
- id: $($paper.id)
- title: $($paper.title)
- year: $year
- venue: arXiv
- url: $($paper.url)
- pdf_url: $($paper.pdf_url)
- tags: $([string]::Join(', ', $paper.tags))

## One-paragraph summary

$($paper.summary)

## Problem setting
- task or environment:
- user or agent setting:
- personalization relevance:
- procedural-memory relevance:

## Memory design
- what is stored:
- storage format:
- update rule:
- retrieval rule:
- forgetting or consolidation:

## Method details
- architecture:
- training or prompting:
- tools or external memory:

## Evaluation
- benchmarks:
- metrics:
- baselines:

## Main findings
- finding 1:
- finding 2:

## Limitations
- limitation 1:
- limitation 2:

## Why it matters for this survey

## Citation block
```bibtex
$($paper.bib)
```
"@

  $links = @"
$($paper.url)
$($paper.pdf_url)
"@

  Set-Content -Path (Join-Path $folderPath 'metadata.md') -Value $metadata -Encoding utf8
  Set-Content -Path (Join-Path $folderPath 'notes.md') -Value $notes -Encoding utf8
  Set-Content -Path (Join-Path $folderPath 'bib.txt') -Value $paper.bib -Encoding utf8
  Set-Content -Path (Join-Path $folderPath 'links.txt') -Value $links -Encoding utf8
}

Write-Output ("Materialized {0} paper folders into {1}" -f $SelectedIds.Count, $OutputRoot)
