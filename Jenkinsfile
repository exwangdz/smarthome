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

        stage('执行测试用例') {
            steps {
                powershell('''
                    $env:PYTHONPATH = "$env:WORKSPACE"
                    Write-Host "开始执行 pytest..."
                    pytest --junitxml=test-results.xml --maxfail=1 --tb=short
                ''')
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
    }

    post {
        always {
            echo '构建结束'
        }
        failure {
            echo '构建失败'
        }
        unstable {
            echo '存在测试失败用例'
        }
    }
}
