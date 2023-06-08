from edu import models

def save_answer_task(answer: str, task_id: int, user_id: int, test_id:int=None) -> bool:
    task = models.Task.objects.filter(pk=task_id).first()
    status = (answer == task.answer)
    last_answer = models.Answer.objects.filter(task=task_id, user=user_id, test=test_id).first()
    print(last_answer, status)
    if last_answer:
        print('update')
        if not last_answer.status or last_answer.test:
            last_answer.answer = answer
            last_answer.status = status
            last_answer.save()
    else:
        print('create')
        models.Answer.objects.create(answer=answer, task_id=task_id, user_id=user_id, test_id=test_id, status=status)
        return status

    return status


def save_answer_test(data: dict, user_id: int, test_id:int) -> None:
    res = sum([
        save_answer_task(answer=answer, task_id=task_id, user_id=user_id, test_id=test_id)
        for task_id, answer in data.items()
    ])
    models.TestAnswer.objects.create(test_id=test_id, user_id=user_id, status=round(res/len(data) * 100))
