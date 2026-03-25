pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Hars7hitha/NotesMind.git'
            }
        }
        stage('Build Docker') {
            steps {
                bat 'docker build -t notes-app .'
            }
        }
        stage('Run Docker') {
            steps {
                bat 'docker stop notes-app-container || true'
                bat 'docker rm notes-app-container || true'
                bat 'docker run -d -p 5000:5000 --name notes-app-container notes-app'
            }
        }
    }
}