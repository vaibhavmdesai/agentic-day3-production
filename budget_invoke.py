from prod_invoke import production_invoke
from cost_tracking import SessionCostTracker

def budget_aware_invoke(tracker: SessionCostTracker, messages: list) -> str:
	if not tracker.check_budget():
		return "I've reached my session limit. Please start a new session."

	# Here you can use guarded_invoke / production_invoke / your graph
	result = production_invoke(messages)
	# For simplicity in this assignment, you can mock token usage or
	# read from response.usage_metadata if your model supports it.
	tracker.log_call(
		input_tokens=100,
		output_tokens=50,
		latency_ms=100.0,
		success=result.success,
	)
	return result.content if result.success else "Something went wrong."
