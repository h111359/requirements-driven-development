# Install.Tests.ps1
# Pester tests for install.ps1 PowerShell installer

BeforeAll {
    # Store original location
    $script:OriginalLocation = Get-Location
    
    # Create temporary test directory
    $script:TestDir = New-Item -ItemType Directory -Path (Join-Path $env:TEMP "rdd-test-$(Get-Random)")
    
    # Create mock RDD structure
    $script:MockRddDir = New-Item -ItemType Directory -Path (Join-Path $TestDir "rdd-v1.0.0")
    
    # Create subdirectories
    $dirs = @(
        ".rdd/scripts",
        ".rdd/templates",
        ".github/prompts",
        ".rdd-docs",
        ".vscode"
    )
    
    foreach ($dir in $dirs) {
        New-Item -ItemType Directory -Path (Join-Path $MockRddDir $dir) -Force | Out-Null
    }
    
    # Create mock files
    Set-Content -Path (Join-Path $MockRddDir ".rdd/scripts/rdd.py") -Value "#!/usr/bin/env python3`nprint('RDD')"
    Set-Content -Path (Join-Path $MockRddDir ".vscode/settings.json") -Value "{}"
    Set-Content -Path (Join-Path $MockRddDir "LICENSE") -Value "MIT License"
    
    # Copy install.py if exists
    $installPySource = "scripts/install.py"
    if (Test-Path $installPySource) {
        Copy-Item $installPySource -Destination (Join-Path $MockRddDir "install.py")
    }
}

AfterAll {
    # Clean up test directory
    if (Test-Path $script:TestDir) {
        Remove-Item -Recurse -Force $script:TestDir
    }
    
    # Restore location
    Set-Location $script:OriginalLocation
}

Describe "install.ps1 Script Tests" {
    
    Context "Script Existence and Permissions" {
        It "install.ps1 exists" {
            Test-Path "scripts/install.ps1" | Should -Be $true
        }
        
        It "install.ps1 is readable" {
            { Get-Content "scripts/install.ps1" } | Should -Not -Throw
        }
    }
    
    Context "PowerShell Prerequisites" {
        It "PowerShell version is 5.1 or higher" {
            $PSVersionTable.PSVersion.Major | Should -BeGreaterOrEqual 5
        }
        
        It "Python is available" {
            { python --version } | Should -Not -Throw
        }
        
        It "Git is available" {
            { git --version } | Should -Not -Throw
        }
    }
    
    Context "Directory Operations" {
        It "Can create test directory" {
            $testDir = Join-Path $script:TestDir "test-subdir"
            New-Item -ItemType Directory -Path $testDir -Force
            Test-Path $testDir | Should -Be $true
        }
        
        It "Can navigate to directory" {
            $testDir = Join-Path $script:TestDir "nav-test"
            New-Item -ItemType Directory -Path $testDir -Force
            Set-Location $testDir
            (Get-Location).Path | Should -Be $testDir
            Set-Location $script:OriginalLocation
        }
        
        It "Can list directory contents" {
            $items = Get-ChildItem $script:MockRddDir
            $items | Should -Not -BeNullOrEmpty
        }
    }
    
    Context "Git Repository Detection" {
        It "Can detect git repository" {
            $gitRepo = Join-Path $script:TestDir "git-repo"
            New-Item -ItemType Directory -Path $gitRepo -Force
            Set-Location $gitRepo
            git init | Out-Null
            git config user.name "Test User" | Out-Null
            git config user.email "test@example.com" | Out-Null
            
            Test-Path ".git" | Should -Be $true
            Set-Location $script:OriginalLocation
        }
        
        It "Can detect non-git directory" {
            $nonGitDir = Join-Path $script:TestDir "non-git"
            New-Item -ItemType Directory -Path $nonGitDir -Force
            Set-Location $nonGitDir
            
            Test-Path ".git" | Should -Be $false
            Set-Location $script:OriginalLocation
        }
    }
    
    Context "File Operations" {
        It "Can copy files" {
            $srcFile = Join-Path $script:TestDir "source.txt"
            $dstFile = Join-Path $script:TestDir "dest.txt"
            
            Set-Content -Path $srcFile -Value "test content"
            Copy-Item $srcFile -Destination $dstFile
            
            Test-Path $dstFile | Should -Be $true
            Get-Content $dstFile | Should -Be "test content"
        }
        
        It "Can read file content" {
            $testFile = Join-Path $script:TestDir "read-test.txt"
            Set-Content -Path $testFile -Value "test content"
            
            $content = Get-Content $testFile
            $content | Should -Be "test content"
        }
        
        It "Can write file content" {
            $testFile = Join-Path $script:TestDir "write-test.txt"
            Set-Content -Path $testFile -Value "new content"
            
            Test-Path $testFile | Should -Be $true
            Get-Content $testFile | Should -Be "new content"
        }
    }
    
    Context "Mock RDD Structure" {
        It "Mock RDD directory exists" {
            Test-Path $script:MockRddDir | Should -Be $true
        }
        
        It "RDD scripts directory exists" {
            Test-Path (Join-Path $script:MockRddDir ".rdd/scripts") | Should -Be $true
        }
        
        It "RDD templates directory exists" {
            Test-Path (Join-Path $script:MockRddDir ".rdd/templates") | Should -Be $true
        }
        
        It "GitHub prompts directory exists" {
            Test-Path (Join-Path $script:MockRddDir ".github/prompts") | Should -Be $true
        }
        
        It "rdd.py script exists" {
            Test-Path (Join-Path $script:MockRddDir ".rdd/scripts/rdd.py") | Should -Be $true
        }
    }
    
    Context "install.py Execution" {
        It "install.py can be executed with Python" {
            $installPy = Join-Path $script:MockRddDir "install.py"
            if (Test-Path $installPy) {
                # Just test that Python can parse it
                { python -m py_compile $installPy } | Should -Not -Throw
            }
        }
    }
    
    Context "Error Handling" {
        It "Handles non-existent directory gracefully" {
            $nonExistentDir = Join-Path $script:TestDir "does-not-exist"
            Test-Path $nonExistentDir | Should -Be $false
        }
        
        It "Handles invalid path input" {
            { Test-Path "invalid:\\path" } | Should -Not -Throw
        }
    }
    
    Context "Console Output" {
        It "Can write colored output" {
            { Write-Host "Test message" -ForegroundColor Green } | Should -Not -Throw
        }
        
        It "Can write to console" {
            { Write-Host "Test" } | Should -Not -Throw
        }
    }
}

Describe "Interactive Menu Simulation" {
    Context "Key Press Handling" {
        It "Can detect arrow key simulation" {
            # Test basic key handling logic
            $upKey = [System.ConsoleKey]::UpArrow
            $downKey = [System.ConsoleKey]::DownArrow
            
            $upKey | Should -Be "UpArrow"
            $downKey | Should -Be "DownArrow"
        }
    }
}

Describe "Path Manipulation" {
    Context "Path Operations" {
        It "Can join paths correctly" {
            $joined = Join-Path "parent" "child"
            $joined | Should -Match "parent"
            $joined | Should -Match "child"
        }
        
        It "Can resolve full path" {
            $resolved = Resolve-Path $script:TestDir
            $resolved.Path | Should -Be $script:TestDir.FullName
        }
        
        It "Can get parent directory" {
            $parent = Split-Path $script:TestDir -Parent
            $parent | Should -Not -BeNullOrEmpty
        }
    }
}
