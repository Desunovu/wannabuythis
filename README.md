### wannabuythis

wantbuythis is a web application for advanced wishlist management. This monorepository contains backend and frontend applications in their respective directories.

**Technology Stack:**
- **Frontend:** Nuxt.js
- **Backend:** Python, FastAPI, SQLAlchemy (see /backend/pyproject.toml for details)
- **Other remarks:** Initially, the project was created for educational purposes, to practice architectural patterns and various python application designs. The code does not pretend to be a good example of TDD, DDD, EDA and other approaches.

**Startup Instructions:**
1. **Clone the Repository:**
    ```sh
    git clone https://github.com/desunovu/wannabuythis.git
    cd wannabuythis
    ```

2. **Set Up the backend in development mode:**
    - Install and configure Poetry
    - Install the required dependencies:
      ```sh
      cd backend
      poetry install
      ```
    - Run postgres from docker-compose:
      ```sh
      docker-compose up -d postgres
      ```
    - Run database migrations:
      ```sh
      poetry run alembic upgrade head
      ```
    - Start the FastAPI server:
      ```sh
      poetry run uvicorn src.integration.entrypoints.fastapi_app:app --reload
      ```
