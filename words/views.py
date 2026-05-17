from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Word, UserWord
from .forms import AddWordForm


@login_required(login_url='authentication:login')
def word_list(request):
    """List all words in user's vocabulary"""
    user_words = UserWord.objects.filter(user=request.user).select_related('word').order_by('-added_at')

    # Filter by CEFR level if provided
    cefr_level = request.GET.get('level', '')
    if cefr_level:
        user_words = user_words.filter(word__cefr_level=cefr_level)

    # Search by word
    search_query = request.GET.get('search', '')
    if search_query:
        user_words = user_words.filter(
            Q(word__word__icontains=search_query) |
            Q(word__translation__icontains=search_query)
        )

    # Counts by CEFR level for simple tabs/filters
    counts_by_level = {level[0]: UserWord.objects.filter(user=request.user, word__cefr_level=level[0]).count() for level in Word.CEFR_LEVELS}
    # Prepare a list of (level, label, count) for template-friendly iteration
    cefr_with_counts = [(level, label, counts_by_level.get(level, 0)) for level, label in Word.CEFR_LEVELS]
    total_words = UserWord.objects.filter(user=request.user).count()
    # Count mastered words (accuracy > 80)
    mastered_count = 0
    for uw in UserWord.objects.filter(user=request.user):
        try:
            if uw.get_accuracy() and uw.get_accuracy() > 80:
                mastered_count += 1
        except Exception:
            continue

    context = {
        'user_words': user_words,
        'cefr_levels': Word.CEFR_LEVELS,
        'current_level': cefr_level,
        'search_query': search_query,
        'total_words': total_words,
        'counts_by_level': counts_by_level,
        'cefr_with_counts': cefr_with_counts,
        'mastered_count': mastered_count,
    }
    return render(request, 'words/word_list.html', context)


@login_required(login_url='authentication:login')
def add_word(request):
    """Add a new word to user's vocabulary"""
    if request.method == 'POST':
        form = AddWordForm(request.POST)
        if form.is_valid():
            # Get parsed word data from form
            word_text = form.cleaned_data['parsed_word']
            translation = form.cleaned_data['parsed_translation']
            cefr_level = form.cleaned_data['parsed_cefr_level']
            
            # Create or get the Word
            word, created = Word.objects.get_or_create(
                word=word_text,
                defaults={
                    'translation': translation,
                    'cefr_level': cefr_level,
                    'example_sentences': form.cleaned_data.get('parsed_example_sentences', ''),
                    'verb_forms': form.cleaned_data.get('parsed_verb_forms', ''),
                    'is_verb': form.cleaned_data.get('parsed_is_verb', False),
                }
            )

            if not created:
                updates = []
                if not word.example_sentences:
                    word.example_sentences = form.cleaned_data.get('parsed_example_sentences', '')
                    updates.append('example_sentences')
                if not word.verb_forms:
                    word.verb_forms = form.cleaned_data.get('parsed_verb_forms', '')
                    updates.append('verb_forms')
                if not word.is_verb and form.cleaned_data.get('parsed_is_verb', False):
                    word.is_verb = True
                    updates.append('is_verb')
                if updates:
                    word.save(update_fields=updates)
            
            # Add to user's vocabulary
            user_word, created = UserWord.objects.get_or_create(
                user=request.user,
                word=word,
            )
            
            if created:
                messages.success(
                    request,
                    f'✨ Word "{word_text}" has been added to your vocabulary!'
                )
            else:
                messages.info(
                    request,
                    f'ℹ️ You already have "{word_text}" in your vocabulary.'
                )
            
            return redirect('words:word_list')
    else:
        form = AddWordForm()
    
    context = {'form': form}
    return render(request, 'words/add_word.html', context)


@login_required(login_url='authentication:login')
def word_detail(request, pk):
    """View details of a specific word"""
    user_word = get_object_or_404(UserWord, pk=pk, user=request.user)
    
    context = {
        'user_word': user_word,
        'word': user_word.word,
        'accuracy': user_word.get_accuracy(),
    }
    return render(request, 'words/word_detail.html', context)


@login_required(login_url='authentication:login')
def delete_word(request, pk):
    """Remove a word from user's vocabulary"""
    user_word = get_object_or_404(UserWord, pk=pk, user=request.user)
    word_text = user_word.word.word
    
    if request.method == 'POST':
        user_word.delete()
        messages.success(request, f'✅ Word "{word_text}" has been removed from your vocabulary.')
        return redirect('words:word_list')
    
    context = {'user_word': user_word}
    return render(request, 'words/delete_word.html', context)
