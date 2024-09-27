$ErrorActionPreference = "Stop"

# https://www.electronjs.org/docs/latest/api/app#appgetpathname
if ($IsWindows) {
    $appData = [System.IO.Path]::Combine($env:APPDATA)
} elseif ($IsMacOS) {
    $appData = [System.IO.Path]::Combine([Environment]::ExpandEnvironmentVariables("~/Library/Application Support"))
} else {
    $xdgConfigHome = $env:XDG_CONFIG_HOME
    if (-not [string]::IsNullOrEmpty($xdgConfigHome)) {
        $appData = [System.IO.Path]::Combine($xdgConfigHome)
    } else {
        $appData = [System.IO.Path]::Combine([Environment]::ExpandEnvironmentVariables("~/.config"))
    }
}

Write-Host -ForegroundColor Green "App Data Path:" 
$appData

$localStoragePath = [System.IO.Path]::Combine($appData, "oss-browser", "Local Storage", "file__0.localstorage")
Write-Host -ForegroundColor Green "Local Storage Path:" 
$localStoragePath

$base64Value = & sqlite3 "$localStoragePath" "SELECT hex(value) FROM ItemTable WHERE key = 'auth-his'"
$bytes = [System.Convert]::FromHexString($base64Value)
$encryptedHex = [System.Text.Encoding]::Unicode.GetString($bytes)
Write-Host -ForegroundColor Green "Encrypted Hex:" 
$encryptedHex

# from EVP_BytesToKey or `openssl aes192 -k "x82m#*lx8vv" -md md5 -P -nosalt`
$keyHex = "fee4f348522b12260fec6ba9925686333635fae3febafca0"
$ivHex = "aac0e22065147dbd9f97881dae73f545"

$key = [System.Convert]::FromHexString($keyHex)
$iv = [System.Convert]::FromHexString($ivHex)
$encrypted = [System.Convert]::FromHexString($encryptedHex)

$aes = [System.Security.Cryptography.Aes]::Create()
$aes.Key = $key
$aes.IV = $iv
$aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
$aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7

$decryptor = $aes.CreateDecryptor()
$decryptedBytes = $decryptor.TransformFinalBlock($encrypted, 0, $encrypted.Length)
$decryptedText = [System.Text.Encoding]::UTF8.GetString($decryptedBytes)

Write-Host -ForegroundColor Green "Decrypted Text:" 
$decryptedText

Write-Host -ForegroundColor Green "Decrypted Data:"
$decryptedData = ConvertFrom-Json $decryptedText
$decryptedData
