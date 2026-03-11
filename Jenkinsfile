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
            
            REM Run bandit and capture exit code
            bandit -r . -f txt -o bandit_report.txt
            
            REM Check Bandit's exit code directly
            if %errorlevel% equ 1 (
                echo ❌ Security issues found!
                type bandit_report.txt
                exit /b 1
            ) else (
                echo ✅ No security issues found!
                exit /b 0
            )
               '''
            }
            post {
                always {
                    echo 'Archiving Bandit reports...'
                    archiveArtifacts artifacts: 'bandit_report.txt, bandit_report.json', allowEmptyArchive: true
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
            echo '✅ Pipeline completed successfully - No security issues found!'
        }
        failure {
            echo '❌ Pipeline failed - Security issues detected!'
        }
    }
}
