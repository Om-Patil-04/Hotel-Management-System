pipeline {
    agent any

    environment {
        GCP_PROJECT = "mlops-new-447207"
        IMAGE_NAME  = "ml-project"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/data-guru0/MLOPS-COURSE-PROJECT-1.git'
                    ]]
                )
            }
        }

        stage('Build & Push Docker Image (GCR)') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh '''
                        set -e
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account \
                          --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker gcr.io --quiet

                        docker build \
                          --pull \
                          -t gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest .

                        docker push gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh '''
                        set -e
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account \
                          --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ${IMAGE_NAME} \
                          --image gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest \
                          --platform managed \
                          --region us-central1 \
                          --allow-unauthenticated
                    '''
                }
            }
        }
    }
}
