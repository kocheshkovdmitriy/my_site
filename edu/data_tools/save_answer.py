from edu import models

def save_answer_task(answer, task_id, user_id, test_id=None):
    task = models.Task.objects.get(pk=task_id)
    status = answer == task.answer
    last_answer = models.Answer.objects.filter(task=task_id, user=user_id, test=test_id).first()
    print(last_answer, status)
    if last_answer:
        print('update')
        if not last_answer.status:
            last_answer.answer = answer
            last_answer.status = status
            last_answer.save()
    else:
        print('create')
        models.Answer.objects.create(answer=answer, task_id=task_id, user_id=user_id, test_id=test_id, status=status)
        return status
