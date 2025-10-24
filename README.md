# **Wannabuythis**

**Wannabuythis** is a web application designed for advanced wishlist management. It enables users to create, manage, and share wishlists with others. Originally developed as a pet project, the application serves as a platform for exploring software architecture and modern web development practices.

---

## **Features**

- Create, update, and delete wishlists and wishlist items.
- Share wishlists with others.
- Advanced management options, including prioritization and status tracking.

---

## **Technology Stack**

- **Frontend:** [Nuxt.js](https://nuxt.com/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **Deployment:** [Docker](https://www.docker.com/), [Kubernetes (K3s)](https://k3s.io/)

**Note:** This project was developed for educational purposes to practice software design patterns and concepts such as Test-Driven Development (TDD), Domain-Driven Design (DDD), and Event-Driven Architecture (EDA). While it includes practical implementations, the codebase may not fully adhere to industry best practices for these methodologies.

---

## **Demo screenshots**

[[TODO add link to the assets]]()

---

## **Development Setup**

### **Prerequisites**

- [Docker](https://www.docker.com/)
- [K3d](https://k3d.io/) (lightweight local K3s cluster) or [K3s](https://k3s.io/) installed directly
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [systemd](https://www.freedesktop.org/wiki/Software/systemd/)

### **Running the Application in Development Mode**

In development mode, the application runs the following services within Docker containers, with the source code linked to the host system for live updates:

1. A **PostgreSQL** database.
2. A **FastAPI** backend application (served via uvicorn --reload).
3. A **Nuxt 3** frontend application (served via npm run dev).

To start the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/desunovu/wannabuythis.git  
   cd wannabuythis  
   ```
2. Build and launch the containers:
   ```bash
   docker compose up -d  
   ```
3. Access the application:
   - Frontend: [http://localhost:3000](http://localhost:3000/)
   - Backend (FastAPI Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

---

## **Local Deployment with K3s**

### **0. Create or Select a Local K3s/K3d Cluster**

Choose one of the following options:

* **Native k3s** (installed as a service): make sure the server is running, e.g. `sudo systemctl start k3s` (or it may already be up after install).
* **k3d** (container-based K3s): create a disposable local cluster (example below exposes HTTP 80):

```bash
k3d cluster create wannabuythis --agents 1 -p "80:80@loadbalancer"
```

> Skip this step if you already have a cluster and `kubectl` is pointed to it.

### **1. Configure Kubernetes Resources**

Create a dedicated namespace for the project (run once):

```bash
kubectl create namespace wannabuythis
```

Ensure the required configuration files are set up:

- Modify `configmap.yaml` as needed.
- Manually create the secret with required keys (`POSTGRES_USER`, `POSTGRES_PASSWORD`) using the following command:

  ```bash
  kubectl create secret generic wannabuythis-secret \
    --from-literal=POSTGRES_USER=<username> \
    --from-literal=POSTGRES_PASSWORD=<password> \
    -n wannabuythis
  ```

Apply the Kubernetes manifests:

```bash
kubectl apply -f ./k8s
```

### **2. Expose Services (Traefik Ingress)**

K3s bundles the Traefik ingress controller by default. After applying manifests you can reach:

- Frontend: http://localhost/  
- Backend API docs: http://localhost/api/docs

### **3. Verify Deployment**

Once everything is set up, verify that the application is running:

```bash
kubectl get pod -n=wannabuythis
kubectl get application -n=wannabuythis
kubectl get application -n=kube-system | grep traefik
```

---

## **License**

This project is released under the [AGPL-3.0 license](./LICENSE).
