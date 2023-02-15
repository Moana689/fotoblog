from django.template import Library
from django.utils import timezone

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = Library()

# un filter peut prendre 2 arguments max
# dans un gabarit les filters s'utilisent : object|filter
# ils peuvent être utilisés dans des conditions : {% if instance|model_type == 'Blog' %}
# ou dans des balises de gabarit : {{ instance.date_created|get_posted_at_display }}
@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def get_posted_at_display(posted_at):
    seconds_ago = (timezone.now() - posted_at).total_seconds()
    if seconds_ago <= MINUTE:
        return 'Publié à l''instant.'
    elif seconds_ago <= HOUR:
        return f'Publié il y a {int(seconds_ago // MINUTE)} minutes.'
    elif seconds_ago <= DAY:
        return f'Publié il y a {int(seconds_ago // HOUR)} heures.'
    return f'Publié le {posted_at.strftime("%d %b %y à %Hh%M")}'


# simple_tag = balise personnalisée
# les balises personnalisées ne sont pas limité en arguments
@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'vous'
    return user.username
