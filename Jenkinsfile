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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install bandit cdxgen
                '''
            }
        }
        
        stage('Security Scan with Bandit') {
            steps {
                sh '''
                    . venv/bin/activate
                    bandit -r . -f html -o bandit_report.html || true
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
                sh '''
                    . venv/bin/activate
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
                script {
                    // This is the correct docker.build syntax
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
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