from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView, DetailView
from .models import Video,VideoLesson,VideoChapter
from .models import Category,CategorySub,Member
from .forms import VideoForm,VideochapterForm,VideolessonForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from slugify import slugify


def index(request):
    video = Video.objects.filter(published=True)
    context = {'video_list':video,}

    return render(request,'video/index.html',context)


class BookDetailView(DetailView):
    model = Video
    template_name = 'video/detail.html'
    slug_url_kwarg = 'slug'


#------------------------------------------------------
#chapter management
#------------------------------------------------------


def management_course(request):
    videos = Video.objects.filter(member__user=request.user.id)
    return render(request,'video/course.html',{"video_list":videos})


def video_add(request):
    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.slug = slugify(video.name)
            video.member = Member.objects.filter(user_id=request.user.id).first()
            video.published = True
            video.save()
            form.save_m2m()
            messages.success(request, 'บันทึกสำเร็จ')
            return HttpResponseRedirect(reverse('video:management_course'))
        messages.error(request, 'บันทึกไม่สำเร็จ!')
    return render(request, 'video/add.html', {
        'form': form,
    })


def update_video(request, id):
    videos= Video.objects.get(id=id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=videos)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึกสำเร็จ')
            return redirect('video:management_course')
    else:
        form = VideoForm(instance=videos)
    return render(request, 'video/update_video.html', {'form': form})


def video_delete(request, id):
    videos = Video.objects.get(id=id)
    videos.delete()
    messages.success(request, 'ลบสำเร็จ')
    return redirect(reverse('video:management_course'))


#------------------------------------------------------
#chapter management
#------------------------------------------------------


def management_chapter(request):
    courseid=request.GET.get('courseid')
    chapters = VideoChapter.objects.filter(video__id=courseid)
    return render(request,'video/chapter.html',{"chapters_list":chapters,"courseid":courseid})


def video_addchapter(request):
    form = VideochapterForm()
    courseid=request.GET.get('courseid')
    if request.method == 'POST':
        form = VideochapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.video_id=courseid
            chapter.save()
            form.save_m2m()
            messages.success(request, 'บันทึกสำเร็จ')
            return HttpResponseRedirect(reverse('video:management_chapter')+'?courseid='+str(courseid))
        messages.error(request, 'บันทึกไม่สำเร็จ!')
    return render(request, 'video/add_chapter.html', {
        'form': form,
    })


def update_chapter(request, id):
    courseid=request.GET.get('courseid')
    chapters= VideoChapter.objects.get(id=id)
    if request.method == 'POST':
        form = VideochapterForm(request.POST,  instance=chapters)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึกสำเร็จ')
            return redirect(reverse('video:management_chapter')+'?courseid='+str(courseid))
    else:
        form = VideochapterForm(instance=chapters)
    return render(request, 'video/update_chapter.html', {'form': form,'courseid':courseid})


def chapter_delete(request, id):
    courseid=request.GET.get('courseid')
    chaptervideo = VideoChapter.objects.get(id=id)
    chaptervideo.delete()
    messages.success(request, 'ลบสำเร็จ')
    return redirect(reverse('video:management_chapter')+'?courseid='+str(courseid))



#------------------------------------------------------
#lesson management
#------------------------------------------------------


def management_lesson(request):
    courseid=request.GET.get('courseid')
    chapterid=request.GET.get('chapterid')
    lesson = VideoLesson.objects.filter(chapter__id=chapterid)
    return render(request,'video/lesson.html',{"lesson_list":lesson,"courseid":courseid,"chapterid":chapterid})


def video_addlesson(request):
    form = VideolessonForm()
    courseid=request.GET.get('courseid')
    chapterid=request.GET.get('chapterid')
    if request.method == 'POST':
        form = VideolessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson_obj = form.save(commit=False)
            lesson_obj.videos_id=courseid
            lesson_obj.chapter_id=chapterid
            lesson_obj.save()
            form.save_m2m()
            messages.success(request, 'บันทึกสำเร็จ')
            return redirect(reverse('video:management_lesson')+'?courseid='+str(courseid)+'&chapterid='+str(chapterid))
        messages.error(request, 'บันทึกไม่สำเร็จ!')
    return render(request, 'video/add_lesson.html', {
        'form': form,
        'courseid':courseid,
        'chapterid':chapterid,
    })


def update_lesson(request, id):
    courseid=request.GET.get('courseid')
    chapterid=request.GET.get('chapterid')
    lessons= VideoLesson.objects.get(id=id)
    if request.method == 'POST':
        form = VideolessonForm(request.POST,  instance=lessons)
        if form.is_valid():
            lesson_obj = form.save(commit=False)
            lesson_obj.videos_id=courseid
            lesson_obj.chapter_id=chapterid
            form.save()
            messages.success(request, 'แก้ไขสำเร็จ')
            return redirect(reverse('video:management_lesson')+'?courseid='+str(courseid)+'&chapterid='+str(chapterid))
    else:
        form = VideolessonForm(instance=lessons)
    return render(request, 'video/update_lesson.html', {
        'form': form,
        'courseid':courseid,
        'chapterid':chapterid,
        })

def lesson_delete(request, id):
    courseid=request.GET.get('courseid')
    chapterid=request.GET.get('chapterid')
    lessonvideo = VideoLesson.objects.get(id=id)
    lessonvideo.delete()
    messages.success(request, 'ลบสำเร็จ')
    return redirect(reverse('video:management_lesson')+'?courseid='+str(courseid)+'&chapterid='+str(chapterid))
