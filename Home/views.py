from django.shortcuts import render, redirect



def Home(request):
	if request.user.is_authenticated:
		return redirect('home')

	return render(request, 'Home.html')