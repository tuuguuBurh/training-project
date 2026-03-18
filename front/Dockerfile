FROM node:24-alpine AS base

# Set environment variables
ENV TZ=Asia/Tokyo

# Use the correct timezone
RUN apk add --no-cache tzdata && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

RUN npm install -g pnpm

COPY ./front/package.json ./
COPY ./front/pnpm-lock.yaml ./
RUN pnpm install

EXPOSE 3000

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Development target
FROM base AS dev

# Production target
FROM base AS prod
COPY ./front ./
RUN pnpm run build
