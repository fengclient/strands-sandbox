"""
E2B Code Interpreter Implementation

Code Interpreter implementation using E2B (https://e2b.dev) as sandbox backend.
Maintains a clean design focused on core functionality.
"""

import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from e2b_code_interpreter import code_interpreter_sync

from .code_interpreter import CodeInterpreter
from .models import (
    ExecuteCodeAction,
    ExecuteCommandAction,
    InitSessionAction,
    LanguageType,
    ListFilesAction,
    ReadFilesAction,
    RemoveFilesAction,
    WriteFilesAction,
)

logger = logging.getLogger(__name__)


class E2BCodeInterpreter(CodeInterpreter):
    """E2B-based Code Interpreter implementation"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        domain: Optional[str] = None,
        auto_create: bool = True,
        persist_sessions: bool = True,
        timeout: int = 300,
    ) -> None:
        """
        Initialize E2B Code Interpreter

        Args:
            api_key: E2B API Key, reads from E2B_API_KEY env var if not provided
            api_url: E2B API URL, optional (for custom endpoint)
            domain: E2B Domain, optional (for custom domain)
            auto_create: Whether to auto-create sessions, default True
            persist_sessions: Whether to persist sessions (skip cleanup on destruction), default True
            timeout: Sandbox timeout in seconds, default 300
        """
        super().__init__()
        self.api_key = api_key or os.getenv("E2B_API_KEY")
        if not self.api_key:
            raise ValueError("E2B API Key not provided. Set api_key parameter or E2B_API_KEY environment variable")

        self.api_url = api_url or os.getenv("E2B_API_URL")
        self.domain = domain or os.getenv("E2B_DOMAIN")
        self.auto_create = auto_create
        self.persist_sessions = persist_sessions
        self.timeout = timeout

        # Default session name
        self.default_session = f"session-{uuid.uuid4().hex[:12]}"

        # Session storage: session_name -> Sandbox
        self._sessions: Dict[str, code_interpreter_sync.Sandbox] = {}

        logger.info(
            f"Initialized E2B Code Interpreter: api_url={self.api_url or 'default'}, "
            f"auto_create={auto_create}, persist_sessions={persist_sessions}"
        )

    def start_platform(self) -> None:
        """E2B does not require platform-level initialization"""
        pass

    def cleanup_platform(self) -> None:
        """Clean up platform resources"""
        if not self._started:
            return

        if not self.persist_sessions:
            logger.info("Cleaning up E2B sandbox resources")
            for session_name, sandbox in list(self._sessions.items()):
                try:
                    sandbox.kill()
                    logger.debug(f"Closed session: {session_name}")
                except Exception as e:
                    logger.debug(f"Session {session_name} cleanup failed: {e}")

            self._sessions.clear()
            logger.info("E2B platform cleanup completed")
        else:
            logger.debug("Skipping cleanup - sessions persisted (persist_sessions=True)")

    def init_session(self, action: InitSessionAction) -> Dict[str, Any]:
        """Initialize a new E2B sandbox session"""
        session_name = action.session_name or self.default_session

        if session_name in self._sessions:
            return {
                "status": "error",
                "content": [{"text": f"Session '{session_name}' already exists"}]
            }

        try:
            logger.info(f"Creating E2B sandbox session: {session_name}")
            
            # Build creation parameters
            create_kwargs = {'api_key': self.api_key}
            if self.api_url:
                create_kwargs['api_url'] = self.api_url
            if self.domain:
                create_kwargs['domain'] = self.domain
            if self.timeout:
                create_kwargs['timeout'] = self.timeout
            
            sandbox = code_interpreter_sync.Sandbox.create(**create_kwargs)
            self._sessions[session_name] = sandbox

            logger.info(f"Session created successfully: {session_name} (ID: {sandbox.sandbox_id})")

            return {
                "status": "success",
                "content": [
                    {
                        "json": {
                            "sessionName": session_name,
                            "description": action.description,
                            "sessionId": sandbox.sandbox_id,
                        }
                    }
                ],
            }

        except Exception as e:
            logger.error(f"Failed to create session '{session_name}': {str(e)}")
            return {
                "status": "error",
                "content": [{"text": f"Failed to create session '{session_name}': {str(e)}"}],
            }

    def list_local_sessions(self) -> Dict[str, Any]:
        """List all local sessions"""
        sessions_info = []
        for name, sandbox in self._sessions.items():
            sessions_info.append({
                "sessionName": name,
                "sessionId": sandbox.sandbox_id,
            })

        return {
            "status": "success",
            "content": [
                {
                    "json": {
                        "sessions": sessions_info,
                        "totalSessions": len(sessions_info)
                    }
                }
            ],
        }

    def _ensure_session(self, session_name: Optional[str]) -> tuple[str, Optional[Dict[str, Any]]]:
        """
        Ensure session exists

        Args:
            session_name: Session name, uses default session if empty

        Returns:
            (session_name, error_dict) tuple, error_dict is None on success
        """
        target_session = session_name or self.default_session

        if target_session in self._sessions:
            return target_session, None

        if self.auto_create:
            logger.info(f"Auto-creating session: {target_session}")
            init_action = InitSessionAction(
                type="initSession",
                session_name=target_session,
                description="Auto-created session"
            )
            result = self.init_session(init_action)

            if result.get("status") != "success":
                return target_session, result

            return target_session, None

        # auto_create=False and session doesn't exist
        error_msg = f"Session '{target_session}' not found. Create it first using initSession"
        logger.error(error_msg)
        return target_session, {
            "status": "error",
            "content": [{"text": error_msg}]
        }

    def execute_code(self, action: ExecuteCodeAction) -> Dict[str, Any]:
        """Execute code"""
        session_name, error = self._ensure_session(action.session_name)
        if error:
            return error

        sandbox = self._sessions[session_name]
        logger.debug(f"Executing {action.language} code in session '{session_name}'")

        try:
            # Restart sandbox if context needs to be cleared
            if action.clear_context:
                logger.debug("Clearing context, restarting sandbox")
                sandbox.kill()
                
                create_kwargs = {'api_key': self.api_key}
                if self.api_url:
                    create_kwargs['api_url'] = self.api_url
                if self.domain:
                    create_kwargs['domain'] = self.domain
                if self.timeout:
                    create_kwargs['timeout'] = self.timeout
                
                sandbox = code_interpreter_sync.Sandbox.create(**create_kwargs)
                self._sessions[session_name] = sandbox

            # Language mapping: LanguageType -> E2B language
            language_map = {
                LanguageType.PYTHON: "python",
                LanguageType.JAVASCRIPT: "js",
                LanguageType.TYPESCRIPT: "ts",
                LanguageType.R: "r",
                LanguageType.JAVA: "java",
                LanguageType.BASH: "bash",
            }
            
            e2b_language = language_map.get(action.language, "python")
            
            # Execute code (pass language parameter)
            execution = sandbox.run_code(action.code, language=e2b_language)

            # Collect output
            output_parts = []
            
            # Add stdout
            if execution.logs and execution.logs.stdout:
                output_parts.extend([line.rstrip() for line in execution.logs.stdout if line.strip()])
            
            # Add stderr
            if execution.logs and execution.logs.stderr:
                stderr_lines = [line.rstrip() for line in execution.logs.stderr if line.strip()]
                if stderr_lines:
                    output_parts.append("[stderr]")
                    output_parts.extend(stderr_lines)
            
            # Add results (if any and not None)
            if execution.results:
                for result in execution.results:
                    if result is not None and result.text:
                        output_parts.append(f"=> {result.text}")

            output = "\n".join(output_parts) if output_parts else "(no output)"

            # Check for errors
            if execution.error:
                return {
                    "status": "error",
                    "content": [{"text": f"Execution error: {execution.error.name}\n{execution.error.value}"}]
                }

            return {
                "status": "success",
                "content": [{"text": output}]
            }

        except Exception as e:
            logger.error(f"Code execution failed: {str(e)}")
            return {
                "status": "error",
                "content": [{"text": f"Code execution failed: {str(e)}"}]
            }

    def execute_command(self, action: ExecuteCommandAction) -> Dict[str, Any]:
        """Execute shell command"""
        session_name, error = self._ensure_session(action.session_name)
        if error:
            return error

        sandbox = self._sessions[session_name]
        logger.debug(f"Executing command in session '{session_name}'")

        try:
            # Use run_code to execute shell command
            code = f"""
