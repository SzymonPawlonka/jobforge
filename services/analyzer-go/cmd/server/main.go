package main

import (
	"log"
	"net"
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"github.com/sedittis/jobforge/services/analyzer-go/internal/analyzer"
	analyzerpb "github.com/sedittis/jobforge/services/analyzer-go/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"
)

func main() {
	port := getenv("PORT", "50051")
	maxBytes := getenvInt("ANALYZER_MAX_FILE_BYTES", analyzer.DefaultMaxFileBytes)
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("listen: %v", err)
	}

	server := grpc.NewServer(
		grpc.MaxRecvMsgSize(maxBytes+4096),
		grpc.MaxSendMsgSize(4*1024*1024),
	)
	analyzerpb.RegisterFileAnalyzerServer(server, analyzer.NewService(maxBytes))

	healthServer := health.NewServer()
	healthServer.SetServingStatus("", healthpb.HealthCheckResponse_SERVING)
	healthServer.SetServingStatus("analyzer.FileAnalyzer", healthpb.HealthCheckResponse_SERVING)
	healthpb.RegisterHealthServer(server, healthServer)

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-stop
		log.Println("graceful shutdown")
		healthServer.SetServingStatus("", healthpb.HealthCheckResponse_NOT_SERVING)
		server.GracefulStop()
	}()

	log.Printf("JobForge analyzer listening on :%s, max file %d bytes", port, maxBytes)
	if err := server.Serve(listener); err != nil {
		log.Fatalf("serve: %v", err)
	}
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func getenvInt(key string, fallback int) int {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}
	parsed, err := strconv.Atoi(value)
	if err != nil || parsed <= 0 {
		log.Printf("invalid %s=%q; using %d", key, value, fallback)
		return fallback
	}
	return parsed
}
