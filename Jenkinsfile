pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('执行测试') {
            steps {
                // 1. 切换到当前工作区（Jenkins 自动设置的变量）
                dir(env.WORKSPACE) {
                    // 2. 删除所有 __pycache__ 和 .pyc 文件（避免 import 冲突）
                    bat '''
                        for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
                        del /s /q *.pyc 2>nul
                    '''
                    
                    // 3. 禁用 Python 写入字节码（可选）
                    withEnv(['PYTHONDONTWRITEBYTECODE=1']) {
                        // 4. 执行 pytest（只针对当前项目目录）
                          bat 'where pytest'
                          bat 'python -c "import pytest; print(pytest.__version__)"'
                          bat 'dir'
                          bat 'pytest --collect-only'
                    }
                }
            }
        }
    }
}
