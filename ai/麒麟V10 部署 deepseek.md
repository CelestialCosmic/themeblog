k8s docker

使用 Kubernetes (k8s) 部署 AI 集群，就像是在海上建造一支舰队，每艘船（容器）都有自己的任务，而 Kubernetes 就是指挥这支舰队的将军。让我们一起深入探讨如何在 Kubernetes 上部署 AI 集群，充分利用其强大的编排能力。

### 一、准备工作

**1. 搭建 Kubernetes 集群**

- **选择部署方式**：你可以自行搭建 Kubernetes 集群，或者使用云服务提供商的托管服务，如 AWS EKS、Google GKE、Azure AKS 等。
- **版本兼容性**：确保 Kubernetes 的版本与后续要安装的工具和插件兼容。

**2. 配置 GPU 节点**

- **硬件要求**：确保集群中的节点配备 NVIDIA GPU，以满足 AI 计算需求。
- **安装 NVIDIA 驱动**：在所有 GPU 节点上安装最新的 NVIDIA 驱动程序。

```bash
# 更新包列表
sudo apt-get update

# 安装必要的依赖
sudo apt-get install -y build-essential dkms

# 下载并安装 NVIDIA 驱动
# 前往 NVIDIA 官网下载适合你 GPU 的驱动版本，然后运行安装程序
sudo bash NVIDIA-Linux-x86_64-*.run
```

### 二、部署 NVIDIA Kubernetes 工具

**1. 安装 NVIDIA Docker 支持**

- **添加 GPG 密钥和仓库**

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
```

- **安装 nvidia-docker2**

```bash
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

**2. 部署 NVIDIA Device Plugin**

- **在 Kubernetes 中部署插件**

```bash
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.11.0/nvidia-device-plugin.yml
```

- **验证 GPU 是否被识别**

```bash
kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"
```

### 三、构建 AI 应用容器镜像

**1. 编写 Dockerfile**

- **基础镜像**：选择合适的基础镜像，如 `nvidia/cuda`，并安装所需的深度学习框架（TensorFlow、PyTorch 等）。

```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 安装 Python 和其他依赖
RUN apt-get update && apt-get install -y python3 python3-pip

# 安装深度学习框架
RUN pip3 install torch

# 复制你的应用代码
COPY . /app

# 设置工作目录
WORKDIR /app

# 指定启动命令
CMD ["python3", "your_ai_app.py"]
```

**2. 构建并推送镜像**

```bash
# 构建镜像
docker build -t your-repo/ai-app:latest .

# 登录镜像仓库
docker login

# 推送镜像
docker push your-repo/ai-app:latest
```

### 四、编写 Kubernetes 部署文件

**1. 创建 Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-app-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ai-app
  template:
    metadata:
      labels:
        app: ai-app
    spec:
      containers:
        - name: ai-app-container
          image: your-repo/ai-app:latest
          resources:
            limits:
              nvidia.com/gpu: 1 # 请求一个 GPU
          ports:
            - containerPort: 8080
          # 使用 NVIDIA GPU 调度器
          nodeSelector:
            nvidia.com/gpu.present: "true"
```

**2. 创建 Service**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-app-service
spec:
  type: NodePort
  selector:
    app: ai-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

### 五、部署到 Kubernetes 集群

**1. 部署应用**

```bash
kubectl apply -f ai-app-deployment.yml
kubectl apply -f ai-app-service.yml
```

**2. 验证部署状态**

```bash
kubectl get pods
kubectl describe pod ai-app-deployment-xxxxx
```

### 六、访问 AI 应用

- **获取节点 IP 和服务端口**

```bash
kubectl get nodes -o wide
kubectl get svc ai-app-service
```

- **访问方式**

在浏览器或通过 `curl` 命令访问 `节点IP:NodePort`，即可与 AI 应用进行交互。

### 七、扩展与优化

**1. 自动水平扩展（HPA）**

- **部署 Metrics Server**

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

- **创建 HPA**

```bash
kubectl autoscale deployment ai-app-deployment --cpu-percent=50 --min=2 --max=10
```

**2. 资源调度优化**

- **使用 Taints 和 Tolerations**：确保只在 GPU 节点上调度 GPU 负载。
- **使用 Node Affinity**：指定 Pod 只能调度到具有特定标签的节点。

### 八、监控与日志

**1. 部署监控系统**

- **Prometheus & Grafana**：用于监控集群和应用的性能指标。
- **安装**

```bash
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/master/bundle.yaml
```

**2. 日志管理**

- **ELK 堆栈（Elasticsearch、Logstash、Kibana）**：收集和分析日志。

### 九、持续集成与持续部署（CI/CD）

- **配置流水线**：使用 Jenkins、GitLab CI 等工具，实现代码的自动构建、测试和部署。
- **版本控制**：在代码中实现版本控制，确保可回滚和追踪。

### 十、高级主题

**1. 分布式训练**

- **使用 MPI Operator**：在 Kubernetes 上运行分布式训练任务。

```bash
kubectl apply -f https://raw.githubusercontent.com/kubeflow/mpi-operator/master/deploy/v1alpha2/mpi-operator.yaml
```

- **编写 MPIJob 资源**：定义分布式训练的任务。

**2. 数据管理**

- **Persistent Volume（PV）和 Persistent Volume Claim（PVC）**：管理持久化存储，用于存储训练数据和模型。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ai-data-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
```

### 十一、可视化管理工具

- **Kubernetes Dashboard**：提供集群的图形化界面，方便管理和监控。
- **Lens**：一款流行的开源 Kubernetes 管理工具。

---

**小结**：

通过上述步骤，你已经在 Kubernetes 上成功部署了一个功能完善的 AI 集群。这不仅提升了 AI 应用的可扩展性和可靠性，还为进一步的自动化和智能化打下了坚实的基础。

就像一棵正在生长的参天大树，你的 AI 集群也需要持续的关注和养护。随着业务需求的变化，你可能需要：

- **探索新的调度策略**：例如使用 Gang Scheduling，以满足复杂的资源需求。
- **优化网络性能**：引入 Service Mesh（如 Istio）来提升服务间通信的效率和安全性。
- **加强安全防护**：实施零信任安全模型，确保集群的安全可靠。

如果你对特定的部分感兴趣，比如分布式训练、模型部署流水线，或者需要解决在实际操作中遇到的问题，随时告诉我，我愿意和你一起探索更深的领域！