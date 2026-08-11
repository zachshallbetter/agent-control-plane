"""Bounded retry/backoff primitives for coordinator work."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_seconds: float = 2.0
    max_seconds: float = 60.0
    def delay(self, attempt: int) -> float:
        if attempt < 1 or attempt >= self.max_attempts: return 0.0
        return min(self.max_seconds, self.base_seconds * (2 ** (attempt - 1)))
    def can_retry(self, attempt: int, retryable: bool) -> bool:
        return retryable and 0 < attempt < self.max_attempts
