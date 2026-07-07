ARG BUILD_FROM=ghcr.io/hassio-addons/debian-base:9.3.0
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# Setup base
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        mariadb-server=1:11.8.6-0+deb13u1 \
        mariadb-client=1:11.8.6-0+deb13u1 \
        mariadb-backup=1:11.8.6-0+deb13u1 \
        pwgen=2.08-2 \
    && rm -rf \
        /var/lib/apt/lists/* \
        /var/lib/mysql \
        /var/log/mysql \
        /tmp/*

# Copy data
COPY rootfs /

WORKDIR /

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Wheemer" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Wheemer" \
    org.opencontainers.image.licenses="Apache-2.0" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