import subprocess
result = subprocess.run({repr(action.command)}, shell=True, capture_output=True, text=True)
print(result.stdout, end='')
if result.stderr:
    print('[stderr]', result.stderr, end='')
result.returncode
"""
            execution = sandbox.run_code(code)

            # Collect output
            output_parts = []
            if execution.logs and execution.logs.stdout:
                output_parts.extend([line.rstrip() for line in execution.logs.stdout if line.strip()])
            
            output = "\n".join(output_parts) if output_parts else "(no output)"
            
            # Get exit code
            exit_code = 0
            if execution.results and len(execution.results) > 0:
                result = execution.results[0]
                if result and result.text:
                    try:
                        exit_code = int(result.text)
                    except (ValueError, TypeError):
                        exit_code = 0

            if execution.error or exit_code != 0:
                return {
                    "status": "error",
                    "content": [{"text": f"Command execution failed (exit code: {exit_code}):\n{output}"}]
                }

            return {
                "status": "success",
                "content": [{"text": output}]
            }

        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return {
                "status": "error",
                "content": [{"text": f"Command execution failed: {str(e)}"}]
            }

    def read_files(self, action: ReadFilesAction) -> Dict[str, Any]:
        """Read files"""
        session_name, error = self._ensure_session(action.session_name)
        if error:
            return error

        sandbox = self._sessions[session_name]
        logger.debug(f"Reading {len(action.paths)} file(s) from session '{session_name}'")

        try:
            files_content = []
            for path in action.paths:
                # Use run_code to read file
                code = f"open({repr(path)}).read()"
                execution = sandbox.run_code(code)
                
                if execution.error:
                    return {
                        "status": "error",
                        "content": [{"text": f"Failed to read file {path}: {execution.error.value}"}]
                    }
                
                content = ""
                if execution.results and execution.results[0]:
                    content = execution.results[0].text or ""
                files_content.append({"path": path, "content": content})

            return {
                "status": "success",
                "content": [{"json": {"files": files_content}}]
            }

        except Exception as e:
            logger.error(f"File read failed: {str(e)}")
            return {
                "status": "error",
                "content": [{"text": f"File read failed: {str(e)}"}]
            }

    def write_files(self, action: WriteFilesAction) -> Dict[str, Any]:
        """Write files"""
        session_name, error = self._ensure_session(action.session_name)
        if error:
            return error

        sandbox = self._sessions[session_name]
        logger.debug(f"Writing {len(action.content)} file(s) to session '{session_name}'")

        try:
            for file_content in action.content:
                # Use run_code to write file
                code = f"""
