#!/usr/bin/env bash

docker-compose exec keycloak bash -c "keycloak/bin/kcreg.sh config credentials --server http://localhost:8080/auth --realm utilityx --user mario.garcia@kaleidos.net && cat ~/.keycloak/kcreg.config"
