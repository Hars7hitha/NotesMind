pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/Hars7hitha/NotesMind.git'
            }
        }
        stage('Build Docker') {
            steps {
                sh 'docker build -t notes-app .'
            }
        }
        stage('Run Docker') {
            steps {
                sh 'docker stop notes-app-container || true'
                sh 'docker rm notes-app-container || true'
                sh 'docker run -d -p 5000:5000 --name notes-app-container notes-app'
            }
        }
    }
}