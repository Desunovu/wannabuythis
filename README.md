# Wannabuythis

A web application for creating, managing, and sharing wishlists with others.

---

## Features

- **User Auth**: Secure local sign-in and registration
- **Wishlist Tools**: Create, edit, and archive lists
- **Item Control**: Track status, priority, and quantity

---

## Architecture

See [AGENTS.md](./AGENTS.md).

---

## Development

### Requirements

- Git
- **Docker** (`docker`)
- **Docker Compose** (`docker-compose`)
- **Docker BuildKit** (`docker-buildx`)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/desunovu/wannabuythis.git
   cd wannabuythis
   ```

2. **Start the application**

   For development with hot-reload:
   ```bash
   docker compose -f compose.yml -f compose.dev.yml watch
   ```

3. **Access the application**
   - Application: http://localhost
   - Backend API docs: http://localhost:8000/docs
   - Traefik dashboard: http://localhost:8080

The development setup includes:
- PostgreSQL database on port 5432
- FastAPI backend with hot-reload, directly accessible on port 8000
- Nuxt.js frontend with hot-reload, directly accessible on port 3000
- Traefik reverse proxy on port 80: routes `/api/*` to backend, `/*` to frontend

---

## Deployment

### Docker Compose

1. **Create a `.env` file** or set the environment variables
   ```bash
   # Signing key for JWT, at least 32 characters
   SECRET_KEY=<your_secret_key>

   # Database
   POSTGRES_USER=<your_username>
   POSTGRES_PASSWORD=<your_password>
   POSTGRES_DB=wannabuythis

   # Outgoing mail, used to deliver activation codes
   SMTP_HOST=<your_smtp_host>
   SMTP_SENDER=<your_email>
   ```

2. **Start the application**
   ```bash
   docker compose up -d
   ```

3. **Access the application**
   - Application: http://localhost

---

## Planned Features

- **Marketplace Integration**: Add direct links to products
- **Product Images**: Display product images and thumbnails
- **Private Wishlists**: Create private wishlists visible only to you
- **Enhanced Priority System**: Advanced prioritization with multiple criteria
- **Gift Reservation**: Reserve gifts to prevent duplicate purchases
- **Reliable Event Processing**: Persist domain events (outbox) and process them asynchronously instead of in-process

---

## CI/CD

GitHub Actions runs backend tests, ruff lint, and an OpenAPI spec check on pull requests touching `backend/**`; Docker images are built and pushed to GitHub Container Registry on manual trigger, and releases are created from the `VERSION` file.

---

## License

This project is licensed under the [GNU Affero General Public License v3.0](./LICENSE) (AGPL-3.0).
