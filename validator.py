import re


VALID_STATUSES = {
    "pending",
    "in_progress",
    "completed",
    "delayed"
}


def validate_action_items(response):

    issues = []
    seen_tasks = set()

    for index, task in enumerate(response.tasks, start=1):

        if not task.owner or not task.owner.strip():
            issues.append(
                f"Task {index}: Owner is missing."
            )

        if not task.deadline or not task.deadline.strip():
            issues.append(
                f"Task {index}: Deadline is missing."
            )

        if not 0 <= task.confidence <= 1:
            issues.append(
                f"Task {index}: Confidence must be between 0 and 1."
            )

        if task.status.lower() not in VALID_STATUSES:
            issues.append(
                f"Task {index}: Invalid status '{task.status}'."
            )

        normalized_task = re.sub(
            r"\s+",
            " ",
            task.task.strip().lower()
        )

        normalized_owner = (
            task.owner.strip().lower()
            if task.owner
            else ""
        )

        task_key = (
            normalized_task,
            normalized_owner
        )

        if task_key in seen_tasks:
            issues.append(
                f"Task {index}: Possible duplicate task."
            )
        else:
            seen_tasks.add(task_key)

    return issues