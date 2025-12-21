# CI/CD Pipeline Setup Guide

## Overview

This document provides complete setup instructions for the Jenkins and GitHub Actions CI/CD pipeline for the Django messaging application.

## Project Structure

```
messaging_app/
├── Jenkinsfile                          # Jenkins pipeline configuration
├── .github/
│   └── workflows/
│       ├── ci.yml                       # GitHub Actions - Testing & Code Quality
│       └── dep.yml                      # GitHub Actions - Docker Build & Deploy
├── config/
│   └── settings.py                      # Django settings
├── messaging/
│   ├── models.py                        # Message, MessageHistory, Notification models
│   ├── views.py
│   ├── admin.py
│   └── migrations/
├── tests/
│   ├── __init__.py
│   └── test_models.py                   # Test cases for models
├── conftest.py                          # pytest configuration
├── pytest.ini                           # pytest configuration
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Docker containerization
├── manage.py                            # Django management script
└── .flake8                              # Flake8 linting configuration
```

## 1. Jenkins Setup

### Prerequisites
- Docker installed
- Docker Hub account
- GitHub account with repository access

### Installation

1. **Start Jenkins in Docker:**

```bash
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

2. **Access Jenkins Dashboard:**
   - Navigate to `http://localhost:8080`
   - Retrieve initial admin password: `docker logs jenkins | grep "Initial Admin Password"`
   - Complete setup wizard

3. **Install Required Plugins:**
   - Go to Manage Jenkins → Manage Plugins
   - Search for and install:
     - Git
     - Pipeline
     - HTML Publisher
     - Cobertura Plugin
     - AnsiColor Plugin

4. **Configure Credentials:**

   **GitHub Credentials:**
   - Manage Jenkins → Manage Credentials
   - Click "Store" → "Jenkins" → "Global credentials"
   - Click "Add Credentials"
   - Type: Username with password
   - Username: Your GitHub username
   - Password: Your GitHub personal access token
   - ID: `github-credentials`

   **Docker Hub Credentials:**
   - Repeat above steps
   - Type: Username with password
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password/token
   - ID: `dockerhub-credentials`

5. **Create Jenkins Pipeline Job:**
   - New Item → Pipeline
   - Name: `messaging-app-pipeline`
   - Pipeline → Definition: `Pipeline script from SCM`
   - SCM: Git
   - Repository URL: `https://github.com/YOUR_USERNAME/alx-backend-python.git`
   - Credentials: Select `github-credentials`
   - Script Path: `messaging_app/Jenkinsfile`
   - Save and click "Build Now"

## 2. GitHub Actions Setup

### Prerequisites
- GitHub repository
- GitHub Secrets configured
- Docker Hub account

### Configuration

#### Step 1: Set GitHub Secrets

Navigate to your repository → Settings → Secrets and variables → Actions

Add the following secrets:

1. **DOCKER_USERNAME**
   - Value: Your Docker Hub username

2. **DOCKER_PASSWORD**
   - Value: Your Docker Hub access token (or password)

#### Step 2: Workflow Files

The following files should exist in `.github/workflows/`:

- **ci.yml** - Runs tests and code quality checks on every push/PR
- **dep.yml** - Builds and pushes Docker image on main branch push

### Workflows Explanation

#### CI Workflow (ci.yml)

Triggers on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

Jobs:
1. **Test Job**
   - Sets up MySQL 8.0 service
   - Installs Python dependencies
   - Runs flake8 linting (non-blocking)
   - Runs Django migrations
   - Executes pytest with coverage
   - Uploads coverage and test reports

#### CD Workflow (dep.yml)

Triggers on:
- Push to `main` branch
- Manual trigger via `workflow_dispatch`

Jobs:
1. **Build and Push Job**
   - Logs into Docker Hub
   - Builds Docker image
   - Pushes to Docker Hub with tags:
     - `branch` (e.g., `main`)
     - `sha` (first 7 characters of commit)
     - `timestamp` (build timestamp)
     - `latest`

## 3. Testing Configuration

### Test Discovery

Tests are automatically discovered in the `tests/` directory matching patterns:
- `test_*.py`
- `*_tests.py`
- Classes matching `Test*`
- Functions matching `test_*`

