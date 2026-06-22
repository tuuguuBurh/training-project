FROM node:24-alpine AS base

ARG TZ=Asia/Ulaanbaatar
ENV TZ=${TZ}

RUN apk add --no-cache \
    tzdata \
    libc6-compat \
    python3 \
    make \
    g++ \
    vips-dev \
  && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
  && echo $TZ > /etc/timezone

WORKDIR /app

# pnpm тохиргоо
ENV CI=true

RUN corepack enable && corepack prepare pnpm@11 --activate

COPY ./front/package.json ./
COPY ./front/pnpm-lock.yaml ./
COPY ./front/pnpm-workspace.yaml ./
COPY ./front/.npmrc* ./

RUN pnpm install

EXPOSE ${FRONT_PORT:-3000}

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=${FRONT_PORT:-3000}

FROM base AS dev

FROM base AS prod
COPY ./front ./
RUN pnpm run build