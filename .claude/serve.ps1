$root = Split-Path -Parent $PSScriptRoot
$l = New-Object System.Net.HttpListener
$l.Prefixes.Add("http://localhost:8777/")
$l.Start()
$types = @{".html"="text/html; charset=utf-8";".jpg"="image/jpeg";".png"="image/png";".mp4"="video/mp4";".css"="text/css";".js"="text/javascript"}
while ($l.IsListening) {
  $c = $l.GetContext()
  try {
    $p = [Uri]::UnescapeDataString($c.Request.Url.AbsolutePath.TrimStart('/'))
    if ($p -eq "") { $p = "index.html" }
    $f = Join-Path $root $p
    if (Test-Path $f -PathType Leaf) {
      $ext = [IO.Path]::GetExtension($f).ToLower()
      if ($types[$ext]) { $c.Response.ContentType = $types[$ext] }
      $c.Response.AddHeader("Accept-Ranges", "bytes")
      $c.Response.AddHeader("Cache-Control", "no-cache")
      $fs = [IO.File]::OpenRead($f)
      try {
        $len = $fs.Length; $start = 0; $end = $len - 1
        $range = $c.Request.Headers["Range"]
        if ($range -match '^bytes=(\d*)-(\d*)$') {
          if ($matches[1] -ne '') { $start = [int64]$matches[1] }
          if ($matches[2] -ne '') { $end = [Math]::Min([int64]$matches[2], $len - 1) }
          elseif ($matches[1] -eq '') { $start = $len - [int64]$matches[2] }
          $c.Response.StatusCode = 206
          $c.Response.AddHeader("Content-Range", "bytes $start-$end/$len")
        }
        $count = $end - $start + 1
        $c.Response.ContentLength64 = $count
        $fs.Seek($start, 'Begin') | Out-Null
        $buf = New-Object byte[] 65536
        while ($count -gt 0) {
          $n = $fs.Read($buf, 0, [Math]::Min($buf.Length, $count))
          if ($n -le 0) { break }
          $c.Response.OutputStream.Write($buf, 0, $n); $count -= $n
        }
      } finally { $fs.Close() }
    } else { $c.Response.StatusCode = 404 }
  } catch {} finally { try { $c.Response.Close() } catch {} }
}

