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
- **Deployment:** [Docker](https://www.docker.com/)

**Note:** This project was developed for educational purposes to practice software design patterns and concepts such as Test-Driven Development (TDD), Domain-Driven Design (DDD), and Event-Driven Architecture (EDA). While it includes practical implementations, the codebase may not fully adhere to industry best practices for these methodologies.

---

## **Demo screenshots**
[[TODO add link to the assets]]()

---

## **Development Setup**

### **Prerequisites**

- [Docker](https://www.docker.com/)

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

## **License**

This project is released under the [AGPL-3.0 license](./LICENSE). 