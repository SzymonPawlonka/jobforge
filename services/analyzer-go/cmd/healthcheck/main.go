package main

import (
	"context"
	"flag"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"
)

func main() {
	address := flag.String("addr", "localhost:50051", "gRPC server address")
	flag.Parse()

	connection, err := grpc.NewClient(*address, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatal(err)
	}
	defer connection.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	response, err := healthpb.NewHealthClient(connection).Check(ctx, &healthpb.HealthCheckRequest{})
	if err != nil {
		log.Fatal(err)
	}
	if response.GetStatus() != healthpb.HealthCheckResponse_SERVING {
		log.Fatalf("service is not serving: %s", response.GetStatus())
	}
}
