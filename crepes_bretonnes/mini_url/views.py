
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from .forms import MiniURLForm
from .models import MiniURL
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def liste(request):
    """ Affichage des redirections """
    minis = MiniURL.objects.order_by('-nb_acces')

    return render(request, 'mini_url/liste.html', locals())


def nouveau(request):
    """ Ajout d'une redirection """
    if request.method == "POST":
        form = MiniURLForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(liste)
    else:
        form = MiniURLForm()

    return render(request, 'mini_url/nouveau.html', {'form': form})


def redirection(request, code):
    """ Redirection vers l'URL enregistrée """
    mini = get_object_or_404(MiniURL, code=code)
    mini.nb_acces += 1
    mini.save()

    return redirect(mini.url, permanent=True) #redirection permanente

class URLCreate(CreateView):
    model = MiniURL
    template_name = 'mini_url/nouveau.html'
    form_class = MiniURLForm
    success_url = reverse_lazy(liste)

class URLUpdate(UpdateView):
    model = MiniURL
    template_name = 'mini_url/nouveau.html'
    form_class = MiniURLForm
    success_url = reverse_lazy(liste)

    def get_object(self, queryset=None):
        code = self.kwargs.get('code', None)
        return get_object_or_404(MiniURL, code=code)
"""
 def form_valid(self, form):
        self.object = form.save()
        # Envoi d'un message à l'utilisateur
        messages.success(self.request, "Votre profil a été mis à jour avec succès.")
        return HttpResponseRedirect(self.get_success_url())
"""
class URLDelete(DeleteView):
    model = MiniURL
    context_object_name = "mini_url"
    template_name = 'mini_url/supprimer.html'
    success_url = reverse_lazy(liste)

    def get_object(self, queryset=None):
        code = self.kwargs.get('code', None)
        return get_object_or_404(MiniURL, code=code)


