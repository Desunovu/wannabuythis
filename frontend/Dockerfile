# ==== Node-base Stage ====
FROM node:20-alpine AS base
WORKDIR /app

# ==== Dependencies Stage ====
FROM base AS dependencies
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# ==== Development Stage ====
FROM dependencies AS development
ENV NODE_ENV=development
COPY  . .
RUN npm ci
CMD ["npm", "run", "dev"]

# ==== Build Stage ====
FROM dependencies AS build
ENV NODE_ENV=production
COPY . .
RUN npm run build

# ==== Production Stage ====
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=build /app/.output /app/.output

ENV HOST=0.0.0.0
EXPOSE 3000
ENTRYPOINT ["node", ".output/server/index.mjs"]
