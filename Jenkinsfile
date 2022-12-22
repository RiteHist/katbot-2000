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
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'python -m venv venv'
                    sh '. venv/bin/activate'
                    sh 'pip install -r requirements.txt'
                    sh 'pytest --junit-xml test-reports/results.xml'
                }
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}