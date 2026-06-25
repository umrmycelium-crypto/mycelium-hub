def execute_policy(task, context):
    return {
        "intent": task.get("name") if isinstance(task, dict) else getattr(task, "intent", None),
        "status": "OK"
    }
