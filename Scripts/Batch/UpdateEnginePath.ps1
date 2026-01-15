# 관리자 권한으로 실행 필요
$EpicRoot = "C:\Program Files\Epic Games"
$TargetLink = "C:\JK\UE_Latest"

# 최신 버전 찾기
$Latest = Get-ChildItem $EpicRoot -Directory "UE_*" | Sort-Object Name -Descending | Select -First 1

# 기존 링크 제거 후 생성
if (Test-Path $TargetLink) { Remove-Item $TargetLink }
New-Item -ItemType Junction -Path $TargetLink -Value $Latest.FullName
Write-Host "Updated $TargetLink to $($Latest.Name)"