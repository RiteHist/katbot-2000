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
                    sh 'python -m pytest --junit-xml test-reports/pytest_results.xml'
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