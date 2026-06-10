pipeline {
    agent any

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

        stage('生成 Allure 报告') {
            steps {
                allure tool: 'allure', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
        }
        success {
            echo 'Allure 报告已生成，请查看左侧菜单'
        }
    }
}
