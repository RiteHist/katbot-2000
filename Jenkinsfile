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
                    sh 'pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-isort flake8-junit-report'
                    sh 'python -m flake8 --output-file flake8.txt'
                    sh 'junit_conversor flake8.txt test-reports/flake8_junit.xml'
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