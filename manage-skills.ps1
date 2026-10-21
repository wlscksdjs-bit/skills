# ==============================================================================
# wlscksdjs-bit Agent Skills Manager (GitHub On-Demand Skill Manager)
# ==============================================================================
[CmdletBinding()]
param (
    [Parameter(Position = 0)]
    [ValidateSet("list", "use", "add", "remove", "export", "push", "status", "help")]
    [string]$Action = "list",

    [Parameter(Position = 1)]
    [string]$SkillName,

    [string]$Repo = "wlscksdjs-bit/skills",
    [string]$Agent = "antigravity"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsDir = Join-Path $ScriptDir "skills"
$ConfigSkillsDir = "C:\Users\Administrator\.gemini\config\skills"
$WorkspaceSkillsDir = "D:\안티작업 공간\.agents\skills"

function Show-Header {
    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host "   wlscksdjs-bit Agent Skills Manager" -ForegroundColor Cyan
    Write-Host "   GitHub Repository: $Repo" -ForegroundColor DarkCyan
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host ""
}

if ($Action -eq "list") {
    Show-Header
    Write-Host "[1] GitHub Skills Repository ($Repo):" -ForegroundColor Green
    if (Test-Path $SkillsDir) {
        $skills = Get-ChildItem -Directory $SkillsDir
        if ($skills.Count -eq 0) {
            Write-Host "  (No skills registered yet in ./skills)" -ForegroundColor DarkGray
        } else {
            foreach ($s in $skills) {
                $skillFile = Join-Path $s.FullName "SKILL.md"
                if (Test-Path $skillFile) {
                    $desc = ""
                    $lines = Get-Content $skillFile -TotalCount 15
                    foreach ($line in $lines) {
                        if ($line -match "^description:\s*(.*)$") {
                            $desc = $matches[1]
                            break
                        }
                    }
                    Write-Host "  * $($s.Name)" -ForegroundColor Yellow -NoNewline
                    if ($desc) { Write-Host " - $desc" -ForegroundColor Gray } else { Write-Host "" }
                } else {
                    Write-Host "  * $($s.Name) (No SKILL.md)" -ForegroundColor DarkGray
                }
            }
        }
    } else {
        Write-Host "  skills folder not found. Creating..." -ForegroundColor DarkGray
        New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
    }

    Write-Host ""
    Write-Host "[2] Local Environment Status:" -ForegroundColor Green
    if (Test-Path $ConfigSkillsDir) {
        $count = (Get-ChildItem -Directory $ConfigSkillsDir).Count
        Write-Host "  * Global config skills ($ConfigSkillsDir): $count" -ForegroundColor $(if ($count -gt 50) { "Red" } else { "Green" })
    }
    if (Test-Path $WorkspaceSkillsDir) {
        $wcount = (Get-ChildItem -Directory $WorkspaceSkillsDir).Count
        Write-Host "  * Workspace skills ($WorkspaceSkillsDir): $wcount" -ForegroundColor $(if ($wcount -gt 50) { "Red" } else { "Green" })
    }
    Write-Host ""
    Write-Host "[Quick Tips]" -ForegroundColor Cyan
    Write-Host "  On-demand use  : .\manage-skills.ps1 use [skill-name]" -ForegroundColor Cyan
    Write-Host "  Install locally : .\manage-skills.ps1 add [skill-name]" -ForegroundColor Cyan
    Write-Host "  Remove local    : .\manage-skills.ps1 remove [skill-name]" -ForegroundColor Cyan
    Write-Host "  Export local    : .\manage-skills.ps1 export [skill-name]" -ForegroundColor Cyan
    Write-Host "  Push to GitHub  : .\manage-skills.ps1 push [commit-message]" -ForegroundColor Cyan
}
elseif ($Action -eq "use") {
    if (-not $SkillName) {
        Write-Host "Please specify a skill name. Example: .\manage-skills.ps1 use [skill-name]" -ForegroundColor Red
        return
    }
    Show-Header
    Write-Host ">> Fetching and executing '$SkillName' from GitHub on-demand..." -ForegroundColor Green
    npx.cmd skills use "$Repo@$SkillName"
}
elseif ($Action -eq "add") {
    if (-not $SkillName) {
        Write-Host "Please specify a skill name. Example: .\manage-skills.ps1 add [skill-name]" -ForegroundColor Red
        return
    }
    Show-Header
    Write-Host ">> Installing '$SkillName' from GitHub to agent '$Agent'..." -ForegroundColor Green
    npx.cmd skills add $Repo --skill $SkillName --agent $Agent
}
elseif ($Action -eq "remove") {
    if (-not $SkillName) {
        Write-Host "Please specify a skill name. Example: .\manage-skills.ps1 remove [skill-name]" -ForegroundColor Red
        return
    }
    Show-Header
    Write-Host ">> Removing '$SkillName' from agent '$Agent' to save tokens..." -ForegroundColor Green
    npx.cmd skills remove $SkillName --agent $Agent -y
}
elseif ($Action -eq "export") {
    if (-not $SkillName) {
        Write-Host "Please specify a local skill name to export. Example: .\manage-skills.ps1 export [skill-name]" -ForegroundColor Red
        return
    }
    Show-Header
    $sourcePath = $null
    if (Test-Path (Join-Path $WorkspaceSkillsDir $SkillName)) {
        $sourcePath = Join-Path $WorkspaceSkillsDir $SkillName
    } elseif (Test-Path (Join-Path $ConfigSkillsDir $SkillName)) {
        $sourcePath = Join-Path $ConfigSkillsDir $SkillName
    }

    if (-not $sourcePath) {
        Write-Host "Skill '$SkillName' not found in workspace or config directories." -ForegroundColor Red
        return
    }

    if (-not (Test-Path $SkillsDir)) {
        New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
    }

    $targetPath = Join-Path $SkillsDir $SkillName
    Copy-Item -Path $sourcePath -Destination $targetPath -Recurse -Force
    Write-Host ">> Exported '$SkillName' from $sourcePath to $targetPath" -ForegroundColor Green
    Write-Host "   To commit and push to GitHub, run: .\manage-skills.ps1 push" -ForegroundColor Cyan
}
elseif ($Action -eq "push") {
    Show-Header
    Write-Host ">> Staging and pushing changes to GitHub ($Repo)..." -ForegroundColor Green
    git -C $ScriptDir add .
    $msg = if ($SkillName) { "feat(skills): update $SkillName" } else { "feat(skills): update skills" }
    git -C $ScriptDir commit -m $msg
    git -C $ScriptDir push -u origin main
}
elseif ($Action -eq "status") {
    Show-Header
    git -C $ScriptDir status
}
else {
    Show-Header
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  .\manage-skills.ps1 list                 - List skills in repo and local status"
    Write-Host "  .\manage-skills.ps1 use [skill-name]     - On-demand use (no local install)"
    Write-Host "  .\manage-skills.ps1 add [skill-name]     - Install skill locally"
    Write-Host "  .\manage-skills.ps1 remove [skill-name]  - Remove skill from local"
    Write-Host "  .\manage-skills.ps1 export [local-skill] - Export local skill into this repo"
    Write-Host "  .\manage-skills.ps1 push [message]       - Commit & push changes to GitHub"
}
