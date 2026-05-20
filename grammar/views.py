from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ai_service import GroqAIService
from .models import (
    GrammarCoachEntry,
    GrammarExercise,
    GrammarExerciseAttempt,
    GrammarPracticeSession,
    GrammarTopic,
)


def _practice_key(slug):
    return f'grammar_practice_{slug}'


def _topic_progress(user):
    sessions = GrammarPracticeSession.objects.filter(user=user).select_related('topic')
    progress = {}
    for session in sessions:
        current = progress.get(session.topic_id)
        if current is None or session.accuracy() > current['accuracy']:
            progress[session.topic_id] = {
                'accuracy': session.accuracy(),
                'correct': session.correct,
                'total': session.total,
            }
    return progress


@login_required
def topic_list(request):
    topics = GrammarTopic.objects.prefetch_related('exercises')
    progress = _topic_progress(request.user)
    for topic in topics:
        item = progress.get(topic.id)
        if not item:
            topic.progress_label = 'Not started'
            topic.progress_class = 'bg-secondary text-muted-foreground'
        elif item['total'] and item['correct'] == item['total']:
            topic.progress_label = 'Mastered'
            topic.progress_class = 'bg-success text-white'
        else:
            topic.progress_label = f"Practiced {item['accuracy']}%"
            topic.progress_class = 'bg-accent text-white'

    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    topics_by_level = [
        {
            'level': level,
            'topics': [topic for topic in topics if topic.cefr_level == level],
        }
        for level in levels
    ]
    return render(request, 'grammar/index.html', {'topics_by_level': topics_by_level})


@login_required
def topic_detail(request, slug):
    topic = get_object_or_404(GrammarTopic.objects.prefetch_related('exercises'), slug=slug)
    best_session = GrammarPracticeSession.objects.filter(user=request.user, topic=topic).first()
    return render(request, 'grammar/topic_detail.html', {
        'topic': topic,
        'best_session': best_session,
    })


@login_required
def coach(request):
    entry = None
    recent_entries = GrammarCoachEntry.objects.filter(user=request.user)[:5]

    if request.method == 'POST':
        sentence = request.POST.get('sentence', '').strip()
        if not sentence:
            messages.error(request, 'Write a German sentence first.')
            return redirect('grammar:coach')

        try:
            result = GroqAIService().check_grammar(sentence)
            entry = GrammarCoachEntry.objects.create(
                user=request.user,
                sentence=sentence,
                corrected_sentence=result.get('corrected', ''),
                is_correct=bool(result.get('is_correct', False)),
                cefr_level=result.get('cefr_level', ''),
                topic=result.get('topic', ''),
                explanation=result.get('explanation', ''),
                mistakes=result.get('mistakes') or [],
                examples=result.get('examples') or [],
            )
            recent_entries = GrammarCoachEntry.objects.filter(user=request.user)[:5]
        except Exception as exc:
            messages.error(request, f'Grammar coach could not analyze that sentence yet: {exc}')

    return render(request, 'grammar/coach.html', {
        'entry': entry,
        'recent_entries': recent_entries,
    })


@login_required
def exercise(request, slug):
    topic = get_object_or_404(GrammarTopic.objects.prefetch_related('exercises'), slug=slug)
    exercises = list(topic.exercises.all())
    if not exercises:
        return render(request, 'grammar/exercise_empty.html', {'topic': topic})

    request.session[_practice_key(slug)] = {
        'exercise_ids': [exercise.id for exercise in exercises],
        'answers': {},
        'saved_session_id': None,
    }
    request.session.modified = True
    return redirect('grammar:exercise_question', slug=slug, position=0)


@login_required
def exercise_question(request, slug, position):
    topic = get_object_or_404(GrammarTopic, slug=slug)
    practice = request.session.get(_practice_key(slug))
    if not practice:
        return redirect('grammar:exercise', slug=slug)

    exercise_ids = practice.get('exercise_ids', [])
    if position >= len(exercise_ids):
        return redirect('grammar:exercise_results', slug=slug)

    exercise = get_object_or_404(GrammarExercise, id=exercise_ids[position], topic=topic)
    answers = practice.get('answers', {})
    submitted_answer = answers.get(str(exercise.id))
    selected = submitted_answer.get('selected') if submitted_answer else ''

    if request.method == 'POST' and not submitted_answer:
        selected = request.POST.get('answer', '')
        answers[str(exercise.id)] = {
            'selected': selected,
            'is_correct': selected == exercise.correct_option,
        }
        practice['answers'] = answers
        request.session[_practice_key(slug)] = practice
        request.session.modified = True
        submitted_answer = answers[str(exercise.id)]

    return render(request, 'grammar/exercise_question.html', {
        'topic': topic,
        'exercise': exercise,
        'position': position,
        'question_number': position + 1,
        'total': len(exercise_ids),
        'progress_percent': round((position / len(exercise_ids)) * 100) if exercise_ids else 0,
        'submitted_answer': submitted_answer,
        'selected': selected,
        'next_position': position + 1,
    })


@login_required
def exercise_results(request, slug):
    topic = get_object_or_404(GrammarTopic, slug=slug)
    practice = request.session.get(_practice_key(slug))
    if not practice:
        return redirect('grammar:exercise', slug=slug)

    exercise_ids = practice.get('exercise_ids', [])
    answers = practice.get('answers', {})
    exercises = list(GrammarExercise.objects.filter(id__in=exercise_ids, topic=topic))
    exercises.sort(key=lambda exercise: exercise_ids.index(exercise.id))
    correct = sum(1 for answer in answers.values() if answer.get('is_correct'))
    total = len(exercises)

    saved_session_id = practice.get('saved_session_id')
    if saved_session_id:
        practice_session = GrammarPracticeSession.objects.get(id=saved_session_id, user=request.user)
    else:
        practice_session = GrammarPracticeSession.objects.create(
            user=request.user,
            topic=topic,
            correct=correct,
            total=total,
        )
        for exercise in exercises:
            answer = answers.get(str(exercise.id), {})
            GrammarExerciseAttempt.objects.create(
                session=practice_session,
                exercise=exercise,
                selected_option=answer.get('selected', ''),
                is_correct=answer.get('is_correct', False),
            )
        practice['saved_session_id'] = practice_session.id
        request.session[_practice_key(slug)] = practice
        request.session.modified = True

    rows = []
    for exercise in exercises:
        answer = answers.get(str(exercise.id), {})
        rows.append({
            'exercise': exercise,
            'selected': answer.get('selected', ''),
            'is_correct': answer.get('is_correct', False),
        })

    return render(request, 'grammar/exercise_results.html', {
        'topic': topic,
        'practice_session': practice_session,
        'rows': rows,
        'correct': correct,
        'total': total,
        'accuracy': practice_session.accuracy(),
    })
