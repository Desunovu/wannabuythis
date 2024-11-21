# Stage 1: Base
FROM node:20-alpine AS base
WORKDIR /app
COPY package.json /app
RUN npm install

# Stage 2: Development
FROM base AS development
WORKDIR /app
# Install additional dev dependencies
RUN npm install -g npm@latest
# Run the app in development mode
CMD ["npm", "run", "dev"]

# Stage 3: Build
FROM base AS build
WORKDIR /app
COPY . /app
# Build the application for production
RUN npm run build

# Stage 4: Production
FROM node:20-alpine AS production
WORKDIR /app
# Copy built application from the build stage
COPY --from=build /usr/src/app/.output ./
# Install only production dependencies
RUN npm install --production
# Command to run Nuxt in production mode
CMD ["node", "server/index.mjs"]
