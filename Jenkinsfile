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
            archiveArtifacts artifacts: 'bandit_report.txt', allowEmptyArchive: true
        }
    }
}
