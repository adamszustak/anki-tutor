class NoRequiredVarEnv(Exception):
    """Exception raised when required env vars are missing."""

    def __init__(self, env_name: str) -> None:
        self.msg = (
            f"Script cannot find required environment variable {env_name}."
        )

    def __str__(self) -> str:
        return self.msg
