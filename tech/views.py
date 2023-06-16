from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import requests
from accounts.models import Users
from config.utils.login_required import login_check
from tech.forms import CommentForm, BugReportForm
from tech.models import Post, Profile, Bug

@login_check
def first(request, category):
    user = Users.objects.all()
    post_list = Post.objects.filter(category=category).all()

    return render(request, "tech/tech/main.html", {
        "post_list" : post_list,
        "user" : user,
    })

@login_check
def seconds(request, pk):
    post = get_object_or_404(Post, pk=pk)
    profile = Profile.objects.filter(name='Eno7')




    comment_form = CommentForm()

    viewed= request.session.get('viewed_posts', [])
    if pk not in viewed:
        post.view_count += 1
        post.save()
        viewed.append(pk)
        request.session['viewed_posts'] = viewed

    viewed = len(set(viewed))

    return render(request, "tech/tech/demo.html", {
        "post": post,
        "profile": profile,
        "comment_form": comment_form,
        "viewed" : viewed,
    })

@login_check
def index(request):
    post_list = Post.objects.all()

    comment_form = CommentForm()

    return render(request, "tech/tech/index.html", {
        "post_list": post_list,
        "comment_form": comment_form,
    })

@login_check
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, f"{post.author}님 댓글이 성공적으로 등록되었습니다!")
            if request.is_ajax():
                return render(request, "tech/tech/_comment.html", {
                    "comment": comment,
                })
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "tech/tech/comment_form.html", {
        "form": form,
    })
@login_check
def donate(request):
    user = Users.objects.all()
    return render(request, 'tech/tech/donate.html', {
        "user" : user,
    })


@login_check
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    author = post.author
    messages.success(request, f"{author}님을 팔로우합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_check
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    author = post.author
    messages.warning(request, f"{author}님의 팔로우를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)
@login_check
def bug_search(request):
    query = request.GET.get('q')
    if query:
        bugs = Bug.objects.filter(title__icontains=query) or Bug.objects.filter(description__icontains=query).distinct()
    else:
        bugs = Bug.objects.all()
    return render(request, 'tech/bug/search.html', {'bugs': bugs, 'query': query})
@login_check
def bug_report_success(request):
    bug_list = Bug.objects.filter(author=request.user).values('id',
                                                              'status',
                                                              'description',
                                                              'image',
                                                              'created_at',
                                                              'title',
                                                              'category')

    status_list = Bug.objects.filter(author=request.user).values('id', 'status')

    return render(request, 'tech/bug/bug_report_success.html',{
        "bug_list" : bug_list,
        "status_list" : status_list,
    })
@login_check
def bug_report(request):
    user = Users.objects.all()
    bug_list = Bug.objects.filter(author=request.user)
    if request.method == 'POST':
        form = BugReportForm(request.POST, request.FILES)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.author = request.user
            bug.bug_rock = min(bug.author.bug_set.count() + 1, 100)
            bug.status = 'None'
            if bug.bug_rock >5:
                messages.error(request, "5개 이상은 제보하실 수 없습니다.")
                return redirect('tech:bug_success')
            bug.save()
            bug.bug_rock += 1
            bug.author.save()
            bug.refresh_from_db()
            messages.success(request, f"{bug.author}님 감사합니다! 검토 후 빠르게 해결하도록 하겠습니다.")
            return redirect('tech:bug_success')
    else:
        form = BugReportForm()
    return render(request, 'tech/bug/bug_report.html', {
        'form': form,
        "bug_list": bug_list,
    })

@login_check
def bug_report_modify(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    bug_list = Bug.objects.filter(author=request.user)
    if request.user != bug.author:
        messages.error(request, 'Error!')
        return redirect('tech:bug_success')
    if request.method == "POST":
        bug_form = BugReportForm(request.POST, request.FILES, instance=bug)
        if bug_form.is_valid():
            bug = bug_form.save(commit=False)
            bug.updated_at = timezone.now()
            bug.save()
            return redirect('tech:bug_success')
    else:
        form = BugReportForm(instance=bug)
    return render(request, 'tech/bug/bug_report.html', {
        'form' : form,
        'bug_list' : bug_list,
    })

@login_check
def bug_report_delete(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    if request.user == bug.author:
        bug.delete()
    else:
        messages.error(request, 'Error')
        return redirect('tech:bug_success', pk=bug.id)

def test(request):
    post = Post.objects.filter(author=request.user).select_related('author')

    post_nickname = post.author.nickname
    post_staff = post.author.is_staff
    post_avatar = post.author.avatar

    return render(request, 'trash_html/../templates/study.html',
                  {
                      "post_nickname" : post_nickname,
                      "post_staff" : post_staff,
                      "post_avatar" : post_avatar,
                  })

def conditions(request):
    return render(request, "Conditions/Conditions.html")
def conditions_personal(request):
    return render(request, "Conditions/conditions_of_personal_information.html")
