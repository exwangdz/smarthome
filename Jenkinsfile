pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('执行测试并生成 Allure 数据') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    powershell('''
                        pip install allure-pytest
                        $env:PYTHONPATH = "$env:WORKSPACE"
                        Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue
                        pytest --alluredir=allure-results --clean-alluredir --maxfail=1
                    ''')
                }
            }
        }
    }

    post {
        always {
            script {
                // 只要 allure-results 目录存在，就尝试生成报告（不检查内部文件）
                if (fileExists('allure-results')) {
                    // 生成 Allure 报告，超时 3 分钟
                    timeout(time: 3, unit: 'MINUTES') {
                        bat '''
                            if exist allure-report rmdir /s /q allure-report
                            allure generate allure-results --clean -o allure-report
                        '''
                    }
                    // 发布 HTML 报告，超时 1 分钟
                    timeout(time: 1, unit: 'MINUTES') {
                        publishHTML([
                            reportDir: 'allure-report',
                            reportFiles: 'index.html',
                            reportName: 'Allure Report',
                            keepAll: false,          // 减少性能开销
                            alwaysLinkToLastBuild: true,
                            allowMissing: true
                        ])
                    }
                } else {
                    echo "allure-results directory not found, skipping report."
                }

                // JUnit 测试结果（如果有）
                junit allowEmptyResults: true, testResults: 'test-results.xml'
            }
        }
    }
}
