from difflib import SequenceMatcher


def normalize(text):

    if text is None:
        return ""

    return " ".join(
        str(text).lower().strip().split()
    )


def task_similarity(task1, task2):

    return SequenceMatcher(
        None,
        normalize(task1),
        normalize(task2)
    ).ratio()


def evaluate_action_items(predicted_response, ground_truth):

    predicted = [
        {
            "task": task.task,
            "owner": task.owner,
            "deadline": task.deadline,
            "status": task.status
        }
        for task in predicted_response.tasks
    ]

    matched_predictions = set()
    matched_ground_truth = set()

    correct_owner = 0
    correct_deadline = 0
    correct_status = 0

    for gt_index, gt in enumerate(ground_truth):

        best_match = None
        best_score = 0

        for pred_index, pred in enumerate(predicted):

            if pred_index in matched_predictions:
                continue

            score = task_similarity(
                gt["task"],
                pred["task"]
            )

            if score > best_score:
                best_score = score
                best_match = pred_index

        if best_match is not None and best_score >= 0.70:

            matched_predictions.add(best_match)
            matched_ground_truth.add(gt_index)

            pred = predicted[best_match]

            if normalize(pred["owner"]) == normalize(gt["owner"]):
                correct_owner += 1

            if normalize(pred["deadline"]) == normalize(gt["deadline"]):
                correct_deadline += 1

            if normalize(pred["status"]) == normalize(gt["status"]):
                correct_status += 1

    true_positive = len(matched_ground_truth)

    false_negative = len(ground_truth) - true_positive

    false_positive = len(predicted) - true_positive

    if true_positive + false_positive > 0:
        precision = true_positive / (
            true_positive + false_positive
        )
    else:
        precision = 0

    if true_positive + false_negative > 0:
        recall = true_positive / (
            true_positive + false_negative
        )
    else:
        recall = 0

    if precision + recall > 0:
        f1_score = (
            2 * precision * recall
            / (precision + recall)
        )
    else:
        f1_score = 0

    if true_positive > 0:

        owner_accuracy = correct_owner / true_positive

        deadline_accuracy = correct_deadline / true_positive

        status_accuracy = correct_status / true_positive

    else:

        owner_accuracy = 0
        deadline_accuracy = 0
        status_accuracy = 0

    return {
        "total_ground_truth": len(ground_truth),
        "total_predicted": len(predicted),
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "owner_accuracy": owner_accuracy,
        "deadline_accuracy": deadline_accuracy,
        "status_accuracy": status_accuracy
    }