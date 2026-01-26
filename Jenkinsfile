pipeline {
    agent any

    environment {
        GCP_PROJECT = 'tough-bindery-483312-t2'
        IMAGE       = 'hotel-management-system'
        TAG         = "${env.BUILD_NUMBER}"
        REGION      = 'asia-south1'
        SERVICE     = 'hotel-management-system'
    }

    stages {
        stage('Build & Push Docker Image') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh '''
                        set -e

                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
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

        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh '''
                        set -e

                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project $GCP_PROJECT

                        gcloud run deploy $SERVICE \
                          --image gcr.io/$GCP_PROJECT/$IMAGE:$TAG \
                          --region $REGION \
                          --platform managed \
                          --allow-unauthenticated \
                          --service-account om-patil@tough-bindery-483312-t2.iam.gserviceaccount.com
                    '''
                }
            }
        }
    }
}
