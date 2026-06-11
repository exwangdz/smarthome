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
                powershell('''
                    pip install allure-pytest
                    $env:PYTHONPATH = "$env:WORKSPACE"
                    Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue
                    pytest --alluredir=allure-results --clean-alluredir --maxfail=1
                ''')
            }
        }

        stage('生成 Allure HTML 报告') {
            steps {
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
                    allowMissing: true       // 必须参数：报告文件不存在时不导致构建失败
                ])
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
        }
        success {
            echo 'Allure 报告已生成，请点击左侧 "Allure Report" 链接查看'
        }
    }
}
