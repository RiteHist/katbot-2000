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
                sh 'pip install --target ${env.WORKSPACE} -r requirements.txt'
                sh 'pytest --junit-xml test-reports/results.xml'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}