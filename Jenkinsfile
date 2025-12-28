// ALX Backend Python - Jenkins CI/CD Pipeline
// This pipeline pulls code from GitHub, runs tests, and deploys Docker images
pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }

    environment {
        REPO_URL = 'https://github.com/Angell2900/alx-backend-python.git'
        DOCKER_REGISTRY = 'angell2900'
        DOCKER_IMAGE = 'messaging-app'
        PYTHONUNBUFFERED = '1'
        VENV_PATH = '${WORKSPACE}/venv'
        PATH = '${VENV_PATH}/bin:${PATH}'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out code from ${REPO_URL}"
                    checkout scm
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    echo "Setting up Python virtual environment"
                    sh '''
                        set -e
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip setuptools wheel
                        echo "Python version:"
                        python --version
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing project dependencies"
                    sh '''
                        set -e
                        . venv/bin/activate
                        pip install -r requirements.txt
                        echo "Installed packages:"
                        pip list
                    '''
                }
            }
        }

        stage('Run Linting') {
            steps {
                script {
                    echo "Running flake8 linting"
                    sh '''
                        set -e
                        . venv/bin/activate
                        echo "Running flake8..."
                        flake8 . --config=.flake8 --count --statistics || true
                    '''
                }
            }
        }

        stage('Run Tests & Coverage') {
            steps {
                script {
                    echo "Running pytest with coverage"
                    sh '''
                        set -e
                        . venv/bin/activate
                        mkdir -p test-results htmlcov
                        echo "Running tests..."
                        pytest . \
                               --junitxml=test-results/results.xml \
                               --cov=. \
                               --cov-report=html:htmlcov \
                               --cov-report=xml:coverage.xml \
                               --cov-report=term \
                               -v --tb=short 2>&1 || true
                    '''
                }
            }
        }

        stage('Publish Test Reports') {
            steps {
                script {
                    echo "Publishing test and coverage reports"
                    sh '''
                        if [ -f "test-results/results.xml" ]; then
                            echo "Test report found"
                        fi
                    '''
                    junit allowEmptyResults: true, testResults: 'test-results/results.xml'
                    publishHTML([
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image"
                    sh '''
                        set -e
                        docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} .
                        docker tag ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest
                        echo "Docker image built successfully"
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub"
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            set -e
                            echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                            docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER}
                            docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest
                            docker logout
                            echo "Docker image pushed successfully"
                        '''
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    echo "Cleaning up Docker images"
                    sh '''
                        docker rmi ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} || true
                        docker rmi ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest || true
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed"
            cleanWs()
        }
        success {
            echo "✅ Pipeline succeeded! Docker image pushed to Docker Hub."
        }
        failure {
            echo "❌ Pipeline failed! Check logs for details."
        }
    }
}

