pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/Hars7hitha/NotesMind'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t notes-app .'
            }
        }

        stage('Run Docker') {
            steps {
                sh 'docker run -d -p 5000:5000 notes-app'
            }
        }
    }
}