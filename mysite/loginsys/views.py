from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.core.context_processors import csrf
from loginsys.models import Profile
from loginsys.form import (ProfileCreationForm,
                           ProfileUpdateForm)
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User


def login(request):
    args = {}
    args.update(csrf(request))
    path = request.META.get('HTTP_REFERER', '/')
    if 'next' in request.GET:
        return_path = request.GET['my_redirect_field']
    elif path == request.build_absolute_uri():
        return_path = '/'
    else:
        return_path = path
    args['return_path'] = return_path
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            last_login = user.last_login.strftime("%d-%m-%Y %H:%M:%S")
            auth.login(request, user)
            messages.success(request, _('Вітаю Вас на сайті, ' + username + '! Останій раз на сайті Ви були ' +
                                        str(last_login) + '.'), extra_tags='success')
            return redirect(return_path)
        elif not username and password:
            args['login_error_username'] = "Обов'язково введіть ім'я!"
            return render_to_response('login.html', args)
        elif username and not password:
            args['username'] = username
            args['login_error_password'] = "Обов'язково введіть пароль!"
            return render_to_response('login.html', args)
        elif not username and not password:
            args['login_error_username_password'] = "Ви не ввели жодних даних!"
            return render_to_response('login.html', args)
        else:
            args['login_error'] = 'Користувач не знайдений!'
            return render_to_response('login.html', args)
    else:
        args['username'] = ''
        args['password'] = ''
    return render(request, 'login.html', args)


def logout(request):
    messages.success(request, 'Щастливо, ' + request.user.username + '!', extra_tags='success')
    auth.logout(request)
    return_path = request.META.get('HTTP_REFERER', '/')  # HTTP_REFERER — ссылка на страницу с которой пришли на текущую, если такая существует
    return redirect(return_path)


def register(request):
    title = 'Форма для реєстрації'
    button_create = 'Зареєструватися'
    path = request.META.get('HTTP_REFERER', '/')
    if path == request.build_absolute_uri():
        return_path = '/'
    else:
        return_path = path
    form = ProfileCreationForm()
    if request.POST:
        form = ProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            new_user = auth.authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password2'])
            new_profile = Profile(user=new_user, avatar=form.cleaned_data['avatar'],
                                  sex=form.cleaned_data['sex'])
            new_profile.save()
            auth.login(request, new_user)
            messages.success(request, 'Дякую, що долучилися до нас, ' + new_profile.user.username + '!',
                             extra_tags='success')
            return redirect(return_path)
        else:
            form = form
    context = {
        'title': title,
        'button_create': button_create,
        'form': form,
        'return_path': return_path,
        }
    return render(request, 'register.html', context)


def update(request):
    path = request.META.get('HTTP_REFERER', '/')
    if path == request.build_absolute_uri():
        return_path = '/'
    else:
        return_path = path
    instance = get_object_or_404(User, username=request.user)
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=instance,
                             initial={'sex': instance.profile.sex, 'avatar': instance.profile.avatar})
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.instance)
        messages.success(request, _('Ви змінили свій профіль, ' + instance.username + '!'),
                         extra_tags='success')
        return redirect(return_path)
    else:
        form = form
    title = _('Форма для зміни профіля \'' + str(instance.get_full_name() + '\''))
    button_update = _('Змінити')
    button_delete = _('Видалити')
    context = {
        'title': title,
        'button_create': button_update,
        'button_delete': button_delete,
        'form': form,
        'return_path': return_path,
        'profile': instance,
        }
    return render(request, 'register.html', context)


def delete(request, id=None):
    instance = get_object_or_404(User, id=id)
    name = instance.get_full_name()
    return_path = settings.LOGIN_REDIRECT_URL
    title = _('Ви впевнені, що хочете видалити профіль \'' + name + '\' ?')
    button_delete = _('видалити профіль')
    button_cancel = _('відміна')
    context = {
        'title': title,
        'button_delete': button_delete,
        'button_cancel': button_cancel,
        'return_path': return_path,
        }
    if request.POST:
        instance.delete()
        messages.success(request, _('Користувач \'' + name + '\' видалений!'), extra_tags='success')
        return redirect(return_path)
    return render(request, 'profile_delete_form.html', context)


# from django.contrib.contenttypes.models import ContentType
#
#
# def show_users(request, ct, ids):
#     model = get_object_or_404(ContentType, id=ct)
#     queryset = model.get_all_objects_for_this_type()
#     users = []
#     users_ids = ids.split(',')
#     if len(users_ids) > 1:
#         for user_id in users_ids:
#             content = queryset.get(pk=user_id)
#             users.append(content)
#     else:
#         users = queryset.get(pk=ids)
#     return render(request, 'show_user_from_admin.html', {'users': users})





