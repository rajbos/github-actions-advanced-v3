param(
    [string]$DeckDirectory = (Join-Path $PSScriptRoot '..\slides\powerpoint'),
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\.validation\powerpoint-render')
)

$ErrorActionPreference = 'Stop'
$decks = @(Get-ChildItem -LiteralPath $DeckDirectory -Filter '*.pptx' -File)
if ($decks.Count -eq 0) { throw "No PowerPoint decks found in $DeckDirectory" }
$output = [IO.Path]::GetFullPath($OutputDirectory)
[void](New-Item -ItemType Directory -Path $output -Force)
$hadPowerPoint = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$ppt = New-Object -ComObject PowerPoint.Application
$failures = [Collections.Generic.List[string]]::new()
$results = @()

function Test-TextBounds($shape, [string]$location) {
    if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame2.HasText -eq -1) {
        $text = $shape.TextFrame2.TextRange
        $width = $shape.Width - $shape.TextFrame2.MarginLeft - $shape.TextFrame2.MarginRight
        $height = $shape.Height - $shape.TextFrame2.MarginTop - $shape.TextFrame2.MarginBottom
        if ($text.BoundWidth -gt ($width + 2) -or $text.BoundHeight -gt ($height + 2)) {
            $failures.Add("$location bounds=$($text.BoundWidth)x$($text.BoundHeight); available=${width}x${height}")
        }
    }
}

try {
    foreach ($file in $decks) {
        $deck = $null
        try {
            $deck = $ppt.Presentations.Open($file.FullName, -1, 0, 0)
            foreach ($slide in $deck.Slides) {
                foreach ($shape in $slide.Shapes) {
                    $location = "$($file.Name) slide $($slide.SlideIndex) $($shape.Name)"
                    if ($shape.Left -lt 0 -or $shape.Top -lt 0 -or
                        $shape.Left + $shape.Width -gt $deck.PageSetup.SlideWidth + 2 -or
                        $shape.Top + $shape.Height -gt $deck.PageSetup.SlideHeight + 2) {
                        $failures.Add("$location extends beyond the slide")
                    }
                    if ($shape.Name -like 'Example *' -and $shape.Top + $shape.Height -gt 6.8 * 72) {
                        $failures.Add("$location overlaps the footer region")
                    }
                    Test-TextBounds $shape $location
                    if ($shape.HasTable -eq -1) {
                        for ($r = 1; $r -le $shape.Table.Rows.Count; $r++) {
                            for ($c = 1; $c -le $shape.Table.Columns.Count; $c++) {
                                Test-TextBounds $shape.Table.Cell($r, $c).Shape "$location cell $r,$c"
                            }
                        }
                    }
                }
            }
            $deck.Export((Join-Path $output $file.BaseName), 'PNG', 1600, 900)
            $results += @{
                file = $file.Name
                sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
                slides = $deck.Slides.Count
            }
            Write-Output "$($file.Name): rendered $($deck.Slides.Count) slides"
        }
        finally {
            if ($null -ne $deck) {
                $deck.Close()
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)
            }
        }
    }
    @{
        powerpoint_version = $ppt.Version
        decks = $results
        overflows = @($failures.ToArray())
        tolerance_points = 2
        includes_table_cells = $true
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $output 'native-validation.json') -Encoding utf8
    if ($failures.Count -gt 0) { throw ($failures -join "`n") }
    Write-Output 'Native text-fit checks passed, including all table cells.'
}
finally {
    if (-not $hadPowerPoint -and $ppt.Presentations.Count -eq 0) { $ppt.Quit() }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($ppt)
}
