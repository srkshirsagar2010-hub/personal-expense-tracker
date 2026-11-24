
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/srkshirsagar2010-hub/personal-expense-tracker.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt --break-system-packages'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t shrey2020/personal-expense-tracker:${BUILD_NUMBER} .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Docker Hub authentication will be configured next.'
            }
        }
    }
}
