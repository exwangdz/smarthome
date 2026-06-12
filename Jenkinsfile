pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }
        stage('执行测试') {
            steps {
                bat 'pytest'
            }
        }
    }
}
