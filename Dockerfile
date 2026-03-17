FROM debian:stable-slim
ARG HUNSPELL_PACKAGES
RUN apt update -qq && apt install -y --no-install-recommends \
    hunspell ${HUNSPELL_PACKAGES} python3 \
    && rm -rf /var/lib/apt/lists/*
