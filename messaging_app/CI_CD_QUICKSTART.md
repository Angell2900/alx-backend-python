# CI/CD Pipeline Quick Start

## Files Modified/Created

✅ **Jenkinsfile** - Complete Jenkins pipeline with all stages
✅ **.github/workflows/ci.yml** - GitHub Actions CI workflow
✅ **.github/workflows/dep.yml** - GitHub Actions CD workflow
✅ **conftest.py** - Updated pytest configuration
✅ **messaging/models.py** - Created Message, MessageHistory, Notification models
✅ **tests/__init__.py** - Created test package initialization
✅ **CI_CD_SETUP.md** - Comprehensive setup documentation

## Quick Setup Checklist

### 1. Prerequisites
- [ ] Docker installed
- [ ] Docker Hub account
- [ ] GitHub account
- [ ] Python 3.10+
- [ ] Git installed

### 2. GitHub Repository Setup
- [ ] Push code to GitHub
- [ ] Go to Settings → Secrets and variables → Actions
- [ ] Add `DOCKER_USERNAME` secret
- [ ] Add `DOCKER_PASSWORD` secret

### 3. GitHub Actions Verification
- [ ] Go to Actions tab in repository
- [ ] Verify workflows are visible:
  - [ ] CI - Testing & Code Quality
  - [ ] CD - Build & Deploy Docker
- [ ] Trigger a push to main branch
- [ ] Watch workflows execute

### 4. Jenkins Setup (Optional)
- [ ] Start Jenkins: `docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts`
- [ ] Access http://localhost:8080
- [ ] Install plugins: Git, Pipeline, HTML Publisher
- [ ] Configure GitHub credentials
- [ ] Configure Docker Hub credentials
- [ ] Create pipeline job from Jenkinsfile
- [ ] Trigger build manually

### 5. Run Tests Locally
```bash
cd messaging_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ --cov=. --cov-report=html -v
```

### 6. Docker Build (Optional)
```bash
cd messaging_app
docker build -t angell2900/messaging-app:latest .
docker run -d -p 8000:8000 angell2900/messaging-app:latest
```

## Pipeline Overview

### CI Pipeline (ci.yml)
**Triggers:** Push to main/develop, Pull Requests
**Steps:**
1. Checkout code
2. Set up Python 3.10
3. Wait for MySQL
4. Install dependencies
5. Run flake8 linting
6. Run migrations
7. Execute tests with coverage
8. Upload reports

**Duration:** ~5 minutes

### CD Pipeline (dep.yml)
**Triggers:** Push to main branch
**Steps:**
1. Checkout code
2. Set up Docker Buildx
3. Log in to Docker Hub
4. Build Docker image
5. Push to Docker Hub with tags
6. Notify deployment

**Duration:** ~3 minutes

### Jenkins Pipeline (Jenkinsfile)
**Triggers:** Manual or via GitHub webhook
**Stages:**
1. Checkout
2. Setup Python Environment
3. Install Dependencies
4. Run Linting
5. Run Tests & Coverage
6. Publish Test Reports
7. Build Docker Image
8. Push to Docker Hub
9. Cleanup

**Duration:** ~10 minutes

## Test Models

### Message Model
- Fields: sender, receiver, content, created_at, updated_at, read, parent_message
- Relations: Replies through parent_message
- Tests: Creation, string representation, reply functionality

### MessageHistory Model
- Fields: message, old_content, edited_by, edited_at
- Tracks message edits and revisions
- Tests: Creation, edit history

### Notification Model
- Fields: user, message, is_read, created_at
- Notifies users of received messages
- Tests: Creation, string representation

## Environment Variables

### For Local MySQL Testing
```bash
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=messaging_app_test
DATABASE_USER=test_user
DATABASE_PASSWORD=test_password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
SECRET_KEY=test-secret-key
DEBUG=False
```

### GitHub Actions (ci.yml)
Automatically sets these for MySQL tests

### Jenkins
Set in Jenkinsfile environment block or Jenkins credentials

## Docker Hub Tags

After successful push:
- `angell2900/messaging-app:main` - Latest from main branch
- `angell2900/messaging-app:abc1234` - Commit SHA (7 chars)
- `angell2900/messaging-app:20250101_120000` - Timestamp
- `angell2900/messaging-app:latest` - Latest overall

## Code Quality Standards

- **Flake8**: Max line length 127 chars
- **Coverage**: Tracked in HTML report
- **Tests**: All tests must pass
- **Linting**: Non-blocking but reported

## Monitoring

### GitHub Actions
- Repository → Actions tab
- Click workflow for detailed logs
- Check artifacts for reports

### Jenkins
- Jenkins dashboard at http://localhost:8080
- Build history and logs
- Test result trends

### Docker Hub
- https://hub.docker.com/
- View pushed images and tags
- Track build history

## Troubleshooting

### Tests Failing
1. Check test output in Actions/Jenkins logs
2. Run locally: `pytest tests/ -v`
3. Check database connectivity
4. Verify migrations run successfully

### Docker Push Failing
1. Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets
2. Check Docker Hub account permissions
3. Verify image name matches

### MySQL Connection Issues
1. Check wait loop in ci.yml
2. Verify port 3306 is available
3. Check credentials match service config

## Success Indicators

✅ GitHub Actions workflows appear in Actions tab
✅ Workflows run on push to main
✅ Tests pass with coverage reports
✅ Docker image builds and pushes
✅ Jenkins pipeline runs successfully
✅ Docker Hub has new images with correct tags

## Next Steps

1. **Monitor first workflow runs** - Check Actions tab
2. **Review test reports** - Download coverage HTML
3. **Verify Docker images** - Check Docker Hub
4. **Set up branch protection** - Require CI to pass
5. **Add deployment** - Integrate with your infrastructure

## Support

For detailed setup instructions, see: `CI_CD_SETUP.md`
