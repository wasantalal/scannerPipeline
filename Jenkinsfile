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
        
        stage('Security Scan with Bandit') {
            steps {
                bat '''
                    echo Running Bandit security scan...
                    call venv\\Scripts\\activate.bat
                    bandit -r . -f html -o bandit_report.html || (
                        echo Bandit found issues but continuing...
                        exit /b 0
                    )
                    echo Bandit scan complete!
                '''
            }
            post {
                always {
                    echo 'Archiving Bandit report...'
                    archiveArtifacts artifacts: 'bandit_report.html', allowEmptyArchive: true
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
