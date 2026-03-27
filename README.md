# D2X DevOps Assignment

## Part 1  Observability Setup (Kubernetes + Prometheus + Grafana)

### Overview

This project sets up a local Kubernetes cluster with Prometheus and Grafana to monitor the CPU and memory usage per running pod. It was completed on a 2015 MacBook Pro with specs - (macOS Monterey 12.7.6, 8GB RAM, Intel Core i5).

---

### Tools that were used

Minikube - Local Kubernetes cluster
HyperKit - VM driver for Minikube on macOS 
kubectl - Command line tool to interact with the cluster 
Helm - Package manager for Kubernetes 
kube,prometheus,stack Helm chart that deploys Prometheus and Grafana together 
Prometheus Scrapes and stores the metrics from pods 
Grafana Visualises the metrics as dashboards 


### Setup Steps

#### 1. Install the dependencies

```bash
brew install kind kubectl helm minikube
brew install hyperkit
```

#### 2. Start the Minikube cluster

```bash
minikube start --driver=hyperkit
```

Verify the cluster is running:

```bash
kubectl get nodes
```

Expected output:
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   Xm    v1.35.1
```

#### 3. Add the Prometheus Helm repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

#### 4. Deploy kube,prometheus,stack

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

This installs Prometheus, Grafana, Alertmanager, and Node Exporter in the `monitoring` namespace.

#### 5. Verify all pods are running

```bash
kubectl --namespace monitoring get pods
```

All pods should show `Running` status.

#### 6. Access Grafana

```bash
kubectl --namespace monitoring port-forward svc/monitoring-grafana 3000:80
```

Open your browser and navigate to: **http://localhost:3000**

Login credentials:
- Username: `admin`
- Password: retrieve with the command below

```bash
kubectl --namespace monitoring get secret monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d ; echo
```

#### 7. Deploy NGINX (bonus app)

```bash
kubectl create deployment nginx --image=nginx
kubectl get pods
```

---

### Grafana Dashboards

The `kube-prometheus-stack` Helm chart comes with pre-built dashboards. The following were used:

- **Kubernetes / Compute Resources / Pod** — CPU and memory usage per pod
- **Kubernetes / Networking / Cluster** — Network packet transmission rates
- **Node Exporter / Nodes** — System-level metrics (CPU, memory, disk, network)

Screenshots of each dashboard are included in the repository.

#### Interview dashboard (custom)

This repo also includes a custom, interview-focused Grafana dashboard JSON:

- `nginx-k8s-interview-dashboard.json` — NGINX + Kubernetes overview (health, saturation, workloads, NGINX traffic/pressure)

To import it in Grafana:

1. In Grafana, go to **Dashboards → New → Import**
2. Upload `nginx-k8s-interview-dashboard.json`
3. Select your Prometheus datasource (it defaults to a datasource named `prometheus`)

---

### To Resume the Environment

Every time you restart your machine, run:

```bash
minikube start --driver=hyperkit
kubectl --namespace monitoring port-forward svc/monitoring-grafana 3000:80
```

Then open **http://localhost:3000**.

---

### Challenges Faced

**1. Usage of AI**
when i faced issues with compatibilty or unfamiliar tools, i used AI as assistance to find workarounds and to understand concepts. For example, identifying HyperKIT as a viable Minikube driver for macOS 12 after Docker Desktop and Colima both failed. Solutions were all verified and executed manually.


**2. Docker Desktop incompatibility**
Docker Desktop requires macOS 14 (Sonoma) or later. My machine runs macOS 12.7.6 (Monterey), so Docker Desktop could not be installed.

**3. Colima/qemu dependency failure**
Colima was attempted as a Docker Desktop alternative. However, it depends on `qemu`, which has a broken `gnutls` dependency (`z3` formula) on macOS 12. Multiple install attempts failed with `FormulaUnavailableError`.

**4. Solution Minikube with HyperKit**
Minikube with the HyperKit driver was the viable path. HyperKit is a lightweight hypervisor for macOS that does not require Docker or qemu. This allowed the Kubernetes cluster to run successfully on the hardware.

**5. NGINX metrics not visible in Grafana**
After deploying NGINX, CPU metrics did not appear in the Kubernetes / Compute Resources / Pod dashboard. This was because the NGINX deployment had no resource requests or limits defined. Prometheus relies on these to populate certain metrics. To fix this in production, resource limits would be added to the deployment manifest:




```yaml
resources:
  requests:
    cpu: "100m"
    memory: "64Mi"
  limits:
    cpu: "200m"
    memory: "128Mi"
```

---

### Alerting  How to Alert When a Pod Exceeds 80% CPU

To alert when a pod exceeds 80% CPU usage, a `PrometheusRule` resource would be created in the cluster. This defines the alert condition using PromQL (Prometheus Query Language):

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: cpu-alert
  namespace: monitoring
spec:
  groups:
    - name: pod-alerts
      rules:
        - alert: HighPodCPU
          expr: rate(container_cpu_usage_seconds_total[5m]) > 0.8
          for: 1m
          labels:
            severity: warning
          annotations:
            summary: "Pod {{ $labels.pod }} is using over 80% CPU"
```

This alert fires when a pod's CPU usage rate exceeds 80% for more than 1 minute. Alertmanager (which is included in the kube-prometheus-stack) would then route this alert to a notification channel such as Slack or email.

---

## Part 2  Python Data Exercise

### Overview

A Python script that fetches the New York State Baby Names dataset from the NYC Open Data API and answers three questions about the data.

### Requirements

```bash
pip3 install pandas requests
```

### Usage

```bash
# Top 5 male names for a given year
python3 baby_names.py --function male --year 2020

# Top female names across a year range
python3 baby_names.py --function female --start_year 2018 --end_year 2020

# Most common name overall
python3 baby_names.py --function overall
```

### Functions

| Function | Description |
|----------|-------------|
| `top_5_male_names(year)` | Returns top 5 male names for a given year |
| `top_female_names(start_year, end_year)` | Returns top female names across a year range |
| `top_name_overall()` | Returns the most common name in the entire dataset |

### Output

Results are returned as formatted JSON. Example:

```json
[
  "Liam",
  "Noah",
  "Jacob",
  "Ethan",
  "Lucas"
]
```

### Dataset

Source: [NYC Open Data - Popular Baby Names](https://data.cityofnewyork.us/resource/25th-nujf.json)

### References

- [Claude AI](https://claude.ai/)  Used for finding workarounds for compatibility issues, understanding DevOps concepts, guidance through setup process and drafting this ReadME.
- [Youtube  Kubernetes Concepts](https://www.youtube.com/watch?v=E2pP1MOfo3g)
- [Pandas Filter Guide](https://builtin.com/data-science/pandas-filter)
- [NYC Open data  Baby Names API](https://data.cityofnewyork.us/Health/Popular-Baby-Names/25th-nujf/data_preview)
- [Python Requests JSON Example](https://reqbin.com/code/python/rituxo3j/python-requests-json-example#:~:text=To%20request%20JSON%20data%20from,JSON%20decoding%20fails%2C%20then%20response.)
