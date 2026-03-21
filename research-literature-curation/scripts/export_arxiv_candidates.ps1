param(
  [Parameter(Mandatory = $true)]
  [string[]]$Queries,

  [int]$MaxResultsPerQuery = 25,

  [string]$OutputPath = "candidate_pool.json"
)

$ProgressPreference = "SilentlyContinue"

function Get-ArxivFeed {
  param(
    [string]$Query,
    [int]$MaxResults
  )

  $encoded = [System.Uri]::EscapeDataString($Query)
  $url = "https://export.arxiv.org/api/query?search_query=all:$encoded&start=0&max_results=$MaxResults"
  [xml]$xml = (Invoke-WebRequest -UseBasicParsing $url).Content
  return $xml.feed.entry
}

$seen = @{}
$items = New-Object System.Collections.Generic.List[object]

foreach ($query in $Queries) {
  $entries = Get-ArxivFeed -Query $query -MaxResults $MaxResultsPerQuery
  foreach ($entry in $entries) {
    $id = ($entry.id -split '/')[-1]
    if ($seen.ContainsKey($id)) {
      continue
    }

    $pdfLink = $null
    foreach ($link in $entry.link) {
      if ($link.title -eq 'pdf') {
        $pdfLink = $link.href
      }
    }

    $authors = @()
    foreach ($author in $entry.author) {
      $authors += $author.name
    }

    $tags = @()
    foreach ($category in $entry.category) {
      $tags += $category.term
    }

    $obj = [PSCustomObject]@{
      id = $id
      title = ($entry.title -replace '\s+', ' ').Trim()
      published = [string]$entry.published
      updated = [string]$entry.updated
      url = [string]$entry.id
      pdf_url = $pdfLink
      authors = $authors
      tags = $tags
      summary = ($entry.summary -replace '\s+', ' ').Trim()
      search_query = $query
      bib = "@misc{$id, title={" + (($entry.title -replace '\s+', ' ').Trim()) + "}, year={" + ([datetime]$entry.published).Year + "}, eprint={" + $id + "}, archivePrefix={arXiv}}"
    }

    $items.Add($obj) | Out-Null
    $seen[$id] = $true
  }
}

$items | ConvertTo-Json -Depth 8 | Set-Content -Path $OutputPath -Encoding utf8
Write-Output ("Exported {0} unique papers to {1}" -f $items.Count, $OutputPath)
