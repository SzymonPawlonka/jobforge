FROM golang:1.23-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/analyzer ./cmd/server \
    && CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/healthcheck ./cmd/healthcheck

FROM alpine:3.21
RUN apk add --no-cache ca-certificates \
    && addgroup -S app && adduser -S -G app app
COPY --from=build /out/analyzer /usr/local/bin/analyzer
COPY --from=build /out/healthcheck /usr/local/bin/healthcheck
USER app
EXPOSE 50051
ENTRYPOINT ["/usr/local/bin/analyzer"]
