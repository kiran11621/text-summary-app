pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'text-summary-app'
        DOCKER_TAG = 'latest'
    }

    stages {
        stage('Email Notification') {
            steps {
                emailext(
                    to: 'kiran11621@gmail.com',
                    subject: "📧 Test Email from Jenkins Pipeline",
                    body: """\
Hi Kiran,

This is a test email triggered at the start of the Jenkins pipeline to verify email configuration.

- Jenkins
                    """
                )
            }
        }

        stage('Clone') {
            steps {
                git branch: 'docker-deploy', url: 'https://github.com/kiran11621/text-summary-app.git'
            }
        }

        // stage('Secrets Scan (GitLeaks)') {
        //     steps {
        //         echo 'Running Gitleaks Scan using Docker...'
        //         bat """ 
        //           docker run --rm -v %WORKSPACE%:/repo zricethezav/gitleaks:latest detect --source=/repo --no-git --config=/repo/.gitleaks.toml --redact --verbose 
        //         """
        //     }
        // }
        // stage('Secrets Scan (GitLeaks)') {
        //     steps {
        //         bat 'dir %WORKSPACE%' // optional debug
        //         bat """
        //             docker run --rm -v "%WORKSPACE%:/repo" zricethezav/gitleaks:latest detect --source=/repo --no-git --config=/repo/.gitleaks.toml --redact --verbose
        //         """
        //     }
        // }
        stage('Secrets Scan (GitLeaks)') {
            steps {
                echo 'Running Gitleaks Scan using Docker...'
                bat """ 
                  docker run --rm -v %WORKSPACE%:/repo zricethezav/gitleaks:latest detect --source=/repo --no-git --config=/repo/.gitleaks.toml --redact --verbose 
                """
            }
        }

        stage('Unit & Function Tests') {
            steps {
                echo 'Running basic unit and function tests...'
                bat """
                    C:\\Users\\kiran\\AppData\\Local\\Programs\\Python\\Python39\\python.exe -m pip install --upgrade pip
                    C:\\Users\\kiran\\AppData\\Local\\Programs\\Python\\Python39\\python.exe -m pip install -r requirements.txt
                    C:\\Users\\kiran\\AppData\\Local\\Programs\\Python\\Python39\\python.exe -m pip install pytest
                    C:\\Users\\kiran\\AppData\\Local\\Programs\\Python\\Python39\\python.exe -m pytest tests/
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Docker Image Scan (Trivy)') {
            steps {
                echo 'Scanning Docker image for vulnerabilities...'
                bat """
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image ${DOCKER_IMAGE}:${DOCKER_TAG}
                """
            }
        }

        stage('Manual Approval') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    input message: 'Approve deployment?', ok: 'Deploy'
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    bat 'docker rm -f text-summary-container || exit 0'
                    bat "docker run -d --name text-summary-container -p 5000:5000 %DOCKER_IMAGE%:%DOCKER_TAG%"
                }
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'Running smoke test to verify the Flask app is live...'
                bat """
                    timeout /t 5 >nul
                    curl -s -o nul -w %%{http_code} http://localhost:5000 > status.txt
                    set /p STATUS_CODE=<status.txt
                    if NOT %%STATUS_CODE%%==200 (
                        echo Smoke test failed with HTTP status: %%STATUS_CODE%%
                        exit /b 1
                    )
                    echo Smoke test passed! App is responding with HTTP 200.
                """
            }
        }

    }

    post {
        success {
            echo '✅ Build, scan, and deploy successful!'
            emailext(
                to: 'kiran11621@gmail.com',
                subject: "✅ ${env.JOB_NAME} - Build #${env.BUILD_NUMBER} SUCCESS",
                body: """\
Hi Kiran,

The Jenkins job *${env.JOB_NAME}* (Build #${env.BUILD_NUMBER}) has completed successfully. ✅

View logs and details: ${env.BUILD_URL}

- Jenkins
                """
            )
        }
        failure {
            echo '❌ Something failed. Check logs.'
            emailext(
                to: 'kiran11621@gmail.com',
                subject: "❌ ${env.JOB_NAME} - Build #${env.BUILD_NUMBER} FAILED",
                body: """\
Hi Kiran,

The Jenkins job *${env.JOB_NAME}* (Build #${env.BUILD_NUMBER}) has failed. ❌

View logs and details: ${env.BUILD_URL}

- Jenkins
                """
            )
        }
    }
}
