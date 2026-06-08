from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
import time
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Word, UserWord
from .forms import AddWordForm, EditWordForm


WORD_METADATA_FIELDS = [
    'translation',
    'cefr_level',
    'example_sentences',
    'verb_forms',
    'is_verb',
    'is_noun',
    'singular_form',
    'plural_form',
    'masculine_form',
    'feminine_form',
]


def _parsed_word_metadata(cleaned_data):
    return {
        'translation': cleaned_data['parsed_translation'],
        'cefr_level': cleaned_data['parsed_cefr_level'],
        'example_sentences': cleaned_data.get('parsed_example_sentences', ''),
        'verb_forms': cleaned_data.get('parsed_verb_forms', ''),
        'is_verb': cleaned_data.get('parsed_is_verb', False),
        'is_noun': cleaned_data.get('parsed_is_noun', False),
        'singular_form': cleaned_data.get('parsed_singular_form', ''),
        'plural_form': cleaned_data.get('parsed_plural_form', ''),
        'masculine_form': cleaned_data.get('parsed_masculine_form', ''),
        'feminine_form': cleaned_data.get('parsed_feminine_form', ''),
    }


@login_required(login_url='authentication:login')
@never_cache
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
            Q(word__translation__icontains=search_query) |
            Q(word__singular_form__icontains=search_query) |
            Q(word__plural_form__icontains=search_query) |
            Q(word__masculine_form__icontains=search_query) |
            Q(word__feminine_form__icontains=search_query)
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
            input_text = form.cleaned_data['word']
            word_text = form.cleaned_data['parsed_word']
            word_defaults = _parsed_word_metadata(form.cleaned_data)
            
            word = Word.objects.filter(word__iexact=word_text).first()
            if not word:
                word = Word.objects.filter(word__iexact=input_text).first()
                if word:
                    word.word = word_text
                    for field, value in word_defaults.items():
                        setattr(word, field, value)
                    word.save(update_fields=['word', *word_defaults.keys()])
                else:
                    word = Word.objects.create(word=word_text, **word_defaults)

            else:
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
                for field in (
                    'singular_form',
                    'plural_form',
                    'masculine_form',
                    'feminine_form',
                ):
                    parsed_value = form.cleaned_data.get(f'parsed_{field}', '')
                    if not getattr(word, field) and parsed_value:
                        setattr(word, field, parsed_value)
                        updates.append(field)
                if not word.is_noun and form.cleaned_data.get('parsed_is_noun', False):
                    word.is_noun = True
                    updates.append('is_noun')
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
            
            return redirect(f"{reverse('words:word_list')}?refresh={int(time.time())}")
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
def edit_word(request, pk):
    """Edit a saved word's stored metadata."""
    user_word = get_object_or_404(UserWord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EditWordForm(request.POST, instance=user_word.word)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{form.instance.word}" has been updated.')
            return redirect('words:word_detail', pk=user_word.pk)
    else:
        form = EditWordForm(instance=user_word.word)

    return render(request, 'words/edit_word.html', {'form': form, 'user_word': user_word})


@login_required(login_url='authentication:login')
@require_POST
def refresh_word(request, pk):
    """Retrieve fresh AI metadata for a saved word."""
    user_word = get_object_or_404(UserWord, pk=pk, user=request.user)
    form = AddWordForm({'word': user_word.word.word})

    if not form.is_valid():
        messages.error(
            request,
            f'Could not retrieve fresh information: {form.errors.get("word", ["Unknown error"])[0]}',
        )
        return redirect('words:word_detail', pk=user_word.pk)

    word = user_word.word
    metadata = _parsed_word_metadata(form.cleaned_data)
    for field, value in metadata.items():
        setattr(word, field, value)
    word.save(update_fields=WORD_METADATA_FIELDS)
    messages.success(request, f'Information for "{word.word}" has been retrieved again.')
    return redirect('words:word_detail', pk=user_word.pk)


@login_required(login_url='authentication:login')
def delete_word(request, pk):
    """Remove a word from user's vocabulary"""
    user_word = get_object_or_404(UserWord, pk=pk, user=request.user)
    word_text = user_word.word.word
    
    if request.method == 'POST':
        user_word.delete()
        messages.success(request, f'✅ Word "{word_text}" has been removed from your vocabulary.')
        return redirect(f"{reverse('words:word_list')}?refresh={int(time.time())}")
    
    context = {'user_word': user_word}
    return render(request, 'words/delete_word.html', context)
