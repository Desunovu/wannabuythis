# Wannabuythis

A web application for creating, managing, and sharing wishlists with others.

---

## Features

- **User Auth**: Secure local sign-in and registration
- **Wishlist Tools**: Сreate, edit, and archive lists
- **Item Control**: Track status, priority, and quantity

---

## Technology Stack

- **Frontend**: [Nuxt.js 3](https://nuxt.com/) (Vue-based framework)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) with [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: [PostgreSQL 16](https://www.postgresql.org/)
- **Deployment**: [Docker](https://www.docker.com/), [Kubernetes (K3s)](https://k3s.io/)

---

## Quick Start

### Requirements

- [Docker](https://www.docker.com/) and Docker Compose
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/desunovu/wannabuythis.git
   cd wannabuythis
   ```

2. **Start the application**

   For standard operation:
   ```bash
   docker compose up -d
   ```

   For development with hot-reload:
   ```bash
   docker compose watch
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

The development setup includes:
- PostgreSQL database on port 5432
- FastAPI backend with hot-reload on port 8000
- Nuxt.js frontend with hot-reload on port 3000

---

## Deployment

### Kubernetes (K3s/K3d)

#### Requirements
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- K3s or K3d cluster

#### Deploy to Kubernetes

1. **Create namespace**
   ```bash
   kubectl create namespace wannabuythis
   ```

2. **Create secret**
   ```bash
   kubectl create secret generic wannabuythis-secret \
     --from-literal=POSTGRES_USER=<your_username> \
     --from-literal=POSTGRES_PASSWORD=<your_password> \
     -n wannabuythis
   ```

3. **Apply manifests**
   ```bash
   kubectl apply -f ./k8s
   ```

4. **Access the application**

The application is available via standard HTTP (Port 80): http://localhost/

> Note: If you are running k3s on a remote server, replace `localhost` with your server's IP address or domain name.

5. **Verify deployment**
   ```bash
   kubectl get pods -n wannabuythis
   kubectl get ingress -n wannabuythis
   ```

---

## Planned Features

- **Marketplace Integration**: Add direct links to products
- **Product Images**: Display product images and thumbnails
- **Private Wishlists**: Create private wishlists visible only to you
- **Enhanced Priority System**: Advanced prioritization with multiple criteria
- **Gift Reservation**: Reserve gifts to prevent duplicate purchases

---

## CI/CD

The project uses GitHub Actions for automated workflows:

- **Test Backend**: Runs backend tests on pull requests
- **Build & Push**: Builds Docker images and pushes to GitHub Container Registry
- **OpenAPI Generation**: Auto-generates OpenAPI specs from backend code
- **Release Management**: Creates GitHub releases from VERSION file updates

---

## **License**

This project is licensed under the [GNU Affero General Public License v3.0](./LICENSE) (AGPL-3.0).
