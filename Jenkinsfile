pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                bat '''
                    echo Setting up Python environment...
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install bandit
                    echo Python setup complete!
                '''
            }
        }
        
        stage('Bandit Security Scan') {
            steps {
                bat '''
                    @echo off
                    echo Running Bandit security scan...
                    call venv\\Scripts\\activate.bat
                    
                    echo ========================================
                    echo Running Bandit with severity filtering
                    echo ========================================
                    
                    REM Run bandit and capture output
                    bandit -r . -f txt -o bandit_report.txt
                    
                    REM Check for high severity issues
                    echo Checking for HIGH severity issues...
                    
                    REM Use findstr to look for "HIGH" in the report and capture the result
                    findstr /C:"Severity: HIGH" bandit_report.txt > high_severity.txt
                    
                    REM Check if any high severity issues were found
                    if %errorlevel% equ 0 (
                        echo ========================================
                        echo ❌ HIGH SEVERITY ISSUES FOUND!
                        echo ========================================
                        type high_severity.txt
                        echo.
                        echo Pipeline will FAIL due to high severity issues
                        exit /b 1
                    ) else (
                        echo ========================================
                        echo ✅ No high severity issues found!
                        echo ========================================
                        
                        REM Show summary of all issues
                        echo Bandit scan complete. No high severity issues.
                        findstr /C:"Code scanned:" bandit_report.txt
                        findstr /C:"Issues found:" bandit_report.txt
                        exit /b 0
                    )
                '''
            }
            post {
                always {
                    echo 'Archiving Bandit report...'
                    archiveArtifacts artifacts: 'bandit_report.txt, high_severity.txt', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        success {
            echo '✅ Pipeline completed successfully - No high severity issues found!'
        }
        failure {
            echo '❌ Pipeline failed - High severity security issues detected!'
        }
    }
}
