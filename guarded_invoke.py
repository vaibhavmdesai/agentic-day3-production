from test_production_invoke import production_invoke, InvocationResult, ErrorCategory
from test_circuit_breaker import CircuitBreaker

breaker = CircuitBreaker()


def guarded_invoke(messages: list) -> InvocationResult:
	if not breaker.allow_request():
		return InvocationResult(
			success=False,
			error="Circuit breaker open",
			error_category=ErrorCategory.UNKNOWN,
			attempts=0,
		)

	result = production_invoke(messages)
	if result.success:
		breaker.record_success()
	else:
		breaker.record_failure()
	return result