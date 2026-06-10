pipeline {
    agent any
    stages {
        stage('拉取代码') {
            steps {
                withEnv(['http_proxy=', 'https_proxy=', 'HTTP_PROXY=', 'HTTPS_PROXY=']) {
                    checkout scm
                }  // 关闭 withEnv
            }  // 关闭 steps
        }  // 关闭 stage

        stage('执行测试用例') {
            steps {
                bat '''
                    cd %WORKSPACE%
                    if not exist "test-reports" mkdir test-reports
                    pytest testcases/ --junitxml=test-reports/junit.xml --html=test-reports/report.html --self-contained-html
                '''
            }  // 关闭 steps
            post {
                always {
                    junit 'test-reports/junit.xml'
                    publishHTML([
                        reportDir: 'test-reports',
                        reportFiles: 'report.html',
                        reportName: 'Pytest HTML Report'
                    ])
                }  // 关闭 always
            }  // 关闭 post
        }  // 关闭 stage
    }  // 关闭 stages

    post {
        always {
            cleanWs()
        }  // 关闭 always
    }  // 关闭 pipeline 的 post
}  // 关闭 pipeline
