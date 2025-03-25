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
- **Deployment:** [Docker](https://www.docker.com/), [Kubernetes (Minikube)](https://minikube.sigs.k8s.io/docs/)

**Note:** This project was developed for educational purposes to practice software design patterns and concepts such as Test-Driven Development (TDD), Domain-Driven Design (DDD), and Event-Driven Architecture (EDA). While it includes practical implementations, the codebase may not fully adhere to industry best practices for these methodologies.

---

## **Demo screenshots**

[[TODO add link to the assets]]()

---

## **Development Setup**

### **Prerequisites**

- [Docker](https://www.docker.com/)
- [Minikube](https://minikube.sigs.k8s.io/docs/)
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

## **Local Deployment with Minikube**

### **1. Configure Kubernetes Resources**

Ensure the required configuration files are set up:

- Modify `configmap.yaml` as needed.
- Create and populate `secret.yaml` (use `secret-template.yaml` as a reference).

Apply the Kubernetes manifests:

```bash
kubectl apply -f ./k8s
```

### **4. Set Up Ingress Access**

Minikube exposes the Ingress controller on a NodePort. To make the application accessible on port 80, run the following command manually:

1. Identify the NodePort assigned to the Ingress controller:

   ```bash
   kubectl get service -n ingress-nginx | grep ingress-nginx-controller
   ```

   Look for the `NodePort`, e.g., `32219`.

2. Start a socat process to forward traffic from port 80:
   ```bash
   sudo socat TCP4-LISTEN:80,fork TCP4:$(minikube ip):32219
   ```
   Keep this terminal window open while working with Minikube, as closing it will stop the forwarding.

### **5. Configure Firewall Rules**

Allow traffic on port 80:

```bash
sudo firewall-cmd --add-port=80/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

### **6. Verify Deployment**

Once everything is set up, verify that the application is running:

```bash
kubectl get pod -n=wannabuythis
kubectl get service -n=wannabuythis
kubectl get service -n=ingress-nginx
```

The frontend should now be accessible at `http://localhost`.

---

## **License**

This project is released under the [AGPL-3.0 license](./LICENSE).
