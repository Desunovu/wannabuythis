### WannaBuyThis

WannaBuyThis is an application designed to help you manage and organize your wish lists. It is divided into various frontend and backend applications to ensure a seamless and efficient user experience.

**Technology Stack:**
- **Frontend:** *not implemented yet*
- **Backend:** Python, FastAPI, SQLAlchemy. (For more information, see /backend/pyproject.toml)
- **Other remarks:** The project was created to train in the use of test-driven development approaches, domain-driven design, event architecture and patterns of their support.

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

**Features:**
- Create, edit, and manage wish lists.
- User authentication and authorization.
