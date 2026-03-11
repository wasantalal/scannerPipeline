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
        
        stage('Setup Tools') {
            steps {
                bat '''
                    echo Setting up Python environment...
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install bandit
                    
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
