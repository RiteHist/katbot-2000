pipeline {
    agent none
    environment {
        HOME = "${env.WORKSPACE}"
    }
    stages {
        stage('Quality Tests') {
            agent {
                docker {
                    label 'docker'
                    image 'python:3.9-alpine'
                }
            }
            steps {
                sh 'pip install --user -r requirements.txt'
                sh 'pip install flake8 pep8-naming flake8-broken-line flake8-return'
                sh "python -m flake8 --exit-zero src/ --output-file=test-reports/flake8.txt"
            }
            post {
                always {
                    recordIssues(tools: [flake8(pattern: 'test-reports/flake8.txt')])
                }
                cleanup {
                    cleanWs()
                }
            }
        }
        stage('Unit Tests') {
            agent {
                docker {
                    label 'docker'
                    image 'python:3.9-alpine'
                }
            }
            steps {
                sh 'pip install -r requirements.txt --user'
                sh 'python -m pytest --junit-xml test-reports/pytest_results.xml'
            }
            post {
                always {
                    junit 'test-reports/pytest_results.xml'
                }
                cleanup {
                    cleanWs()
                }
            }
        }
        stage('Deploy') {
            agent {
                node {
                    label 'prod'
                    customWorkspace '/home/ritehist/katbot-2000'
                }
            }
            steps {
                sh 'cp ../important/.env .'
                sh 'docker compose down'
                sh 'docker compose up -d --build'
            }
        }
    }
}
