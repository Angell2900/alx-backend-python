# Jenkins Setup and Configuration Guide

## Status: Jenkins Container is Running ✅

Jenkins is already running on your system with the following configuration:
- **Container ID**: `dcbd7d3a6093`
- **Port**: `8080` (http://localhost:8080)
- **Jenkins Home**: Volume `jenkins_home`
- **Initial Admin Password**: `dd8dd7f187be4a0c9f9ceb3182d1e78a`

## Step 1: Access Jenkins Dashboard

1. Open your browser and navigate to: **http://localhost:8080**
2. You will see the Jenkins unlock page
3. Paste the initial admin password: `dd8dd7f187be4a0c9f9ceb3182d1e78a`
4. Click **Continue**

## Step 2: Install Suggested Plugins

1. You'll be prompted to "Customize Jenkins"
2. Click **"Install suggested plugins"**
3. Wait for all plugins to install (this may take a few minutes)

## Step 3: Create First Admin User

After plugins are installed:
1. Create an admin user with:
   - Username: `admin`
   - Password: (choose a secure password)
   - Full name: (your name or "Admin")
   - Email: (your email)
2. Click **Save and Continue**
3. Click **Save and Finish**

## Step 4: Install Additional Plugins

1. Go to **Manage Jenkins** → **Plugin Manager**
2. Go to the **"Available"** tab
3. Search for and install the following plugins:
   - **GitHub Integration Plugin** (for Git operations)
   - **Pipeline** (if not already installed)
   - **Pipeline: GitHub Integration** (optional, for GitHub PR integration)
   - **ShiningPanda Plugin** (for Python/Django support) - *Note: This is deprecated but may be referenced*

**Installation Steps**:
- Check the checkbox next to each plugin
- Click **"Download now and install after restart"**
- Check "Restart Jenkins when installation is complete"

## Step 5: Add GitHub Credentials

1. Go to **Manage Jenkins** → **Credentials**
2. Click **System** (on the left)
3. Click **Global credentials (unrestricted)**
4. Click **Add Credentials** (top left)
5. Fill in the form:
   - **Kind**: Username with password
   - **Scope**: Global
   - **Username**: `Angell2900` (your GitHub username)
   - **Password**: (your GitHub personal access token)
   - **ID**: `github-credentials`
   - **Description**: GitHub credentials for alx-backend-python
6. Click **Create**

### How to Generate a GitHub Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click **Generate new token**
3. Give it a name: `Jenkins CI`
4. Select scopes:
   - `repo` (full control of private repositories)
   - `workflow` (for Actions)
5. Click **Generate token**
6. Copy the token (you can only see it once!)
7. Use this token as the password in Jenkins credentials

## Step 6: Create a New Jenkins Pipeline Job

1. Click **New Item** on the left sidebar
2. Enter job name: `messaging-app-pipeline`
3. Select **Pipeline**
4. Click **OK**

## Step 7: Configure Pipeline Job

In the job configuration:

### General Tab:
- **Description**: Pipeline for ALX messaging app CI/CD

### Build Triggers:
- Check **GitHub hook trigger for GITScm polling**
- This allows GitHub to trigger builds on push

### Pipeline Section:
- **Definition**: Pipeline script from SCM
- **SCM**: Git
  - **Repository URL**: `https://github.com/Angell2900/alx-backend-python.git`
  - **Credentials**: Select `github-credentials`
  - **Branch Specifier**: `*/main`
- **Script Path**: `messaging_app/Jenkinsfile`
- Check **Lightweight checkout**

Click **Save**

## Step 8: Configure GitHub Webhook (Optional but Recommended)

1. Go to your GitHub repo: https://github.com/Angell2900/alx-backend-python
2. Go to **Settings** → **Webhooks**
3. Click **Add webhook**
4. **Payload URL**: `http://localhost:8080/github-webhook/` (note the trailing slash)
5. **Content type**: application/json
6. **Events**: Select "Push events" and "Pull request events"
7. Click **Add webhook**

## Step 9: Trigger the Pipeline

### Manual Trigger:
1. Go to Jenkins dashboard
2. Click on `messaging-app-pipeline` job
3. Click **Build Now** (on the left sidebar)
4. Monitor the build in the "Build History" on the left
5. Click on the build number to see logs

### Expected Build Output:
The pipeline will:
1. ✅ Checkout code from GitHub
2. ✅ Setup Python virtual environment
3. ✅ Install dependencies (including pytest, flake8)
4. ✅ Run flake8 linting
5. ✅ Run pytest with coverage
6. ✅ Publish test and coverage reports
7. ✅ Build Docker image
8. ✅ Push to Docker Hub (requires credentials)
9. ✅ Cleanup

## Step 10: Add Docker Hub Credentials (Optional)

For the Docker push stage to work:

1. In Jenkins, go to **Manage Jenkins** → **Credentials**
2. Click **System** → **Global credentials**
3. Click **Add Credentials**
4. Fill in:
   - **Kind**: Username with password
   - **Username**: Your Docker Hub username
   - **Password**: Your Docker Hub password (or access token)
   - **ID**: `dockerhub-credentials`
5. Click **Create**

## Troubleshooting

### Jenkins Not Responding
```bash
# Check if container is running
docker ps | grep jenkins

# Restart Jenkins
docker restart jenkins

# View logs
docker logs -f jenkins
```

### Build Fails with "Git not found"
- Git plugin should be installed automatically with suggested plugins
- If not, install **Git plugin** manually

### Build Fails with "Python not found"
- The Jenkins container has Python, but may need to be added to PATH
- Check the Jenkinsfile paths are correct

### Docker Commands Fail in Pipeline
- Jenkins container may not have Docker installed
- To enable Docker in Jenkins:
  ```bash
  docker exec jenkins apt-get update
  docker exec jenkins apt-get install -y docker.io
  ```

## Next Steps

After Jenkins is configured and working:

1. **Add GitHub Secrets** for Docker Hub credentials:
   - Go to https://github.com/Angell2900/alx-backend-python/settings/secrets/actions
   - Add `DOCKER_USERNAME` and `DOCKER_PASSWORD`

2. **Monitor GitHub Actions**:
   - Go to your repo → Actions tab
   - Watch CI and CD workflows execute on every push

3. **Verify Docker Image**:
   - Check Docker Hub at https://hub.docker.com/r/angell2900/messaging-app
   - Should see new images with tags: `main`, `latest`, `<sha>`, `<timestamp>`

## Files Reference

- **Jenkinsfile**: `messaging_app/Jenkinsfile`
- **CI Workflow**: `messaging_app/.github/workflows/ci.yml`
- **CD Workflow**: `messaging_app/.github/workflows/dep.yml`
- **Django App**: `messaging_app/`
- **Requirements**: `messaging_app/requirements.txt`
- **Tests**: `messaging_app/tests/`

## Commands Quick Reference

```bash
# Check Jenkins status
docker ps | grep jenkins

# View Jenkins logs
docker logs -f jenkins

# Access Jenkins container
docker exec -it jenkins bash

# Get Jenkins admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Restart Jenkins
docker restart jenkins

# Stop Jenkins
docker stop jenkins

# Start Jenkins
docker start jenkins
```

---

**Note**: Once all steps are complete and Jenkins pipeline runs successfully, you can request manual review of your project. All three components (Jenkins, GitHub Actions CI, and GitHub Actions CD) should be working together.
