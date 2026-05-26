from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from Vocab_Buddy.streaks import get_user_streak_days
from words.models import UserWord, Word
from .forms import ReviewForm, QuizAnswerForm
from .models import QuizResult, ReviewSession
from .scheduler import SpacedRepetitionScheduler
import random


def index(request):
    return render(request, 'learning/index.html')


def home(request):
    """Render the dashboard-style home page using user's vocabulary stats."""
    context = {}
    if request.user.is_authenticated:
        uwords = list(UserWord.objects.filter(user=request.user).select_related('word'))
        total_words = len(uwords)
        mastered_words = 0
        review_due = 0
        streak_days = get_user_streak_days(request.user)
        for uw in uwords:
            try:
                acc = uw.get_accuracy()
            except Exception:
                acc = 0
            if acc and acc > 80:
                mastered_words += 1
            if not uw.last_reviewed:
                review_due += 1

        stats = [
            {'label': 'Total Words', 'value': total_words, 'color': 'bg-primary'},
            {'label': 'Words Mastered', 'value': mastered_words, 'color': 'bg-success'},
            {'label': 'Study Streak', 'value': f'🔥 {streak_days} day streak' if streak_days else '🔥 Start your streak', 'color': 'bg-accent'},
            {'label': 'Review Due', 'value': review_due, 'color': 'bg-chart-4'},
        ]
        today = timezone.localdate()
        start_day = today - timedelta(days=6)
        counts_by_day = {start_day + timedelta(days=offset): 0 for offset in range(7)}

        for uw in uwords:
            added_day = timezone.localdate(uw.added_at)
            if start_day <= added_day <= today:
                counts_by_day[added_day] += 1

        weekly_data = []
        max_words = max(counts_by_day.values(), default=0)
        chart_max = max(1, max_words)
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        for offset in range(7):
            current_day = start_day + timedelta(days=offset)
            count = counts_by_day[current_day]
            weekly_data.append({
                'day': day_names[current_day.weekday()],
                'date': current_day.strftime('%b %d'),
                'words': count,
                'height': max(8, round((count / chart_max) * 100)) if count else 8,
                'is_today': current_day == today,
            })

        weekly_total = sum(point['words'] for point in weekly_data)

        context.update({
            'stats': stats,
            'weekly_data': weekly_data,
            'weekly_total': weekly_total,
            'weekly_start_label': start_day.strftime('%b %d'),
            'weekly_end_label': today.strftime('%b %d'),
        })

    return render(request, 'home.html', context)


def _parse_examples(raw_examples):
    lines = [line.strip() for line in (raw_examples or '').splitlines() if line.strip()]
    return lines[:2]


def _parse_verb_forms(raw_text):
    rows = []
    meta = {
        'verb': '',
        'meaning': '',
        'type': '',
        'participle': '',
        'auxiliary': '',
    }
    present_rows = []
    past_rows = []
    section = None

    for line in [line.strip() for line in (raw_text or '').splitlines() if line.strip()]:
        if line.startswith('VERB:'):
            meta['verb'] = line.split(':', 1)[1].strip()
            continue
        if line.startswith('MEANING:'):
            meta['meaning'] = line.split(':', 1)[1].strip()
            continue
        if line.startswith('TYPE:'):
            meta['type'] = line.split(':', 1)[1].strip()
            continue
        if line.startswith('PRESENT TENSE:'):
            section = 'present'
            continue
        if line.startswith('PAST TENSE'):
            section = 'past'
            continue
        if line.startswith('PERFECT TENSE:'):
            section = 'perfect'
            continue
        if section == 'perfect':
            if line.startswith('Past Participle:'):
                meta['participle'] = line.split(':', 1)[1].strip()
            elif line.startswith('Auxiliary:'):
                meta['auxiliary'] = line.split(':', 1)[1].strip()
            continue
        if section in {'present', 'past'}:
            parts = line.split(None, 1)
            if len(parts) == 2:
                row = {'pronoun': parts[0].strip(), 'form': parts[1].strip()}
                if section == 'present':
                    present_rows.append(row)
                else:
                    past_rows.append(row)

    return {
        'meta': meta,
        'present_rows': present_rows,
        'past_rows': past_rows,
    }


@login_required
def review_start(request):
    """Start review session with per-word learning content."""
    uwords_qs = UserWord.objects.filter(user=request.user).select_related('word')
    if not uwords_qs.exists():
        return render(request, 'learning/review_done.html')

    level_map = {'A1': 0, 'A2': 1, 'B1': 2, 'B2': 3, 'C1': 4, 'C2': 5}
    cards = []

    def weighted_sample(items, weights, count):
        selected = []
        pool_items = list(items)
        pool_weights = list(weights)
        for _ in range(min(count, len(pool_items))):
            total = sum(pool_weights)
            if total <= 0:
                selected.extend(pool_items)
                break
            pick = random.uniform(0, total)
            running = 0
            chosen_index = 0
            for idx, weight in enumerate(pool_weights):
                running += weight
                if running >= pick:
                    chosen_index = idx
                    break
            selected.append(pool_items.pop(chosen_index))
            pool_weights.pop(chosen_index)
        return selected

    for uw in uwords_qs:
        review_count = uw.review_count or 0
        correct_count = uw.correct_count or 0
        incorrect = max(0, review_count - correct_count)
        level_weight = level_map.get(uw.word.cefr_level, 0)
        new_word_boost = 5 if review_count == 0 else 0
        weight = 1 + incorrect * 3 + level_weight + new_word_boost

        examples = _parse_examples(uw.word.example_sentences or '')
        verb_forms_raw = uw.word.verb_forms or ''
        is_verb = uw.word.is_verb or bool(verb_forms_raw)
        verb_forms_data = _parse_verb_forms(verb_forms_raw) if is_verb and verb_forms_raw else None

        cards.append({
            'pk': uw.pk,
            'front': uw.word.word,
            'back': uw.word.translation,
            'level': uw.word.cefr_level,
            'weight': weight,
            'examples': examples,
            'is_verb': is_verb,
            'verb_forms_data': verb_forms_data,
        })

    if len(cards) > 10:
        weights = [card['weight'] for card in cards]
        cards = weighted_sample(cards, weights, 10)
    cards.sort(key=lambda card: card['weight'], reverse=True)

    import json
    cards_json_str = json.dumps(cards, ensure_ascii=False)

    context = {
        'uwords': uwords_qs,
        'cards_json_str': cards_json_str,
        'cards': cards,
    }
    return render(request, 'learning/review_session.html', context)


