from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

from articleapp.models import Article
from likeapp.models import LikeRecord

@transaction.atomic()
def db_transaction(user, article):
    like_record = LikeRecord.objects.filter(user=user, article=article)
    x = len(LikeRecord.objects.filter(article=article))
    if article.like != x:
        raise ValidationError('like already exists')
    elif like_record.exists():
        like_record.delete()
        article.like -= 1
        article.save()
        return 2
    else:
        LikeRecord(user=user, article=article).save()
        article.like += 1
        article.save()
        return 1




@method_decorator(login_required, 'get')
class LikeArticleView(RedirectView):
    def get(self, request, *args, **kwargs):
        user = request.user
        article = Article.objects.get(pk=kwargs['article_pk'])

        # try:
        #     db_transaction(user, article)
        #     messages.add_message(request, messages.SUCCESS, "좋아요 했따링")
        # except ValidationError:
        #     messages.add_message(request, messages.ERROR, "좋아요은 한번만...")
        #     return HttpResponseRedirect(reverse('articleapp:detail', kwargs={'pk': kwargs['article_pk']}))
        try:
            db_return = db_transaction(user, article)
            if db_return == 1:
                messages.add_message(request, messages.SUCCESS, "좋아요 완료~!!")
            elif db_return == 2:
                messages.add_message(request, messages.INFO, "좋아요 취소...")
        except:
            messages.add_message(request, messages.ERROR, "반영이 안됨")
            HttpResponseRedirect(reverse('articleapp:detail', kwargs={'pk': kwargs['article_pk']}))

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk':kwargs['article_pk']})