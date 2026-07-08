// Code generated manually to match analyzer.proto. DO NOT EDIT.
// source: analyzer.proto

package analyzerpb

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

const _ = grpc.SupportPackageIsVersion9

const FileAnalyzer_AnalyzeFile_FullMethodName = "/analyzer.FileAnalyzer/AnalyzeFile"

type FileAnalyzerClient interface {
	AnalyzeFile(ctx context.Context, in *FileRequest, opts ...grpc.CallOption) (*FileAnalysis, error)
}

type fileAnalyzerClient struct{ cc grpc.ClientConnInterface }

func NewFileAnalyzerClient(cc grpc.ClientConnInterface) FileAnalyzerClient {
	return &fileAnalyzerClient{cc}
}

func (c *fileAnalyzerClient) AnalyzeFile(ctx context.Context, in *FileRequest, opts ...grpc.CallOption) (*FileAnalysis, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(FileAnalysis)
	err := c.cc.Invoke(ctx, FileAnalyzer_AnalyzeFile_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

type FileAnalyzerServer interface {
	AnalyzeFile(context.Context, *FileRequest) (*FileAnalysis, error)
	mustEmbedUnimplementedFileAnalyzerServer()
}

type UnimplementedFileAnalyzerServer struct{}

func (UnimplementedFileAnalyzerServer) AnalyzeFile(context.Context, *FileRequest) (*FileAnalysis, error) {
	return nil, status.Errorf(codes.Unimplemented, "method AnalyzeFile not implemented")
}
func (UnimplementedFileAnalyzerServer) mustEmbedUnimplementedFileAnalyzerServer() {}
func (UnimplementedFileAnalyzerServer) testEmbeddedByValue()                      {}

type UnsafeFileAnalyzerServer interface{ mustEmbedUnimplementedFileAnalyzerServer() }

func RegisterFileAnalyzerServer(s grpc.ServiceRegistrar, srv FileAnalyzerServer) {
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&FileAnalyzer_ServiceDesc, srv)
}

func _FileAnalyzer_AnalyzeFile_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FileRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(FileAnalyzerServer).AnalyzeFile(ctx, in)
	}
	info := &grpc.UnaryServerInfo{Server: srv, FullMethod: FileAnalyzer_AnalyzeFile_FullMethodName}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(FileAnalyzerServer).AnalyzeFile(ctx, req.(*FileRequest))
	}
	return interceptor(ctx, in, info, handler)
}

var FileAnalyzer_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "analyzer.FileAnalyzer",
	HandlerType: (*FileAnalyzerServer)(nil),
	Methods:     []grpc.MethodDesc{{MethodName: "AnalyzeFile", Handler: _FileAnalyzer_AnalyzeFile_Handler}},
	Streams:     []grpc.StreamDesc{},
	Metadata:    "analyzer.proto",
}
