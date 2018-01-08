# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from . forms import (RegistrationForm, AuthenticationForm)


class UserRegistration(View):

    # display form
    template_name = "accounts/registration_form.html"
    form_class = RegistrationForm

    def get(self, request):
        registration_form = self.form_class(None)  # no context

        context = {
            'registration_form': registration_form
        }

        return render(request, self.template_name, context)

    def post(self,request):
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            user = registration_form.save(commit=False)
            # get data for authentication
            username = registration_form.cleaned_data["username"]
            password = registration_form.cleaned_data["password"]
            user.set_password(password)
            user.save()

            # authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("users-list")


        context = {
            "registration_form": registration_form,
        }

        return render(request, self.template_name, context)