### Running Tests Locally

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest tests/ \
  --cov=. \
  --cov-report=html:htmlcov \
  --cov-report=xml:coverage.xml \
  -v

# Run linting
flake8 . --config=.flake8
```

### Test Models

The `tests/test_models.py` file tests three main models:

1. **Message Model**
   - Creation with sender, receiver, content
   - String representation
   - Reply functionality (parent_message)

2. **MessageHistory Model**
   - Tracking message edits
   - Edit metadata (who, when)

3. **Notification Model**
   - User notifications for messages
   - Read/unread status
   - Ordering by creation date

## 4. Docker Configuration

### Dockerfile

The Dockerfile:
- Uses `python:3.10-slim` base image
- Installs required system dependencies
- Installs Python packages from requirements.txt
- Exposes port 8000
- Runs gunicorn with 4 workers

### Building Locally

```bash
cd messaging_app
docker build -t angell2900/messaging-app:latest .
docker run -d -p 8000:8000 angell2900/messaging-app:latest
```

## 5. Code Quality

### Flake8 Configuration

The `.flake8` file configures:
- Max line length: 127 characters
- Excluded directories: git, pycache, venv, migrations
- Ignored rules: E203, E266, W503
- Per-file ignores for __init__.py and tests

### Coverage Requirements

The pipeline generates coverage reports:
- HTML report: `htmlcov/index.html`
- XML report: `coverage.xml`
- Terminal output with coverage percentage

## 6. Troubleshooting

### Common Issues

**Jenkins:**
- "Pipeline execution failed"
  - Check logs in Jenkins UI
  - Verify credentials are correctly set
  - Ensure messaging_app directory exists
  - Verify Docker is running

- "Test reports not found"
  - Run tests with correct flags
  - Verify pytest is installed
  - Check DJANGO_SETTINGS_MODULE is set

**GitHub Actions:**
- "MySQL connection failed"
  - Check health check configuration
  - Ensure sufficient wait time
  - Verify environment variables
  - Check database credentials

- "Docker push failed"
  - Verify Docker credentials are correct
  - Check Docker Hub account permissions
  - Ensure image name matches repository

**Tests:**
- "ModuleNotFoundError"
  - Run pip install -r requirements.txt
  - Check PYTHONPATH includes project root
  - Verify conftest.py is in project root

- "Database errors"
  - Ensure MySQL service is running
  - Check database credentials
  - Run migrations before tests
  - Verify DATABASE_* environment variables

## 7. Repository Secrets Setup Checklist

```
✓ DOCKER_USERNAME      - Docker Hub username
✓ DOCKER_PASSWORD      - Docker Hub token/password
✓ GitHub credentials   - Personal access token (for Jenkins)
```

## 8. Environment Variables Required

For local testing with MySQL:

```bash
export DATABASE_ENGINE=django.db.backends.mysql
export DATABASE_NAME=messaging_app_test
export DATABASE_USER=test_user
export DATABASE_PASSWORD=test_password
export DATABASE_HOST=127.0.0.1
export DATABASE_PORT=3306
export SECRET_KEY=test-secret-key-for-ci
export DEBUG=False
```

## 9. Monitoring & Logs

### Jenkins Logs
- Navigate to job → Build → Console Output
- Check for errors and warnings

### GitHub Actions Logs
- Navigate to repository → Actions
- Click on workflow run
- Expand job details
- View step logs

### Docker Hub
- Monitor image pushes at https://hub.docker.com/
- Check image tags and build history

## 10. Next Steps

1. **Kubernetes Integration**
   - Deploy using Helm charts
   - Set up rolling updates
   - Configure auto-scaling

2. **Security Scanning**
   - Integrate Trivy for image scanning
   - Add Snyk for dependency checks
   - Implement SAST tools

3. **Monitoring & Alerts**
   - Set up Prometheus metrics
   - Configure email notifications
   - Integrate with Slack

4. **Performance Optimization**
   - Implement caching strategies
   - Optimize Docker image size
   - Profile database queries

## Support & Documentation

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest Documentation](https://docs.pytest.org/)
