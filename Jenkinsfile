pipeline {
    agent any
    
    environment {
        // Define Docker image name and tag
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
                    echo Setting up Python environment...
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install bandit
                    echo Python setup complete!
                '''
            }
        }
        
        stage('Download cdxgen') {
            steps {
                bat '''
                    echo Downloading cdxgen for Windows...
                    
                    REM Check if cdxgen.exe already exists
                    if exist cdxgen.exe (
                        echo cdxgen.exe already exists, skipping download...
                    ) else (
                        echo Downloading from GitHub releases...
                        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/CycloneDX/cdxgen/releases/latest/download/cdxgen-win.exe' -OutFile 'cdxgen.exe'"
                        
                        REM Verify download
                        if exist cdxgen.exe (
                            echo cdxgen.exe downloaded successfully!
                            dir cdxgen.exe
                        ) else (
                            echo Failed to download cdxgen.exe
                            exit /b 1
                        )
                    )
                '''
            }
        }
        
        stage('Verify cdxgen') {
            steps {
                bat '''
                    echo Verifying cdxgen installation...
                    .\\cdxgen.exe --version || (
                        echo Failed to run cdxgen
                        exit /b 1
                    )
                '''
            }
        }
        
        stage('Security Scan with Bandit') {
            steps {
                bat '''
                    echo Running Bandit security scan...
                    call venv\\Scripts\\activate.bat
                    bandit -r . -f html -o bandit_report.html || (
                        echo Bandit found issues but continuing...
                        exit /b 0
                    )
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit_report.html', allowEmptyArchive: true
                }
            }
        }
        
        stage('Generate SBOM with cdxgen') {
            steps {
                bat '''
                    echo Generating SBOM with cdxgen...
                    .\\cdxgen.exe -o bom.xml
                    .\\cdxgen.exe -o bom.json
                    echo SBOM generation complete!
                    
                    REM Verify files were created
                    dir bom.xml
                    dir bom.json
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bom.xml, bom.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                bat '''
                    echo Building Docker image...
                    docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% .
                    echo Docker build complete!
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
