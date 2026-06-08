from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ai_service import GroqAIService
from .forms import PracticeMessageForm
from .models import PracticeMessage, PracticeSession
from .services import build_system_prompt, select_challenge_words


def _initial_message(words):
    word_list = ', '.join(item['word'] for item in words)
    return (
        'Write a German paragraph using all five challenge words. '
        f'Try to connect them naturally: {word_list}'
    )


@login_required(login_url='authentication:login')
def lab(request):
    session = PracticeSession.objects.filter(user=request.user).first()
    if not session:
        words = select_challenge_words(request.user)
        if len(words) < 5:
            return render(request, 'practice_lab/not_ready.html', {'word_count': len(words)})
        session = PracticeSession.objects.create(user=request.user, challenge_words=words)
        PracticeMessage.objects.create(
            session=session,
            role='assistant',
            content=_initial_message(words),
        )
    return redirect('practice_lab:session', pk=session.pk)


@login_required(login_url='authentication:login')
def session(request, pk):
    practice_session = get_object_or_404(PracticeSession, pk=pk, user=request.user)
    form = PracticeMessageForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        content = form.cleaned_data['message']
        PracticeMessage.objects.create(session=practice_session, role='user', content=content)
        conversation = [
            {'role': 'system', 'content': build_system_prompt(practice_session.challenge_words)},
            *[
                {'role': message.role, 'content': message.content}
                for message in practice_session.messages.all()
            ],
        ]
        try:
            response = GroqAIService().continue_practice_conversation(conversation)
        except Exception as error:
            messages.error(request, f'Practice Lab could not respond: {error}')
        else:
            PracticeMessage.objects.create(
                session=practice_session,
                role='assistant',
                content=response,
            )
        return redirect('practice_lab:session', pk=practice_session.pk)

    return render(request, 'practice_lab/session.html', {
        'practice_session': practice_session,
        'chat_messages': practice_session.messages.all(),
        'form': form,
    })


@login_required(login_url='authentication:login')
@require_POST
def close_session(request, pk):
    practice_session = get_object_or_404(PracticeSession, pk=pk, user=request.user)
    practice_session.delete()
    messages.success(request, 'Practice session closed. Its chat history has been deleted.')
    return redirect('home')
