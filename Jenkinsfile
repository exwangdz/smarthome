
pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('安装Python依赖') {
            steps {
                // 使用bat脚本（Windows环境）
                bat '''
                    cd %WORKSPACE%
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('执行测试用例') {
            steps {
                bat '''
                    cd %WORKSPACE%
                    python -m pytest tests/ --junitxml=test-reports/junit.xml --html=test-reports/report.html --self-contained-html
                '''
            }
            post {
                always {
                    // 收集JUnit格式的测试报告
                    junit 'test-reports/junit.xml'
                    
                    // 如果需要发布HTML报告（需安装HTML Publisher插件）
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
            // 清理工作空间（可选）
            cleanWs()
        }
    }
}
