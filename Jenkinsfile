pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('执行测试用例') {
            steps {
                bat '''
                    cd %WORKSPACE%
                    if not exist "test-reports" mkdir test-reports
                    pytest testcases/ --junitxml=test-reports/junit.xml --html=test-reports/report.html --self-contained-html
                '''
            }
            post {
                always {
                    junit 'test-reports/junit.xml'
                    publishHTML([
                        reportDir: 'test-reports',
                        reportFiles: 'report.html',
                        reportName: 'Pytest HTML Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
