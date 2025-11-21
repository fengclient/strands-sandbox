"""
Strands Sandbox - Sandbox tool integration for Strands Agents SDK

Provides unified interface for multiple sandbox backend implementations.
"""

from .code_interpreter import CodeInterpreter
from .e2bcodeinterpreter import E2BCodeInterpreter
from .models import (
    CodeInterpreterInput,
    ExecuteCodeAction,
    ExecuteCommandAction,
    FileContent,
    InitSessionAction,
    LanguageType,
    ListFilesAction,
    ListLocalSessionsAction,
    ReadFilesAction,
    RemoveFilesAction,
    WriteFilesAction,
)

__version__ = "0.1.0"

__all__ = [
    # Main classes
    "CodeInterpreter",
    "E2BCodeInterpreter",
    # Models
    "CodeInterpreterInput",
    "LanguageType",
    "FileContent",
    # Actions
    "InitSessionAction",
    "ListLocalSessionsAction",
    "ExecuteCodeAction",
    "ExecuteCommandAction",
    "ReadFilesAction",
    "WriteFilesAction",
    "ListFilesAction",
    "RemoveFilesAction",
]
