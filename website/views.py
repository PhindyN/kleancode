from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
def home(request):
    #API = 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
    lang_list = [ 'Python','C#', 'C++', 'C', 'css', 'C-like', 'DjangoJinja2', 'Docker', 'Java', 'JSON + Web App Manifest', 'JSON5', 'JSONP', 'JS Templates',
                 'Markup templating', 'MATLAB', 'PHP', 'R', 'SQL', 'TypeScript']

    if request.method == "POST":
        code = request.POST["code"]
        lang = request.POST["lang"]

        #Ensure programming is picked
        if lang == "Select Programming Language":
            messages.success(request, "Please select coding language")
            return render(request, 'home.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        else:
            # OpenAI Key
            openai.api_key = "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"
            #openai.api_key = "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"
            # OpenAi stance
            openai.Model.list()
            try:
                response = openai.Completion.create(
                    engine = 'text-davinci-003',
                    prompt = f"Respond only with code. Fix this {lang} code: {code}",
                    temperature = 0,
                    max_tokens = 1000,
                    top_p = 1.0,
                    frequency_penalty = 0.0,
                    presence_penalty = 0.0,
                )
                #Parse the response
                response = (response["choices"][0]["text"]).strip()
                return render(request, 'home.html', {'lang_list': lang_list, 'response': response, 'lang': lang})

            except Exception as e:
                print(e)
                print("d"*80)
                return render(request, 'home.html', {'lang_list': lang_list, 'response': e, 'lang': lang})

    return render(request, 'home.html', {"lang_list":lang_list,'code':'#Write your code in the form below'})

def suggest(request):
    lang_list = ['Python', 'C#', 'C++', 'C', 'css', 'C-like', 'DjangoJinja2', 'Docker', 'Java',
                 'JSON + Web App Manifest', 'JSON5', 'JSONP', 'JS Templates',
                 'Markup templating', 'MATLAB', 'PHP', 'R', 'SQL', 'TypeScript']

    if request.method == "POST":
        code = request.POST["code"]
        lang = request.POST["lang"]

        # Ensure programming is picked
        if lang == "Select Programming Language":
            messages.success(request, "Please select coding language")
            return render(request, 'suggest.html', {'lang_list': lang_list, 'code': code, 'lang': lang})
        else:
            # OpenAI Key
            openai.api_key = "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"
            # openai.api_key = "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"
            # OpenAi stance
            openai.Model.list()
            try:
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"Respond only with code. {code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                # Parse the response
                response = (response["choices"][0]["text"]).strip()
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': response, 'lang': lang})

            except Exception as e:
                print(e)
                print("d" * 80)
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': e, 'lang': lang})

    return render(request, 'suggest.html', {"lang_list": lang_list, 'code': '#Write your code in the form below'})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('home')
        else:
            messages.success(request, "Error logging in Please try again")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Logged Out. Bye!!")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Complete")
            return redirect('home')
    else:
        form = SignUpForm
    return render(request, 'register.html', {"form": form})
