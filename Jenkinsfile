pipeline {
    agent any

    options {
        skipDefaultCheckout()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'assignment3-site'
        STAGING_PORT = '8091'
        PROD_PORT = '8081'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker rm -f assignment3-staging || true
                    docker run -d --name assignment3-staging -p 127.0.0.1:${STAGING_PORT}:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 3
                    curl -sf http://localhost:${STAGING_PORT}/ > /dev/null
                '''
            }
        }

        stage('Test') {
            agent {
                dockerfile {
                    dir 'tests'
                    args '--network host'
                    reuseNode true
                }
            }

            environment {
                HOME = '/tmp'
                BASE_URL = "http://localhost:${STAGING_PORT}"
            }

            steps {
                sh 'rm -f screenshot.png test-results.xml'
                sh 'pytest tests/test_site.py -v --junitxml=test-results.xml'
            }

            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'screenshot.png', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'All tests passed. Deploying assignment website.'
                sh '''
                    docker rm -f assignment3-prod || true
                    docker run -d --name assignment3-prod --restart unless-stopped -p ${PROD_PORT}:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 2
                    curl -sf http://localhost:${PROD_PORT}/ > /dev/null
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f assignment3-staging || true'
        }

        success {
            echo 'Assignment website deployed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the failed stage.'
        }
    }
}
