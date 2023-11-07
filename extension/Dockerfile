FROM --platform=$BUILDPLATFORM node:18.12-alpine3.16 AS client-builder
WORKDIR /ui
# cache packages in layer
COPY ui/package.json /ui/package.json
COPY ui/package-lock.json /ui/package-lock.json
RUN --mount=type=cache,target=/usr/src/app/.npm \
    npm set cache /usr/src/app/.npm && \
    npm ci
# install
COPY ui /ui
RUN npm run build

FROM python:3.8-alpine
LABEL org.opencontainers.image.title="Hey Docker" \
    org.opencontainers.image.description="Empower your Docker workflows and system monitoring with HeyDocker, your virtual Docker companion in your chat app. Streamline operations, gain insights, and maintain optimal performance effortlessly." \
    org.opencontainers.image.vendor="Docker" \
    com.docker.desktop.extension.api.version="0.3.4" \
    com.docker.extension.screenshots="" \
    com.docker.desktop.extension.icon="logo.svg" \
    com.docker.extension.detailed-description="" \
    com.docker.extension.publisher-url="" \
    com.docker.extension.additional-urls="" \
    com.docker.extension.categories="" \
    com.docker.extension.changelog=""

COPY docker-compose.yaml .
COPY metadata.json .
COPY logo.svg .
COPY backend/main.py .
COPY --from=client-builder /ui/build ui
RUN apk update && apk add --no-cache git && python -m pip install git+https://github.com/syanng/HeyDocker.git
CMD nohup heydocker & python main.py
