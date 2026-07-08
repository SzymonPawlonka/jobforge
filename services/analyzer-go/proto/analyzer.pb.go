// Code generated manually to match analyzer.proto. DO NOT EDIT.
// source: analyzer.proto

package analyzerpb

import (
	reflect "reflect"
	sync "sync"

	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
)

const (
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type FileRequest struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Filename      string                 `protobuf:"bytes,1,opt,name=filename,proto3" json:"filename,omitempty"`
	Content       []byte                 `protobuf:"bytes,2,opt,name=content,proto3" json:"content,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *FileRequest) Reset() {
	*x = FileRequest{}
	mi := &file_analyzer_proto_msgTypes[0]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}
func (x *FileRequest) String() string { return protoimpl.X.MessageStringOf(x) }
func (*FileRequest) ProtoMessage()    {}
func (x *FileRequest) ProtoReflect() protoreflect.Message {
	mi := &file_analyzer_proto_msgTypes[0]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use FileRequest.ProtoReflect.Descriptor instead.
func (*FileRequest) Descriptor() ([]byte, []int) { return file_analyzer_proto_rawDescGZIP(), []int{0} }
func (x *FileRequest) GetFilename() string {
	if x != nil {
		return x.Filename
	}
	return ""
}
func (x *FileRequest) GetContent() []byte {
	if x != nil {
		return x.Content
	}
	return nil
}

type FileAnalysis struct {
	state          protoimpl.MessageState `protogen:"open.v1"`
	SizeBytes      int64                  `protobuf:"varint,1,opt,name=size_bytes,json=sizeBytes,proto3" json:"size_bytes,omitempty"`
	CharacterCount int64                  `protobuf:"varint,2,opt,name=character_count,json=characterCount,proto3" json:"character_count,omitempty"`
	WordCount      int64                  `protobuf:"varint,3,opt,name=word_count,json=wordCount,proto3" json:"word_count,omitempty"`
	LineCount      int64                  `protobuf:"varint,4,opt,name=line_count,json=lineCount,proto3" json:"line_count,omitempty"`
	Sha256         string                 `protobuf:"bytes,5,opt,name=sha256,proto3" json:"sha256,omitempty"`
	unknownFields  protoimpl.UnknownFields
	sizeCache      protoimpl.SizeCache
}

func (x *FileAnalysis) Reset() {
	*x = FileAnalysis{}
	mi := &file_analyzer_proto_msgTypes[1]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}
func (x *FileAnalysis) String() string { return protoimpl.X.MessageStringOf(x) }
func (*FileAnalysis) ProtoMessage()    {}
func (x *FileAnalysis) ProtoReflect() protoreflect.Message {
	mi := &file_analyzer_proto_msgTypes[1]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use FileAnalysis.ProtoReflect.Descriptor instead.
func (*FileAnalysis) Descriptor() ([]byte, []int) { return file_analyzer_proto_rawDescGZIP(), []int{1} }
func (x *FileAnalysis) GetSizeBytes() int64 {
	if x != nil {
		return x.SizeBytes
	}
	return 0
}
func (x *FileAnalysis) GetCharacterCount() int64 {
	if x != nil {
		return x.CharacterCount
	}
	return 0
}
func (x *FileAnalysis) GetWordCount() int64 {
	if x != nil {
		return x.WordCount
	}
	return 0
}
func (x *FileAnalysis) GetLineCount() int64 {
	if x != nil {
		return x.LineCount
	}
	return 0
}
func (x *FileAnalysis) GetSha256() string {
	if x != nil {
		return x.Sha256
	}
	return ""
}

var File_analyzer_proto protoreflect.FileDescriptor

var file_analyzer_proto_rawDesc = []byte{
	0x0a, 0x0e, 0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72, 0x2e, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x12, 0x08, 0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a,
	0x65, 0x72, 0x22, 0x30, 0x0a, 0x0b, 0x46, 0x69, 0x6c, 0x65, 0x52, 0x65,
	0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x10, 0x0a, 0x08, 0x66, 0x69, 0x6c,
	0x65, 0x6e, 0x61, 0x6d, 0x65, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x12,
	0x0f, 0x0a, 0x07, 0x63, 0x6f, 0x6e, 0x74, 0x65, 0x6e, 0x74, 0x18, 0x02,
	0x20, 0x01, 0x28, 0x0c, 0x22, 0x73, 0x0a, 0x0c, 0x46, 0x69, 0x6c, 0x65,
	0x41, 0x6e, 0x61, 0x6c, 0x79, 0x73, 0x69, 0x73, 0x12, 0x12, 0x0a, 0x0a,
	0x73, 0x69, 0x7a, 0x65, 0x5f, 0x62, 0x79, 0x74, 0x65, 0x73, 0x18, 0x01,
	0x20, 0x01, 0x28, 0x03, 0x12, 0x17, 0x0a, 0x0f, 0x63, 0x68, 0x61, 0x72,
	0x61, 0x63, 0x74, 0x65, 0x72, 0x5f, 0x63, 0x6f, 0x75, 0x6e, 0x74, 0x18,
	0x02, 0x20, 0x01, 0x28, 0x03, 0x12, 0x12, 0x0a, 0x0a, 0x77, 0x6f, 0x72,
	0x64, 0x5f, 0x63, 0x6f, 0x75, 0x6e, 0x74, 0x18, 0x03, 0x20, 0x01, 0x28,
	0x03, 0x12, 0x12, 0x0a, 0x0a, 0x6c, 0x69, 0x6e, 0x65, 0x5f, 0x63, 0x6f,
	0x75, 0x6e, 0x74, 0x18, 0x04, 0x20, 0x01, 0x28, 0x03, 0x12, 0x0e, 0x0a,
	0x06, 0x73, 0x68, 0x61, 0x32, 0x35, 0x36, 0x18, 0x05, 0x20, 0x01, 0x28,
	0x09, 0x32, 0x4c, 0x0a, 0x0c, 0x46, 0x69, 0x6c, 0x65, 0x41, 0x6e, 0x61,
	0x6c, 0x79, 0x7a, 0x65, 0x72, 0x12, 0x3c, 0x0a, 0x0b, 0x41, 0x6e, 0x61,
	0x6c, 0x79, 0x7a, 0x65, 0x46, 0x69, 0x6c, 0x65, 0x12, 0x15, 0x2e, 0x61,
	0x6e, 0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72, 0x2e, 0x46, 0x69, 0x6c, 0x65,
	0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x16, 0x2e, 0x61, 0x6e,
	0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72, 0x2e, 0x46, 0x69, 0x6c, 0x65, 0x41,
	0x6e, 0x61, 0x6c, 0x79, 0x73, 0x69, 0x73, 0x42, 0x44, 0x5a, 0x42, 0x67,
	0x69, 0x74, 0x68, 0x75, 0x62, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x73, 0x65,
	0x64, 0x69, 0x74, 0x74, 0x69, 0x73, 0x2f, 0x6a, 0x6f, 0x62, 0x66, 0x6f,
	0x72, 0x67, 0x65, 0x2f, 0x73, 0x65, 0x72, 0x76, 0x69, 0x63, 0x65, 0x73,
	0x2f, 0x61, 0x6e, 0x61, 0x6c, 0x79, 0x7a, 0x65, 0x72, 0x2d, 0x67, 0x6f,
	0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x3b, 0x61, 0x6e, 0x61, 0x6c, 0x79,
	0x7a, 0x65, 0x72, 0x70, 0x62, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x33,
}

var (
	file_analyzer_proto_rawDescOnce sync.Once
	file_analyzer_proto_rawDescData = file_analyzer_proto_rawDesc
)

func file_analyzer_proto_rawDescGZIP() []byte {
	file_analyzer_proto_rawDescOnce.Do(func() { file_analyzer_proto_rawDescData = protoimpl.X.CompressGZIP(file_analyzer_proto_rawDescData) })
	return file_analyzer_proto_rawDescData
}

var file_analyzer_proto_msgTypes = make([]protoimpl.MessageInfo, 2)
var file_analyzer_proto_goTypes = []any{(*FileRequest)(nil), (*FileAnalysis)(nil)}
var file_analyzer_proto_depIdxs = []int32{
	0, // 0: analyzer.FileAnalyzer.AnalyzeFile:input_type -> analyzer.FileRequest
	1, // 1: analyzer.FileAnalyzer.AnalyzeFile:output_type -> analyzer.FileAnalysis
	1, // [1:2] is the sub-list for method output_type
	0, // [0:1] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_analyzer_proto_init() }
func file_analyzer_proto_init() {
	if File_analyzer_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_analyzer_proto_msgTypes[0].Exporter = func(v any, i int) any {
			switch v := v.(*FileRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_analyzer_proto_msgTypes[1].Exporter = func(v any, i int) any {
			switch v := v.(*FileAnalysis); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{File: protoimpl.DescBuilder{GoPackagePath: reflect.TypeOf(x{}).PkgPath(), RawDescriptor: file_analyzer_proto_rawDesc, NumEnums: 0, NumMessages: 2, NumExtensions: 0, NumServices: 1}, GoTypes: file_analyzer_proto_goTypes, DependencyIndexes: file_analyzer_proto_depIdxs, MessageInfos: file_analyzer_proto_msgTypes}.Build()
	File_analyzer_proto = out.File
	file_analyzer_proto_rawDesc = nil
	file_analyzer_proto_goTypes = nil
	file_analyzer_proto_depIdxs = nil
}
