pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'phi2-app'
        DOCKER_TAG = 'v1'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install bandit
                '''
            }
        }
        
        stage('Install cdxgen') {
            steps {
                bat '''
                    echo Installing cdxgen via winget...
                    winget install --id=CycloneDX.cdxgen -e --silent --accept-package-agreements
                    
                    echo Copying cdxgen to current directory...
                    for /f "tokens=*" %%i in ('where cdxgen') do copy "%%i" cdxgen.exe
                    
                    echo Verification:
                    cdxgen.exe --version
                '''
            }
        }
        
        stage('Security Scan') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    bandit -r . -f html -o bandit_report.html || exit 0
                '''
            }
            post {
                always {
                    archiveArtifacts 'bandit_report.html'
                }
            }
        }
        
        stage('Generate SBOM') {
            steps {
                bat '''
                    cdxgen.exe -o bom.xml
                    cdxgen.exe -o bom.json
                '''
            }
            post {
                always {
                    archiveArtifacts 'bom.xml, bom.json'
                }
            }
        }
        
        stage('Build Docker') {
            steps {
                bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
