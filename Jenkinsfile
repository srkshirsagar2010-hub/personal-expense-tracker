
pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'shrey2020/personal-expense-tracker'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m py_compile app.py'
                echo 'Python syntax check passed'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                    -t ${DOCKERHUB_REPO}:${BUILD_NUMBER} \
                    -t ${DOCKERHUB_REPO}:latest .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login \
                        -u "$DOCKERHUB_USER" --password-stdin

                        docker push ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                        docker push ${DOCKERHUB_REPO}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker stop expense-tracker || true
                    docker rm expense-tracker || true

                    docker run -d \
                    --name expense-tracker \
                    --restart unless-stopped \
                    -p 5000:5000 \
                    -v /home/victus/expense-tracker-data/expenses.db:/app/expenses.db \
                    ${DOCKERHUB_REPO}:latest
                '''
            }
        }
    }
}

