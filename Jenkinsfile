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
                // 检查 allure-results 目录是否存在且非空（通过检查是否有 .json 文件）
                def hasResults = false
                if (fileExists('allure-results')) {
                    // 使用 bat 检查是否有 .json 文件，结果存入文件
                    bat(script: '@echo off & if exist allure-results\\*.json (echo 1) else (echo 0)', returnStdout: true).trim() == '1'
                    // 注意：上面这行会返回 true/false，但更可靠的方式如下：
                    def checkCmd = bat(script: 'if exist allure-results\\*.json (echo 1) else (echo 0)', returnStdout: true).trim()
                    hasResults = (checkCmd == '1')
                }
                
                if (hasResults) {
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
                } else {
                    echo "No allure-results or no JSON files found, skipping report generation."
                }
                
                // JUnit 报告，允许缺失
                junit allowEmptyResults: true, testResults: 'test-results.xml'
            }
        }
    }
}
