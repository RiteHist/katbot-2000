pipeline {
    agent none

    stages {
        stage('Tests') {
            agent {
                docker {
                    image 'python:3.9-alpine'
                }
            }
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install -r requirements.txt --user'
                    sh 'pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-isort'
                    sh 'python -m flake8'
                    sh 'python -m pytest --junit-xml test-reports/results.xml'
                }
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deploy') {
            agent { label 'main' }
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d --build'
            }
        }
    }
}