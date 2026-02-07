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

        stage('Checkout Code') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/Om-Patil-04/Hotel-Management-System'
                    ]]
                )
            }
        }

        stage('Authenticate GCP') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh '''
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project $GCP_PROJECT
                        gcloud auth configure-docker --quiet
                    '''
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                sh '''
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

        stage('Deploy to Cloud Run') {
            steps {
                sh '''
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
