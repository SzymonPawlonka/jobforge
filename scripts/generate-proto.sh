#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROTO="$ROOT_DIR/services/analyzer-go/proto/analyzer.proto"
PY_OUT="$ROOT_DIR/services/api-python/app/proto"
GO_OUT="$ROOT_DIR/services/analyzer-go"

python -m pip install "grpcio-tools==1.81.1"
GOBIN="$(go env GOPATH)/bin"
export PATH="$GOBIN:$PATH"
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.36.6
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.5.1

mkdir -p "$PY_OUT"
touch "$PY_OUT/__init__.py"
python -m grpc_tools.protoc \
  -I "$(dirname "$PROTO")" \
  --python_out="$PY_OUT" \
  --grpc_python_out="$PY_OUT" \
  "$PROTO"

# grpc_tools generuje import bez prefiksu pakietu; poprawiamy go dla app.proto.
sed -i.bak 's/^import analyzer_pb2 as analyzer__pb2/from app.proto import analyzer_pb2 as analyzer__pb2/' "$PY_OUT/analyzer_pb2_grpc.py"
rm -f "$PY_OUT/analyzer_pb2_grpc.py.bak"

python -m grpc_tools.protoc \
  -I "$(dirname "$PROTO")" \
  --plugin=protoc-gen-go="$GOBIN/protoc-gen-go" \
  --plugin=protoc-gen-go-grpc="$GOBIN/protoc-gen-go-grpc" \
  --go_out="$GO_OUT/proto" --go_opt=paths=source_relative \
  --go-grpc_out="$GO_OUT/proto" --go-grpc_opt=paths=source_relative \
  "$PROTO"

# Przy source_relative pliki lądują w proto/. Go package w .proto ma nazwę analyzerpb.
echo "Kod gRPC wygenerowany."
