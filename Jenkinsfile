pipeline {
    agent any

    environment {
        GCP_PROJECT = 'tough-bindery-483312-t2'
        IMAGE       = 'hotel-management-system'
        TAG         = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build & Push Docker Image (FAST)') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh '''
                        set -e

                        gcloud auth activate-service-account \
                          --key-file=$GOOGLE_APPLICATION_CREDENTIALS

                        gcloud config set project $GCP_PROJECT

                        gcloud auth configure-docker --quiet

                        docker pull gcr.io/$GCP_PROJECT/$IMAGE:latest || true

                        docker build \
                          --cache-from gcr.io/$GCP_PROJECT/$IMAGE:latest \
                          -t gcr.io/$GCP_PROJECT/$IMAGE:$TAG \
                          -t gcr.io/$GCP_PROJECT/$IMAGE:latest .

                        docker push gcr.io/$GCP_PROJECT/$IMAGE:$TAG
                        docker push gcr.io/$GCP_PROJECT/$IMAGE:latest
                    '''
                }
            }
        }
    }
}
