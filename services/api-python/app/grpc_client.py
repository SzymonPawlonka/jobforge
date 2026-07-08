from dataclasses import dataclass

import grpc

from app.config import get_settings
from app.proto import analyzer_pb2, analyzer_pb2_grpc


class AnalyzerUnavailableError(RuntimeError):
    pass


@dataclass(frozen=True)
class AnalysisResult:
    size_bytes: int
    character_count: int
    word_count: int
    line_count: int
    sha256: str

    def as_dict(self) -> dict[str, int | str]:
        return {
            "size_bytes": self.size_bytes,
            "character_count": self.character_count,
            "word_count": self.word_count,
            "line_count": self.line_count,
            "sha256": self.sha256,
        }


class GrpcAnalyzerClient:
    def analyze(self, filename: str, content: bytes) -> AnalysisResult:
        settings = get_settings()
        channel: grpc.Channel
        if settings.grpc_tls:
            channel = grpc.secure_channel(settings.grpc_target, grpc.ssl_channel_credentials())
        else:
            channel = grpc.insecure_channel(settings.grpc_target)
        try:
            stub = analyzer_pb2_grpc.FileAnalyzerStub(channel)
            response = stub.AnalyzeFile(
                analyzer_pb2.FileRequest(filename=filename, content=content),
                timeout=settings.grpc_timeout_seconds,
            )
            return AnalysisResult(
                size_bytes=response.size_bytes,
                character_count=response.character_count,
                word_count=response.word_count,
                line_count=response.line_count,
                sha256=response.sha256,
            )
        except grpc.RpcError as exc:
            code = exc.code().name if exc.code() else "UNKNOWN"
            details = exc.details() or str(exc)
            raise AnalyzerUnavailableError(f"gRPC {code}: {details}") from exc
        finally:
            channel.close()
