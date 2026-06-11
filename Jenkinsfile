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
                        # 调试：列出测试文件
                        Write-Host "=== Test files in testcases ==="
                        Get-ChildItem -Path ./testcases -Recurse -Filter "*.py" | Select-Object FullName
                        pytest --alluredir=allure-results --clean-alluredir --maxfail=1
                    ''')
                }
            }
        }
    }
    post {
        always {
            script {
                if (fileExists('allure-results')) {
                    dir('allure-results') {
                        def files = findFiles(glob: '*.json')
                        if (files.size() > 0) {
                            bat 'if exist allure-report rmdir /s /q allure-report'
                            def allureHome = tool name: 'allure', type: 'hudson.plugins.allure.AllureInstallation'
                            bat "${allureHome}\\bin\\allure generate allure-results --clean -o allure-report"
                            publishHTML([
                                reportDir: 'allure-report',
                                reportFiles: 'index.html',
                                reportName: 'Allure Report',
                                keepAll: true,
                                alwaysLinkToLastBuild: true,
                                allowMissing: true
                            ])
                        } else {
                            echo "No JSON files in allure-results, skipping report."
                        }
                    }
                } else {
                    echo "allure-results directory does not exist."
                }
                junit allowEmptyResults: true, testResults: 'test-results.xml'
            }
        }
    }
}
