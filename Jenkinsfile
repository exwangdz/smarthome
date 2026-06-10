pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

       stage('执行测试用例') {
    steps {
        bat '''
            cd %WORKSPACE%
            echo "Current directory: %CD%"
            echo "Python version:"
            python --version
            echo "pytest location:"
            where pytest
            echo "pytest version:"
            pytest --version
            echo "Collecting tests without running:"
            pytest testcases/ --collect-only
        '''
    }
}
