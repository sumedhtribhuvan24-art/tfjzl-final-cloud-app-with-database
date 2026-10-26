
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Question, Choice, Submission


def submit(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("choices")
        if not selected_ids:
            selected_ids = request.POST.getlist("choice")

        selected_choices = Choice.objects.filter(id__in=selected_ids)
        questions = Question.objects.all()

        score = selected_choices.filter(is_correct=True).aggregate(
            total=models.Sum("question__marks")
        )["total"] or 0

        submission = Submission.objects.create(
            user=request.user,
            score=score
        )
        submission.questions.set(questions)
        submission.selected_choices.set(selected_choices)

        return redirect("show_exam_result", submission_id=submission.id)

    questions = Question.objects.prefetch_related("choices").all()
    return render(
        request,
        "onlinecourseapp/mock_exam.html",
        {"questions": questions}
    )


def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        user=request.user
    )

    return render(
        request,
        "onlinecourseapp/exam_result.html",
        {"submission": submission}
    )
