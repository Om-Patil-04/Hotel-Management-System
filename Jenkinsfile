pipeline {
    agent any

    environment {
        GCP_PROJECT = 'tough-bindery-483312-t2'
        IMAGE       = 'hotel-management-system'
        REGION      = 'asia-south1'
        SERVICE     = 'hotel-management-system'
        ARTIFACT_REGISTRY = 'asia-south1-docker.pkg.dev/tough-bindery-483312-t2/hotel-management'
        SERVICE_ACCOUNT = 'om-patil@tough-bindery-483312-t2.iam.gserviceaccount.com'
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
                        gcloud auth configure-docker $REGION-docker.pkg.dev --quiet
                    '''
                }
            }
        }

        stage('Build & Push Image (Cloud Build)') {
            steps {
                sh '''
                    gcloud builds submit \
                      --config=cloudbuild.yaml \
                      --service-account=projects/$GCP_PROJECT/serviceAccounts/$SERVICE_ACCOUNT \
                      --project=$GCP_PROJECT \
                      .
                '''
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                sh '''
                    gcloud run deploy $SERVICE \
                      --image $ARTIFACT_REGISTRY/$IMAGE:latest \
                      --region $REGION \
                      --platform managed \
                      --allow-unauthenticated \
                      --port 8080 \
                      --service-account $SERVICE_ACCOUNT
                '''
            }
        }
    }
}