with open({repr(file_content.path)}, 'w') as f:
    f.write({repr(file_content.text)})
"""
                execution = sandbox.run_code(code)
                
                if execution.error:
                    return {
                        "status": "error",
                        "content": [{"text": f"Failed to write file {file_content.path}: {execution.error.value}"}]
                    }

            return {
                "status": "success",
                "content": [{"text": f"Successfully wrote {len(action.content)} file(s)"}]
            }

        except Exception as e:
            logger.error(f"File write failed: {str(e)}")
            return {
                "status": "error",
                "content": [{"text": f"File write failed: {str(e)}"}]
            }

    def list_files(self, action: ListFilesAction) -> Dict[str, Any]:
        """List directory files"""
        session_name, error = self._ensure_session(action.session_name)
        if error:
            return error

        sandbox = self._sessions[session_name]
        logger.debug(f"Listing directory '{action.path}' in session '{session_name}'")

        try:
            # Use run_code to list files
            code = f"""
import os
import json
files = []
for item in os.listdir({repr(action.path)}):
    full_path = os.path.join({repr(action.path)}, item)
    files.append({{'name': item, 'type': 'dir' if os.path.isdir(full_path) else 'file'}})
json.dumps(files)
"""
            execution = sandbox.run_code(code)
            
            if execution.error:
                return {
                    "status": "error",
                    "content": [{"text": f"Failed to list files: {execution.error.value}"}]
                }
            
            file_list = []
            if execution.results and execution.results[0]:
                import json
                file_list = json.loads(execution.results[0].text)

            return {
                "status": "success",
                "content": [{"json": {"path": action.path, "files": file_list}}]
            }

        except Exception as e:
            logger.error(f"File listing failed: {str(e)}")
            return {
                "status": "error",
                "content": [{"text": f"File listing failed: {str(e)}"}]
            }

    def remove_files(self, action: RemoveFilesAction) -> Dict[str, Any]:
        """Remove files"""
        session_name, error = self._ensure_session(action.session_name)
        if error:
            return error

        sandbox = self._sessions[session_name]
        logger.debug(f"Removing {len(action.paths)} file(s) from session '{session_name}'")

        try:
            for path in action.paths:
                # Use run_code to remove file
                code = f"import os; os.remove({repr(path)})"
                execution = sandbox.run_code(code)
                
                if execution.error:
                    return {
                        "status": "error",
                        "content": [{"text": f"Failed to remove file {path}: {execution.error.value}"}]
                    }

            return {
                "status": "success",
                "content": [{"text": f"Successfully removed {len(action.paths)} file(s)"}]
            }

        except Exception as e:
            logger.error(f"File removal failed: {str(e)}")
            return {
                "status": "error",
                "content": [{"text": f"File removal failed: {str(e)}"}]
            }

    @staticmethod
    def get_supported_languages() -> List[LanguageType]:
        """Return list of supported programming languages"""
        return [
            LanguageType.PYTHON,
            LanguageType.JAVASCRIPT,
            LanguageType.TYPESCRIPT,
            LanguageType.R,
            LanguageType.JAVA,
            LanguageType.BASH,
        ]
