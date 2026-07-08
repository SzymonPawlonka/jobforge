package analyzer

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"strings"
	"unicode/utf8"

	analyzerpb "github.com/sedittis/jobforge/services/analyzer-go/proto"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

const DefaultMaxFileBytes = 1_048_576

type Service struct {
	analyzerpb.UnimplementedFileAnalyzerServer
	MaxFileBytes int
}

func NewService(maxFileBytes int) *Service {
	if maxFileBytes <= 0 {
		maxFileBytes = DefaultMaxFileBytes
	}
	return &Service{MaxFileBytes: maxFileBytes}
}

func (s *Service) AnalyzeFile(_ context.Context, request *analyzerpb.FileRequest) (*analyzerpb.FileAnalysis, error) {
	content := request.GetContent()
	if len(content) > s.MaxFileBytes {
		return nil, status.Errorf(codes.ResourceExhausted, "file is larger than %d bytes", s.MaxFileBytes)
	}

	lineCount := int64(0)
	if len(content) > 0 {
		lineCount = int64(bytes.Count(content, []byte{'\n'}) + 1)
	}
	digest := sha256.Sum256(content)

	return &analyzerpb.FileAnalysis{
		SizeBytes:      int64(len(content)),
		CharacterCount: int64(utf8.RuneCount(content)),
		WordCount:      int64(len(strings.Fields(string(content)))),
		LineCount:      lineCount,
		Sha256:         hex.EncodeToString(digest[:]),
	}, nil
}
