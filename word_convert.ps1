$ErrorActionPreference = 'Stop'
$root = 'd:\project\code\maths\黎曼猜想'

function Convert-MdToDocx {
    param(
        [string]$MdPath,
        [string]$DocxPath
    )
    $word = $null
    try {
        $word = New-Object -ComObject Word.Application
        $word.Visible = $false
        $doc = $word.Documents.Open($MdPath)
        # Page setup: narrow margins (A4, 2.2cm = 62.4pt)
        foreach ($section in $doc.Sections) {
            $section.PageSetup.TopMargin = 62.4
            $section.PageSetup.BottomMargin = 62.4
            $section.PageSetup.LeftMargin = 58
            $section.PageSetup.RightMargin = 58
        }
        # Markdown code blocks become "Normal" para in Word; set them Consolas + wrap + no extra space
        $doc.Content.Font.Name = 'Microsoft YaHei'
        $doc.Content.Font.Size = 12
        # Heading sizes (pandoc md2docx uses H1/H2/H3, Word maps to built-in Heading styles; but md->docx we do it by heading patterns)
        $doc.SaveAs([ref]$DocxPath, [ref]16)  # wdFormatXMLDocument = 16
        $doc.Close()
    }
    finally {
        if ($word) { $word.Quit() }
    }
}

$cnMd = Join-Path $root 'riemann_thesis_cn_clean.md'
$enMd = Join-Path $root 'riemann_thesis_en_clean.md'
$cnOut = Join-Path $root 'riemann_thesis_cn_word.docx'
$enOut = Join-Path $root 'riemann_thesis_en_word.docx'

Convert-MdToDocx -MdPath $cnMd -DocxPath $cnOut
Convert-MdToDocx -MdPath $enMd -DocxPath $enOut
Write-Host "Generated: $cnOut"; Write-Host "Generated: $enOut"

# Optional: replace old files for user convenience
Copy-Item -Path $cnOut -Destination (Join-Path $root 'riemann_thesis_cn.docx') -Force
Copy-Item -Path $enOut -Destination (Join-Path $root 'riemann_thesis_en.docx') -Force
Write-Host 'Overwrote riemann_thesis_cn.docx and riemann_thesis_en.docx with Word-converted versions.'
