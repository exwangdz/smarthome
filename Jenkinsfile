pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('安装依赖') {
            steps {
                bat '''
                    cd %WORKSPACE%
                '''
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
                    // 解析 JUnit 格式的测试报告，在 Jenkins 界面展示测试趋势
                    junit 'test-reports/junit.xml'

                    // 发布 HTML 报告（需要安装 HTML Publisher Plugin）
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
            // 可选：清理工作空间，节省磁盘空间
            cleanWs()
        }
    }
}
