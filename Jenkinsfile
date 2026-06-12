pipeline {
    agent any
    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }
        stage('执行测试') {
            options {
                timeout(time: 5, unit: 'MINUTES')
            }
            steps {
                bat 'echo "Current directory: %CD%"'
                bat 'dir'
                bat 'python --version'
                bat 'pytest --version'
                bat 'pytest -v --tb=short --capture=no'
            }
        }
    }
}
