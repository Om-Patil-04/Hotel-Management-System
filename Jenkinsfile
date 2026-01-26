pipeline {
    agent any

    environment {
        GCP_PROJECT = 'tough-bindery-483312-t2'
        IMAGE_NAME  = "gcr.io/${GCP_PROJECT}/hotel-management-system"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'GitHub-Token',
                    url: 'https://github.com/Om-Patil-04/Hotel-Management-System.git'
            }
        }

        stage('Build & Push Docker Image to GCR') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh '''
                        set -e

                        gcloud auth activate-service-account \
                          --key-file="$GOOGLE_APPLICATION_CREDENTIALS"

                        gcloud config set project "$GCP_PROJECT"

                        gcloud auth configure-docker gcr.io --quiet

                        docker build -t $IMAGE_NAME:latest .
                        docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Docker image successfully pushed to GCR!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}