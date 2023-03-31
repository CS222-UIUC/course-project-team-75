from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

def name(request):
    submitted = False
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
             cd = form.cleaned_data
             # assert False
             return HttpResponseRedirect('/form?submitted=True')
    else:
        form = NameForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 
        'form/name.html', 
        {'form': form, 'submitted': submitted}
        )
