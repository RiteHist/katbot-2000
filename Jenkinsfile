pipeline {
    agent {
        docker {
            image 'python:3.9-alpine'
        }
    }

    stages {
        stage('Quality Tests') {
            steps {
                sh 'pip install -r requirements.txt --user'
                sh 'pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-junit-report'
                sh 'flake8 . --output-file=test-reports/flake8.txt'
                sh 'flake8_junit test-reports/flake8.txt test-reports/flake8_results.xml'
            }
        }
        stage('Unit Tests') {
            steps {
                sh 'pip install -r requirements.txt --user'
                sh 'python -m pytest --junit-xml test-reports/pytest_results.xml'
            }
        }
    }
    post {
        always {
            junit 'test-reports/results.xml'
        }
    }
}