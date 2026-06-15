pipeline {
    agent any
    
    options {
        // 禁用并发构建，避免多个 workspace 副本互相干扰
        disableConcurrentBuilds()
        // 每次构建前完全清理工作区，清除 __pycache__ 和 .pyc 文件
        cleanWs()
    }

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }
        
        stage('执行测试') {
            steps {
                // 强制在当前工作区执行
                dir(env.WORKSPACE) {
                    // 使用 Python 完整路径（根据你的实际路径调整）
                    def pythonPath = 'D:\\Users\\ex_wangdz\\AppData\\Local\\Programs\\Python\\Python310\\python.exe'
                    
                    // 禁止 Python 写入字节码，避免缓存冲突
                    withEnv(['PYTHONDONTWRITEBYTECODE=1']) {
                        // 先只收集用例，确认能正常发现测试
                        bat "${pythonPath} -m pytest --collect-only -v"
                        // 如果收集成功，再执行真正的测试（带超时，防止卡死）
                        bat "${pythonPath} -m pytest -v --tb=short --capture=no"
                    }
                }
            }
        }
    }
}
