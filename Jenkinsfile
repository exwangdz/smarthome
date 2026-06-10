pipeline {
    agent any

    options {
        timeout(time: 10, unit: 'MINUTES')
    }

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('执行测试并生成 Allure 结果') {
            steps {
                powershell('''
                    # 设置 PYTHONPATH
                    $env:PYTHONPATH = "$env:WORKSPACE"
                    
                    # 创建 allure 结果目录
                    New-Item -ItemType Directory -Force -Path "allure-results"
                    
                    # 运行 pytest，生成 allure 原始数据
                    pytest --alluredir=allure-results --clean-alluredir --maxfail=1 --tb=short
                ''')
            }
        }

        stage('生成并发布 Allure 报告') {
            steps {
                // 使用 allure 插件生成报告
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
            post {
                always {
                    // 可选：同时保留 JUnit 报告作为备份
                    junit 'test-results.xml'
                }
            }
        }
    }

    post {
        always {
            echo '构建结束'
        }
        success {
            echo '测试通过，Allure 报告已生成'
        }
        failure {
            echo '构建失败'
        }
    }
}
