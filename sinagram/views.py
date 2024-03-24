from django.shortcuts import render
from users.decorators import profile_required

@profile_required
def index_view(request):
    return  render(request, 'home/index.html')