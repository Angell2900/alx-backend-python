# Kubernetes Container Orchestration Project

This project demonstrates comprehensive container orchestration using Kubernetes with a Django messaging application. It covers all essential Kubernetes concepts including deployments, services, ingress, scaling, blue-green deployments, and rolling updates.

## 📋 Project Overview

The project includes a complete Django messaging application deployed and managed through Kubernetes with the following features:

- **Django Messaging App**: A web application with user authentication and message management
- **Kubernetes Orchestration**: Complete deployment, scaling, and management workflow
- **Production-Ready Configurations**: Health checks, resource limits, and best practices
- **Advanced Deployment Strategies**: Blue-green deployments and rolling updates
- **External Access**: Ingress configuration for internet access
- **Monitoring and Testing**: Load testing and performance monitoring

## 🏗️ Project Structure

```
messaging_app/
├── kurbeScript                    # Task 0: Kubernetes cluster setup
├── deployment.yaml                # Task 1: Basic Django app deployment
├── kubctl-0x01                    # Task 2: Scaling and load testing
├── ingress.yaml                   # Task 3: External access configuration
├── commands.txt                   # Task 3: Ingress setup commands
├── blue_deployment.yaml           # Task 4: Blue version deployment (v2.0)
├── green_deployment.yaml          # Task 4: Green version deployment
├── kubeservice.yaml               # Task 4: Service configuration
├── kubctl-0x02                    # Task 4: Blue-green deployment script
├── kubctl-0x03                    # Task 5: Rolling update script
└── README.md                      # This file
```

## 🎯 Learning Objectives

This project teaches you to:

1. **Set up Kubernetes locally** using Minikube
2. **Deploy containerized applications** with Kubernetes
3. **Scale applications** horizontally and monitor resources
4. **Configure external access** using Ingress
5. **Implement deployment strategies** (Blue-Green and Rolling Updates)
6. **Monitor and test** application performance

## 🚀 Quick Start

### Prerequisites

- Docker installed
- kubectl installed
- Minikube installed
- Homebrew (for macOS users)

### Step 1: Set Up Kubernetes Cluster

```bash
./kurbeScript
```

This script will:
- Install Minikube and kubectl if not present
- Start a local Kubernetes cluster
- Verify cluster is running
- Show available pods

### Step 2: Deploy Django Application

```bash
kubectl apply -f deployment.yaml
```

This creates:
- Deployment with Django messaging app
- ClusterIP Service for internal access
- Health checks and resource limits

### Step 3: Scale the Application

```bash
./kubctl-0x01
```

This script will:
- Scale deployment to 3 replicas
- Perform load testing with wrk
- Monitor resource usage
- Show deployment status

### Step 4: Set Up External Access

```bash
minikube addons enable ingress
kubectl apply -f ingress.yaml
```

See `commands.txt` for detailed setup instructions.

### Step 5: Blue-Green Deployment

```bash
./kubctl-0x02
```

This script will:
- Deploy blue and green versions
- Test green version before switching
- Provide traffic switching capability
- Enable easy rollback

### Step 6: Rolling Updates

```bash
./kubctl-0x03
```

This script will:
- Trigger a rolling update to version 2.0
- Monitor update progress
- Test application availability during update
- Verify successful completion

## 📊 Key Kubernetes Concepts Covered

### 1. **Deployments**
- Declarative application deployment
- Rolling updates and rollbacks
- Health checks and resource management

### 2. **Services**
- ClusterIP for internal communication
- Load balancing across pods
- Service discovery

### 3. **Ingress**
- External HTTP routing
- Host-based and path-based routing
- Integration with Nginx controller

### 4. **Scaling**
- Horizontal Pod Autoscaling
- Manual scaling with kubectl
- Resource monitoring and load testing

### 5. **Advanced Deployment Strategies**
- **Blue-Green**: Zero-downtime deployments with rollback capability
- **Rolling Updates**: Gradual pod replacement with monitoring

## 🔧 Configuration Details

### Django Application Configuration

```yaml
# Resource limits and requests
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# Health checks
livenessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Service Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: django-messaging-service
spec:
  type: ClusterIP
  selector:
    app: django-messaging
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Ingress Configuration

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: django-messaging-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: messaging-app.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: django-messaging-service
            port:
              number: 80
```

