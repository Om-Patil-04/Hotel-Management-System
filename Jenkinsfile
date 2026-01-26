pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${env.BRANCH_NAME ?: 'master'}"]],
                    userRemoteConfigs: [[
                        credentialsId: 'GitHub-Token',
                        url: 'https://github.com/Om-Patil-04/Hotel-Management-System.git'
                    ]]
                ])
            }
        }
    }
}
