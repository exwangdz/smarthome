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
                bat 'where pytest'
                bat 'python -c "import pytest; print(pytest.__version__)"'
                bat 'dir'
                bat 'pytest --collect-only'
            }
        }
    }
}
