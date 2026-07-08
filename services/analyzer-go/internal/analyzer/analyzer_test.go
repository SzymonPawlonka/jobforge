package analyzer

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"testing"

	analyzerpb "github.com/sedittis/jobforge/services/analyzer-go/proto"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func TestAnalyzeFile(t *testing.T) {
	service := NewService(DefaultMaxFileBytes)
	content := []byte("Ala ma kota\nDruga linia")
	result, err := service.AnalyzeFile(context.Background(), &analyzerpb.FileRequest{Filename: "test.txt", Content: content})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	digest := sha256.Sum256(content)
	if result.SizeBytes != int64(len(content)) || result.WordCount != 5 || result.LineCount != 2 {
		t.Fatalf("unexpected analysis: %+v", result)
	}
	if result.Sha256 != hex.EncodeToString(digest[:]) {
		t.Fatalf("unexpected sha256: %s", result.Sha256)
	}
}

func TestAnalyzeEmptyFile(t *testing.T) {
	result, err := NewService(DefaultMaxFileBytes).AnalyzeFile(context.Background(), &analyzerpb.FileRequest{})
	if err != nil {
		t.Fatal(err)
	}
	if result.SizeBytes != 0 || result.CharacterCount != 0 || result.WordCount != 0 || result.LineCount != 0 {
		t.Fatalf("unexpected empty analysis: %+v", result)
	}
}

func TestRejectsOversizedFile(t *testing.T) {
	_, err := NewService(2).AnalyzeFile(context.Background(), &analyzerpb.FileRequest{Content: []byte("abc")})
	if status.Code(err) != codes.ResourceExhausted {
		t.Fatalf("expected ResourceExhausted, got %v", err)
	}
}
