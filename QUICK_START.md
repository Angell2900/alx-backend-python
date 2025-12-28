# 🚀 Quick Start - Complete Your Setup in 20 Minutes

## ✅ What's Already Done
- Jenkinsfile with 9 stages
- GitHub Actions CI workflow (ci.yml)
- GitHub Actions CD workflow (dep.yml)
- Django models and tests
- Docker configuration
- All dependencies configured

## ⏰ Next: 3 Manual Steps (~20 minutes total)

---

## Step 1: Jenkins Dashboard Setup (10 minutes)

### 1. Open Jenkins
```
http://localhost:8080
```

### 2. Unlock Jenkins
- Paste initial admin password:
```
dd8dd7f187be4a0c9f9ceb3182d1e78a
```
- Click **Continue**

### 3. Install Plugins
- Click **"Install suggested plugins"**
- Wait for installation
- Click **"Continue as admin"** or **"Restart Jenkins"**

### 4. Create Admin User
- Username: `admin`
- Password: (your choice)
- Email: your@email.com
- Click **Save and Continue**

### 5. Create GitHub Credentials
1. Click **Manage Jenkins** → **Credentials**
2. Click **System** → **Global credentials**
3. Click **Add Credentials**
4. Select:
   - **Kind**: Username with password
   - **Scope**: Global
   - **Username**: `Angell2900`
   - **Password**: (GitHub personal access token)
   - **ID**: `github-credentials`
5. Click **Create**

### 6. Create Pipeline Job
1. Click **New Item**
2. Name: `messaging-app-pipeline`
3. Select **Pipeline**
4. Click **OK**
5. In job configuration:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/Angell2900/alx-backend-python.git`
   - **Credentials**: `github-credentials`
   - **Branch**: `*/main`
   - **Script Path**: `messaging_app/Jenkinsfile`
6. Click **Save**
7. Click **Build Now**

✅ Jenkins Setup Complete!

---

## Step 2: Add GitHub Secrets (5 minutes)

### 1. Go to GitHub Settings
```
https://github.com/Angell2900/alx-backend-python/settings/secrets/actions
```

### 2. Add DOCKER_USERNAME
- Click **New repository secret**
- **Name**: `DOCKER_USERNAME`
- **Value**: (your Docker Hub username)
- Click **Add secret**

### 3. Add DOCKER_PASSWORD
- Click **New repository secret**
- **Name**: `DOCKER_PASSWORD`
- **Value**: (your Docker Hub access token)
- Click **Add secret**

✅ GitHub Secrets Added!

---

## Step 3: Verify Everything Works (5 minutes)

### Option A: Trigger from GitHub (Automatic)
```bash
# Make any change and push
git push origin main
```
Watch it happen:
1. Go to **Actions** tab on GitHub
2. See CI workflow run (green ✅)
3. See CD workflow build Docker (green ✅)

### Option B: Trigger from Jenkins (Manual)
1. Go to http://localhost:8080
2. Click `messaging-app-pipeline`
3. Click **Build Now**
4. Watch the build progress

### Expected Results
- ✅ All tests pass
- ✅ Coverage reports generated
- ✅ Docker image built
- ✅ Image pushed to Docker Hub

### Verify Docker Image
```
https://hub.docker.com/r/angell2900/messaging-app
```

---

## 🎯 You're Done!

Once you see:
- ✅ Green checkmark on CI workflow
- ✅ Green checkmark on CD workflow
- ✅ Docker image on Docker Hub

**Request manual review** from your peers.

---

## 🆘 If Something Fails

### Jenkins Build Fails
- Check build logs: Click on the build number → Console Output
- Common issues:
  - Git credentials wrong
  - Python/pytest not installed
  - Docker not available

### GitHub Secrets Not Working
- Verify secret names are exactly: `DOCKER_USERNAME` and `DOCKER_PASSWORD`
- Check secrets are set to the repository (not organization)
- Wait 30 seconds after adding secrets

### Docker Push Fails
- Verify Docker Hub credentials are correct
- Check Docker Hub account exists: https://hub.docker.com/r/angell2900
- Verify repository exists or auto-create is enabled

### Tests Fail
- Check MySQL is running (GitHub Actions handles this)
- Verify Django INSTALLED_APPS includes required apps
- Check database environment variables

---

## 📞 Useful Links

| Component | URL |
|-----------|-----|
| Jenkins | http://localhost:8080 |
| GitHub Repo | https://github.com/Angell2900/alx-backend-python |
| GitHub Actions | https://github.com/Angell2900/alx-backend-python/actions |
| GitHub Secrets | https://github.com/Angell2900/alx-backend-python/settings/secrets/actions |
| Docker Hub | https://hub.docker.com/r/angell2900/messaging-app |
| GitHub Token Creator | https://github.com/settings/tokens |
| Docker Token Creator | https://hub.docker.com/settings/security |

---

## ⚡ TL;DR

1. **Jenkins**: Open http://localhost:8080 → unlock → install plugins → create job with `messaging_app/Jenkinsfile`
2. **GitHub Secrets**: Add `DOCKER_USERNAME` and `DOCKER_PASSWORD`
3. **Test**: Push to main or click "Build Now" in Jenkins
4. **Done**: Watch workflows execute ✅

**Time needed**: ~20 minutes
**Status**: Everything ready to go!

