pipeline {
    agent any

    environment {
        GCP_PROJECT = 'tough-bindery-483312-t2'
        REGION      = 'asia-south1'
        REPO        = 'docker-repo'
        IMAGE       = 'hotel-management-system'
    }

    stages {
        stage('Build & Push Docker Image') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh '''
                        set -e

                        gcloud auth activate-service-account \
                          --key-file=$GOOGLE_APPLICATION_CREDENTIALS

                        gcloud config set project $GCP_PROJECT

                        gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

                        docker build -t ${REGION}-docker.pkg.dev/${GCP_PROJECT}/${REPO}/${IMAGE}:latest .

                        docker push ${REGION}-docker.pkg.dev/${GCP_PROJECT}/${REPO}/${IMAGE}:latest
                    '''
                }
            }
        }
    }
}