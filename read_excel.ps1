$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$workbook = $excel.Workbooks.Open("C:\Users\kiria\Mi unidad\LASER\utiles\MEDIDAS.xlsx")
$sheet = $workbook.Sheets.Item(1)
$maxRow = $sheet.UsedRange.Rows.Count
$maxCol = $sheet.UsedRange.Columns.Count

for ($row = 1; $row -le $maxRow; $row++) {
    $line = ""
    for ($col = 1; $col -le $maxCol; $col++) {
        $cellText = $sheet.Cells.Item($row, $col).Text
        $line += "$cellText | "
    }
    Write-Host $line
}

$workbook.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
