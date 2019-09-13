from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.http import Http404
from .models import Question,Choice
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]
		
class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#output = ', '.join([q.question_text for q in latest_question_list])
	#template = loader.get_template('polls/index.html')
	#return HttpResponse(output)
	context = {'latest_question_list' : latest_question_list}
	#return HttpResponse(template.render(context,request))
	return render(request,"polls/index.html",context)
	
def detail(request, question_id):
	'''try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request,"polls/detail.html",{'question':question})
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})'''
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		return render(request,"polls/error404.html",{'message':'Polls Details Not Found'})
	return render(request,"polls/detail.html",{'question':question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
		'question': question,
		'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('results', args=(question.id,)))
		#return render(request,'polls/results.html',{'question':question})

def first(request):
	request.session["name"] = "ramesh"
	response = HttpResponse("Session is Set ")
	response.set_cookie("values","Grapess Solutions")
	#return HttpResponse("Session is Set")
	return response

def second(request):
	#name = request.session.get("name")
	result = ""
	if "name" in request.session :
		name = request.session.get("name")
		result = str(name) + " is read from Session ID : " + str(request.session.session_key)
	else:
		result += " There is No Name in Session "
	if "sessionid" in request.COOKIES:
		result += " Cookie ID : " + str(request.COOKIES['sessionid'])
	print(request.COOKIES)
	return HttpResponse(result)

def clear_data(request):
	response = HttpResponse(" Everything is Cleared ")
	response.delete_cookie('values')
	response.delete_cookie('sessionid')
	#del request.session["name"]
	return response