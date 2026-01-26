pipeline{
    agent any

    environment {
        VENV_DIR    = 'venv'
        GCP_PROJECT = 'tough-bindery-483312-t2'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'GitHub-Token',
                    url: 'https://github.com/Om-Patil-04/Hotel-Management-System.git'
            }
        }

        stage('Setup Virtual Environment & Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip setuptools
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build & Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        gcloud --version

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

                        docker build -t ${REGION}-docker.pkg.dev/${GCP_PROJECT}/${REPO}/${IMAGE}:latest .

                        docker build -t gcr.io/${GCP_PROJECT}/hotel-management-system:latest .
                        docker push gcr.io/${GCP_PROJECT}/hotel-management-system:latest
                    '''
                }
            }
        }
    }
}
