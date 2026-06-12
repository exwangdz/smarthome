pipeline {
    agent any
    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }
stage('执行测试') {
    options {
        timeout(time: 5, unit: 'MINUTES')
    }
    steps {
        bat 'where pytest'                // 看能否找到 pytest
        bat 'python -c "import pytest; print(pytest.__version__)"'
        bat 'dir'                        // 确认代码文件已拉取
        bat 'pytest --collect-only'      // 只收集用例，不执行
    }
}
