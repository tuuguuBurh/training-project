FROM node:22-alpine AS base

RUN corepack enable && corepack prepare pnpm@10.28.2 --activate

ENV TZ=Asia/Ulaanbaatar \
  NUXT_HOST=0.0.0.0 \
  NUXT_PORT=3000

RUN apk add --no-cache tzdata && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
  echo $TZ > /etc/timezone && \
  apk del --no-cache tzdata

WORKDIR /app

COPY ./front/package.json ./front/pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

EXPOSE 3000

# ============================================
# Development target (runs as root for volume mounts)
# ============================================
FROM base AS dev

# ============================================
# Production target (runs as non-root)
# ============================================
FROM base AS prod

RUN addgroup --system --gid 1001 nodejs && \
  adduser --system --uid 1001 --ingroup nodejs nuxt && \
  chown -R nuxt:nodejs /app

USER nuxt