## 🧪 Testing and Monitoring

### Load Testing

The project includes automated load testing using `wrk`:

```bash
# Install wrk (if not using Homebrew)
brew install wrk

# Run load test
./kubctl-0x01
```

### Application Monitoring

```bash
# Monitor pod resources
kubectl top pods -l app=django-messaging

# Check deployment status
kubectl get deployments

# View logs
kubectl logs -l app=django-messaging

# Describe pods for detailed info
kubectl describe pods -l app=django-messaging
```

### Health Checks

Each deployment includes:
- **Liveness Probe**: Ensures containers are running
- **Readiness Probe**: Ensures containers can accept traffic
- **Startup Probe**: Ensures containers start successfully

## 🔄 Deployment Strategies

### Blue-Green Deployment

**Advantages:**
- Zero downtime
- Easy rollback
- Complete testing before switch
- Safe production deployment

**How it works:**
1. Deploy "green" version alongside "blue"
2. Test green version thoroughly
3. Switch traffic from blue to green
4. Keep blue version for quick rollback

**Usage:**
```bash
./kubctl-0x02

# Switch to green version
kubectl patch service django-messaging-service -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback to blue version
kubectl patch service django-messaging-service -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Rolling Updates

**Advantages:**
- Gradual replacement
- Automatic rollback on failure
- No downtime
- Resource efficient

**How it works:**
1. Update deployment configuration
2. Kubernetes gradually replaces old pods with new ones
3. Each new pod must pass health checks
4. Automatic rollback if failures occur

**Usage:**
```bash
./kubctl-0x03
```

## 🎓 Best Practices Implemented

### 1. **Declarative Configuration**
- All resources defined in YAML files
- Version controlled configurations
- Reproducible deployments

### 2. **Resource Management**
- CPU and memory requests/limits
- Efficient scheduling
- Resource isolation

### 3. **Health Monitoring**
- Comprehensive health checks
- Automatic pod replacement
- Service discovery

### 4. **Security**
- Non-root containers
- Minimal image sizes
- Network policies

### 5. **Scalability**
- Horizontal pod scaling
- Load balancing
- Resource monitoring

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. **Pods not starting**
```bash
# Check pod status
kubectl get pods

# View pod logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>
```

#### 2. **Service not accessible**
```bash
# Check service endpoints
kubectl get endpoints

# Verify service configuration
kubectl describe service django-messaging-service
```

#### 3. **Ingress not working**
```bash
# Check ingress controller status
kubectl get pods -n ingress-nginx

# View ingress logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
```

#### 4. **Deployment failures**
```bash
# Check rollout status
kubectl rollout status deployment/django-messaging-app

# Rollback deployment
kubectl rollout undo deployment/django-messaging-app
```

## 📈 Performance Considerations

### Resource Optimization

- **Requests**: Ensure pods get minimum required resources
- **Limits**: Prevent resource exhaustion
- **Liveness/Readiness**: Proper probe timing for your application

### Scaling Strategies

- **Manual Scaling**: Immediate control for testing
- **HPA**: Automatic scaling based on metrics
- **VPA**: Vertical pod autoscaling for resource optimization

### Network Optimization

- **Service Mesh**: Consider Istio for advanced networking
- **CDN**: Use for static content delivery
- **Caching**: Implement Redis for session management

## 🔗 Additional Resources

### Kubernetes Documentation
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)

### Django on Kubernetes
- [Django Production Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Kubernetes Django Guide](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

### Monitoring and Observability
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)
- [ELK Stack](https://www.elastic.co/what-is/elk-stack)

## 🎉 Project Completion

This project demonstrates mastery of:
- ✅ Container orchestration fundamentals
- ✅ Kubernetes resource management
- ✅ Production deployment strategies
- ✅ Monitoring and testing
- ✅ DevOps best practices

## 📝 Notes

- This project uses SQLite for simplicity. For production, use PostgreSQL or MySQL
- Images should be built and pushed to a registry before deployment
- Consider using Helm for more complex deployments
- Implement proper CI/CD pipelines for automated deployments

## 🤝 Contributing

This is an educational project. Feel free to:
- Suggest improvements
- Add new features
- Fix bugs
- Enhance documentation

---

**Happy Kubernetes Learning!** 🚀
