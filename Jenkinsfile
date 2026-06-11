pipeline {
    agent any
    options {
        timeout(time: 15, unit: 'MINUTES')
    }
    stages {
        stage('拉取代码') {
            steps { checkout scm }
        }
        stage('执行测试并生成 Allure 数据') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    powershell('''
                        pip install allure-pytest
                        $env:PYTHONPATH = "$env:WORKSPACE"
                        Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue
                        pytest --alluredir=allure-results --clean-alluredir   // 去掉 --maxfail=1
                    ''')
                }
            }
        }
    }
    post {
        always {
            script {
                // 无论测试成功或失败都尝试生成报告
                bat '''
                    if exist allure-report rmdir /s /q allure-report
                    allure generate allure-results --clean -o allure-report
                '''
                publishHTML([
                    reportDir: 'allure-report',
                    reportFiles: 'index.html',
                    reportName: 'Allure Report',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: true
                ])
                // junit 如果没有文件可加入条件判断
                junit allowEmptyResults: true, testResults: 'test-results.xml'
            }
        }
    }
}
