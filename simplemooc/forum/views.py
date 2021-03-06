import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView, View

from .forms import ReplyForm
from .models import Reply, Topic

# Create your views here.


# class ForumView(TemplateView):
#     template_name = 'forum/forum_index.html'

class ForumView(ListView):
    model = Topic
    paginate_by = 10
    template_name = 'forum/forum_index.html'

    def get_queryset(self):
        queryset = Topic.objects.all()
        order = self.request.GET.get('order', '')
        if order == 'recents':
            queryset = queryset.order_by('-created')
        elif order == 'views':
            queryset = queryset.order_by('-views')
        elif order == 'answers':
            queryset = queryset.order_by('-answers')
        # Filtrando por tag
        tag = self.kwargs.get('tag', '')
        if tag:
            queryset = queryset.filter(tags__slug__icontains=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Topic.tags.all()
        return context


class TopicView(DetailView):

    model = Topic
    template_name = 'forum/topic.html'

    def get(self, request, *args, **kwargs):
        response = super(TopicView, self).get(request, *args, **kwargs)
        if not (self.request.user.is_authenticated) or (self.object.author != self.request.user):
            self.object.views = self.object.views + 1
            self.object.save()
        return response

    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data(**kwargs)
        context['tags'] = Topic.tags.all()
        context['form'] = ReplyForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(request, 'Para responder, precisa estar logado.')
            return redirect(self.request.path)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(request, 'Resposta enviada com sucesso')
            context['form'] = ReplyForm()
        return self.render_to_response(context)


class ReplyChooseView(View):

    correct = True

    def get(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk, topic__author=request.user)
        reply.correct = self.correct
        reply.save()
        message = 'Resposta atualizada com sucesso'
        if request.is_ajax():
            data = {'success': True, 'message': message}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            messages.success(request, message)
            return redirect(reply.topic.get_absolute_url())