@login_required
def review_next(request):
    """Complete review session: mark all words as reviewed"""
    if request.method == 'POST':
        # Accept reviewed pks from the client (comma-separated) and mark them reviewed
        pks_csv = request.POST.get('reviewed_pks', '')
        pks = [int(x) for x in pks_csv.split(',') if x.strip().isdigit()]
        incorrect_csv = request.POST.get('incorrect_pks', '')
        incorrect_pks = {int(x) for x in incorrect_csv.split(',') if x.strip().isdigit()}
        for pk in pks:
            try:
                uword = UserWord.objects.get(pk=pk, user=request.user)
                uword.review_count = (uword.review_count or 0) + 1
                if pk not in incorrect_pks:
                    uword.correct_count = (uword.correct_count or 0) + 1
                uword.last_reviewed = timezone.now()
                uword.save()
            except UserWord.DoesNotExist:
                pass
        return render(request, 'learning/review_done.html')
    
    return redirect('learning:review_start')


@login_required
def quiz_start(request):
    """Start quiz: select 5 words and generate multiple-choice questions"""
    # Get up to 5 random words from user's vocabulary
    user_words = list(UserWord.objects.filter(user=request.user).values_list('word__word', 'word__translation', 'pk'))
    if len(user_words) < 4:
        return render(request, 'learning/quiz_insufficient.html', {'needed': 4, 'have': len(user_words)})
    
    quiz_words = random.sample(user_words, min(5, len(user_words)))
    questions = []
    
    # Generate multiple-choice questions
    for word_text, translation, word_pk in quiz_words:
        # Get 3 wrong answers from other words
        other_translations = [w[1] for w in user_words if w[0] != word_text]
        wrong_answers = random.sample(other_translations, min(3, len(other_translations)))
        
        # Create options list
        options = [translation] + wrong_answers[:3]
        random.shuffle(options)
        correct_idx = options.index(translation)
        
        questions.append({
            'word': word_text,
            'translation': translation,
            'options': options,
            'correct': correct_idx
        })
    
    request.session['quiz_questions'] = questions
    request.session['quiz_answers'] = []
    request.session['quiz_score'] = 0
    return redirect('learning:quiz_question', qid=0)


@login_required
def quiz_question(request, qid):
    """Show quiz question with multiple-choice options"""
    questions = request.session.get('quiz_questions', [])
    if qid >= len(questions):
        return redirect('learning:quiz_results')

    question = questions[qid]
    
    if request.method == 'POST':
        selected_idx = int(request.POST.get('answer', -1))
        is_correct = selected_idx == question['correct']
        
        quiz_answers = request.session.get('quiz_answers', [])
        quiz_answers.append({
            'question': question['word'],
            'correct_answer': question['translation'],
            'user_answer': question['options'][selected_idx] if 0 <= selected_idx < len(question['options']) else 'Invalid',
            'is_correct': is_correct
        })
        request.session['quiz_answers'] = quiz_answers
        
        if is_correct:
            request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
        
        return redirect('learning:quiz_question', qid=qid+1)
    
    # Display multiple-choice question
    progress_percent = int((qid / len(questions)) * 100) if len(questions) > 0 else 0
    option_letters = ['A', 'B', 'C', 'D']
    options_with_labels = list(zip(option_letters, question['options']))
    context = {
        'question_num': qid + 1,
        'total_questions': len(questions),
        'word': question['word'],
        'options': question['options'],
        'options_with_labels': options_with_labels,

        'qid': qid,
        'progress_percent': progress_percent,
    }
    return render(request, 'learning/quiz_question.html', context)


@login_required
def quiz_results(request):
    """Display quiz results"""
    answers = request.session.get('quiz_answers', [])
    total = len(answers)
    correct = sum(1 for a in answers if a.get('is_correct'))

    if request.user.is_authenticated and total > 0:
        QuizResult.objects.create(user=request.user, total=total, correct=correct)
        for ans in answers:
            try:
                uw = UserWord.objects.get(user=request.user, word__word=ans.get('question'))
                uw.review_count = (uw.review_count or 0) + 1
                if ans.get('is_correct'):
                    uw.correct_count = (uw.correct_count or 0) + 1
                uw.last_reviewed = timezone.now()
                uw.save()
            except UserWord.DoesNotExist:
                continue

    return render(request, 'learning/quiz_results.html', {'answers': answers, 'total': total, 'correct': correct})


@login_required
def verb_info(request, verb):
    """Display verb conjugation info from AI"""
    svc = GroqAIService()
    info = svc.get_verb_info(verb)
    return render(request, 'learning/verb_info.html', {'verb': verb, 'info': info})
