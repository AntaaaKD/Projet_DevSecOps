from channels.layers import get_channel_layer
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User

from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from asgiref.sync import async_to_sync
from .models import Chat, GroupDiscussion, VideoCall, Message, Contact
from .forms import ChatForm, MessageForm, GroupDiscussionForm, VideoCallForm, GroupMessageForm
from accounts.models import CustomUser
from .forms import AddContactForm
# Section Views
@login_required
def chat_section(request):
    user = request.user
    # Filtrer les discussions où l'utilisateur est le créateur ou un participant
    filtered_chats = Chat.objects.filter(Q(participants=user))

    return render(request, 'Wakhtane/chat_section.html', {'chats': filtered_chats})

@login_required
def chat_delete(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
        # Ajoutez ici votre logique de vérification pour s'assurer que l'utilisateur peut supprimer ce chat
        if request.method == 'POST':
            chat.delete()
            return redirect('Wakhtane:chat_section')
        else:
            return HttpResponseNotFound('<h1>Méthode non autorisée</h1>')
    except Chat.DoesNotExist:
        return HttpResponseNotFound('<h1>La discussion spécifiée n\'existe pas</h1>')


@login_required
def group_section(request):
    user = request.user
    # Filtrer les discussions où l'utilisateur est le créateur ou un participant
    group_discussions = GroupDiscussion.objects.filter(Q(members=user))

    return render(request, 'Wakhtane/group_section.html', {'group_discussions': group_discussions})

@login_required
def video_call_detail_view(request, pk):
    video_call = get_object_or_404(VideoCall, pk=pk)
    context = {
        'video_call': video_call,
    }
    return render(request, 'Wakhtane/video_call_detail.html', context)

@login_required
def delete_video_call(request, video_call_id):
    video_call = get_object_or_404(VideoCall, id=video_call_id)
    if request.method == 'POST':
        video_call.delete()
        return redirect('Wakhtane:video_call_list')
    return render(request, 'Wakhtane/delete_video_call.html', {'video_call': video_call})

@login_required
def video_section(request):
    video_calls = VideoCall.objects.all()
    return render(request, 'Wakhtane/video_section.html', {'video_calls': video_calls})

# Group Discussion Views
@login_required
def group_discussion_list_view(request):
    group_discussions = GroupDiscussion.objects.all()
    return render(request, 'Wakhtane/group_discussion_list.html', {'group_discussions': group_discussions})


@login_required
def group_discussion_create_view(request):
    form = GroupDiscussionForm(request.user)

    if request.method == 'POST':
        form = GroupDiscussionForm(request.user, request.POST)
        if form.is_valid():
            group_discussion = form.save(commit=False)
            group_discussion.created_by = request.user
            group_discussion.save()
            group_discussion.members.add(request.user)
            group_discussion.members.add(*form.cleaned_data['members'])
            # Redirection vers une vue après création réussie
            return redirect('Wakhtane:group_section')

    context = {
        'form': form,
    }
    return render(request, 'Wakhtane/group_discussion_form.html', context)

@login_required
def group_discussion_detail_view(request, pk):
    discussion = get_object_or_404(GroupDiscussion, pk=pk)
    # Autres logiques de vue pour le détail de la discussion de groupe, si nécessaire
    return render(request, 'Wakhtane/group_discussion_detail.html', {'discussion': discussion})

@login_required
def group_discussion_delete_view(request, pk):
    discussion = get_object_or_404(GroupDiscussion, pk=pk)

    if request.method == 'POST':
        # Supprimer la discussion de groupe
        discussion.delete()
        messages.success(request, "La discussion de groupe a été supprimée avec succès.")
        return redirect('Wakhtane:group_section')  # Rediriger vers la liste des discussions de groupe

    return redirect('Wakhtane:group_section', pk=pk)


@login_required
def group_discussion_view(request, pk):
    discussion = get_object_or_404(GroupDiscussion, id=pk)
    messages = discussion.messages.all().order_by('timestamp')
    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.discussion = discussion
            message.save()
            form = MessageForm()  # Clear form after successful submission

    context = {
        'discussion': discussion,
        'messages': messages,
        'form': form,
    }
    return render(request, 'Wakhtane/group_discussion_detail.html', context)

# Video Call Views
@login_required
def video_call_list(request):
    video_calls = VideoCall.objects.all()
    return render(request, 'Wakhtane/video_call_list.html', {'video_calls': video_calls})

@login_required
def delete_group_message(request, pk):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        if message.sender == request.user:
            message.delete()
            return HttpResponse(status=204)  # No Content, to indicate success without redirecting

    return redirect('Wakhtane:group_discussion_detail', pk=pk)



@login_required
def video_call_create_view(request):
    if request.method == 'POST':
        form = VideoCallForm(request.POST)
        if form.is_valid():
            video_call = form.save(commit=False)
            video_call.created_by = request.user  # Assigne l'utilisateur connecté comme créateur
            video_call.save()
            form.save_m2m()  # Sauvegarde les relations ManyToMany
            return redirect('Wakhtane:video_call_list')  # Redirection après création
    else:
        form = VideoCallForm()
    return render(request, 'Wakhtane/video_call_form.html', {'form': form})
# Chat Views

@login_required
def chat_create_view(request):
    add_contact_form = AddContactForm()
    create_chat_form = ChatForm(user=request.user)  # Pass user=request.user here

    if request.method == 'POST':
        if 'add_contact_form' in request.POST:
            add_contact_form = AddContactForm(request.POST)
            if add_contact_form.is_valid():
                email = add_contact_form.cleaned_data['email']
                try:
                    user = CustomUser.objects.get(email=email)
                    existing_contact = Contact.objects.filter(user=request.user, email=email).exists()
                    if not existing_contact:
                        Contact.objects.create(user=request.user, email=email)
                    return redirect('Wakhtane:chat_section')
                except CustomUser.DoesNotExist:
                    add_contact_form.add_error('email', f"L'email {email} n'existe pas dans la base de données.")

        elif 'create_chat_form' in request.POST:
            create_chat_form = ChatForm(request.user, request.POST)  # Pass request.POST here
            if create_chat_form.is_valid():
                chat = create_chat_form.save(commit=False)
                chat.created_by = request.user
                chat.save()
                chat.participants.add(request.user)
                chat.participants.add(create_chat_form.cleaned_data['participants'])
                return redirect('Wakhtane:chat_section')

    contacts = Contact.objects.filter(user=request.user)

    context = {
        'add_contact_form': add_contact_form,
        'create_chat_form': create_chat_form,
        'contacts': contacts,
        'user': request.user,  # Pass the user to the context
    }
    return render(request, 'Wakhtane/chat_form.html', context)

@login_required
def chat_detail_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    # Assurez-vous que le contexte inclut le mail du destinataire sélectionné
    if chat.participants.exists():
        other_party_email = chat.participants.first().email
    else:
        other_party_email = "Inconnu"
    context = {
        'chat': chat,
        'other_party': other_party_email,  # Passer le mail du destinataire au contexte
    }
    return render(request, 'Wakhtane/chat_detail.html', context)

@login_required
def create_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Inclure request.FILES
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            # Rediriger l'utilisateur vers la même page après l'envoi du message
            return redirect('Wakhtane:chat_detail', chat_id=chat_id)
    else:
        form = MessageForm()
    return render(request, 'Wakhtane/chat_detail.html', {'chat': chat, 'form': form})


@login_required
def create_group_message_view(request, pk):
    discussion = get_object_or_404(GroupDiscussion, pk=pk)

    if request.method == 'POST':
        form = GroupMessageForm(request.POST, request.FILES)  # Passer request.FILES pour gérer les fichiers
        if form.is_valid():
            message = form.save(commit=False)
            message.discussion = discussion
            message.sender = request.user
            message.save()
            return redirect('Wakhtane:group_discussion_detail', pk=discussion.pk)
    else:
        form = GroupMessageForm()

    return render(request, 'Wakhtane/group_discussion_detail.html', {'form': form, 'discussion': discussion})

@login_required
def dashboard(request):
    return render(request, 'Wakhtane/dashboard.html')


def index(request):
    return render(request, 'Wakhtane/index.html')

@login_required
@require_http_methods(["DELETE"])
def delete_message(request, message_id):
    try:
        message = get_object_or_404(Message, id=message_id)

        # Vérifier si l'utilisateur actuel est l'expéditeur du message et que le message est dans un chat spécifique
        if message.sender == request.user and message.chat_id == request.POST.get('chat_id'):
            # Supprimer le fichier joint s'il existe
            if message.file:
                message.file.delete()

            # Supprimer le message
            message.delete()

            return JsonResponse({'message': 'Le message a été supprimé avec succès.'}, status=204)
        else:
            return JsonResponse({'error': 'Vous n\'êtes pas autorisé à supprimer ce message.'}, status=403)

    except Exception as e:
        return JsonResponse({'error': f'Une erreur est survenue lors de la suppression du message : {str(e)}'}, status=500)

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = AddContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = request.user

            # Vérifie si l'email existe déjà pour n'importe quel utilisateur dans la base de données
            existing_user = User.objects.filter(email=email).exists()

            if existing_user:
                # Vérifie si l'email existe déjà pour l'utilisateur actuel
                existing_contact = Contact.objects.filter(user=user, email=email).exists()

                if not existing_contact:
                    # Si l'email n'existe pas encore pour cet utilisateur, l'ajouter à la liste de contacts
                    Contact.objects.create(user=user, email=email)
                    messages.success(request, f"L'email {email} a été ajouté à votre liste de contacts.")
                else:
                    # Si l'email existe déjà pour cet utilisateur, informer l'utilisateur
                    messages.info(request, f"L'email {email} est déjà dans votre liste de contacts.")
            else:
                # Si l'email n'existe pas du tout dans la base de données, informer l'utilisateur
                messages.error(request, f"L'email {email} n'existe pas dans notre système.")

            return redirect('Wakhtane:chat_list')  # Rediriger où vous souhaitez après l'ajout

    else:
        form = AddContactForm()

    return render(request, 'Wakhtane/chat_list.html', {'form': form})




@login_required
def contact_list_view(request):
    logged_in_user = request.user
    contacts = Contact.objects.exclude(user=logged_in_user)
    return render(request, 'Wakhtane/chat_form.html', {'contacts': contacts})