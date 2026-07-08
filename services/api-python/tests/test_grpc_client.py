from unittest.mock import Mock, patch

from app.grpc_client import GrpcAnalyzerClient
from app.proto import analyzer_pb2


def test_grpc_client_maps_response():
    channel = Mock()
    stub = Mock()
    stub.AnalyzeFile.return_value = analyzer_pb2.FileAnalysis(
        size_bytes=3,
        character_count=3,
        word_count=1,
        line_count=1,
        sha256="abc",
    )
    with (
        patch("app.grpc_client.grpc.insecure_channel", return_value=channel),
        patch("app.grpc_client.analyzer_pb2_grpc.FileAnalyzerStub", return_value=stub),
    ):
        result = GrpcAnalyzerClient().analyze("x.txt", b"abc")

    assert result.as_dict() == {
        "size_bytes": 3,
        "character_count": 3,
        "word_count": 1,
        "line_count": 1,
        "sha256": "abc",
    }
    stub.AnalyzeFile.assert_called_once()
    channel.close.assert_called_once()
