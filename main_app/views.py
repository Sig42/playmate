from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home_page(request):
    return render(request, 'base.html', {'data': 'Hello from view!'})

@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(user=request.user)  # Передаем пользователя
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm()
    return render(request, 'create_game.html', {'form': form})

