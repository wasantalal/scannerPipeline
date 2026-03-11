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
                    pip install bandit
                '''
            }
        }
        
        stage('Install Node.js and npm') {
            steps {
                bat '''
                    echo Checking if Node.js is installed...
                    node --version || (
                        echo Installing Node.js via chocolatey...
                        choco install nodejs -y
                        refreshenv
                    )
                '''
            }
        }
        
        stage('Install cdxgen') {
            steps {
                bat '''
                    echo Installing cdxgen via npm...
                    npm install -g @cyclonedx/cdxgen
                '''
            }
        }
        
        stage('Security Scan with Bandit') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    bandit -r . -f html -o bandit_report.html || exit 0
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit_report.html'
                }
            }
        }
        
        stage('Generate SBOM with cdxgen') {
            steps {
                bat '''
                    cdxgen -o bom.xml
                    cdxgen -o bom.json
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bom.xml, bom.json'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }
    }
    
    post {
        always {
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
