pipeline {
    agent none

    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.9-slim'
                }
            }
            steps {
                sh 'python -m venv venv'
                sh 'pip install -r requirements.txt'
                sh 'pytest --junit-xml test-reports/results.xml'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
                failure {
                    mail to: derpy.hooves.ru@gmail.com, subject: 'Test failed'
                }
            }
        }
    }
}