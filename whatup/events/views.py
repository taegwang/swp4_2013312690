from django.shortcuts import render_to_response
from events.models import Event
from django.template import RequestContext
from events.forms import EventForm
from dateutil.parser import parse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.
def tonight(request):
	events = Event.objects.today().filter(latest=True)
	context = {
		'events': events,
	}
	return render_to_response(
		'events/tonight.html',
		context,
		context_instance=RequestContext(request),
	)

def create(request):
	form = EventForm(request.POST or None)
	if form.is_valid():
		event = form.save(commit=False)
		event.creator = request.user
		guessed_date = None
		for word in event.description.split():
			try:
				guessed_date = parse(word)
				break
			except ValueError:
				continue
		event.start_date = guessed_date
		event.save()
		messages.success(request, "Your event was posted")
		if 'next' in request.POST:
			next = request.POST['next']
		else:
			next = reverse('ev_tonight')
		return HttpResponseRedirect(next)
	return render_to_response(
			'events/create.html',
			{'form': form},
			context_instance = RequestContext(request)
		)
