
from django import forms

from .models import Chat, Message, GroupDiscussion, VideoCall, Contact,CustomUser


class AddContactForm(forms.Form):
    email = forms.EmailField(label='Adresse Email')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            # Vous pouvez ajouter l'utilisateur à la liste de contacts ici
            # Par exemple :
            Contact.objects.get_or_create(user=user, email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(f"L'email {email} n'existe pas dans la base de données.")
        return email

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['title', 'participants']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participants'] = forms.ModelChoiceField(
            queryset=CustomUser.objects.filter(
                email__in=Contact.objects.filter(user=user).values_list('email', flat=True)
            ).exclude(id=user.id),  # Exclure l'utilisateur connecté
            widget=forms.RadioSelect,
            label='Destinataire'
        )
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'file']  # Inclure le champ file

class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'file']  # Inclure le champ 'file' pour le document joint

class GroupDiscussionForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Participants'
    )

    class Meta:
        model = GroupDiscussion
        fields = ['name', 'members']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les utilisateurs en utilisant les adresses email des contacts de l'utilisateur actuel
        self.fields['members'].queryset = CustomUser.objects.filter(
            email__in=Contact.objects.filter(user=user).values_list('email', flat=True)
        ).exclude(id=user.id).distinct()

class VideoCallForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),  # Utilisez CustomUser à la place de User
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = VideoCall
        fields = ['title', 'scheduled_at', 'duration', 'participants']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }



