---
title: How Django meets htmx &#58; A quick tour of modern server side rendering.
date: 2022-03-10 10:00
---

### htmx
The philosophy of htmx is to write less Javascript code, this library gives you access to modern browser features such as AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, using attributes like `hx-get` or `hx-trigger`.

A few considerable features of htmx:

- Any element, not just anchor tag or form can issue an HTTP request.
- Any event, not just form or button can trigger requests.

The quick demo below illustrate how to make POST request to create/update data on a dynamic page.

#### Context
You want to update the user profile with a form. A POST request is sent when the form is submitted.
The input should be validated and new data should be automatically updated after form submission.

Simplified project structure:
```
manage.py
users/
    views.py
    urls.py
templates/
    users/
         profile.html
         password_update.html
```

## STEP 1: Install htmx and render a form that displays input fields

Insert this script into profile.html template, detailed installation instructions can be found [here](https://htmx.org/docs/#installing). I'll skip the profile page for the sake of a brief tutorial.

`password_update.html` is a **fragment** instead of a full html file. A view that responses a fragment html is the key technique helps htmx render element dynamically.
```html
<!-- password_update.html -->

<form hx-post="{% url 'user-password-update' %}" hx-swap="outerHTML">
    {% csrf_token %}
    <div class="form-group">
        <div class="row my-2">
            <div class="col">
                <label>Old password:</label>
                {{form.old_password}}
                {% for error in form.old_password.errors %}
                    <div class="error-feedback">{{error}}</div>
                {% endfor %}
            </div>
        </div>
        <div class="row my-2">
            <div class="col">
                <label>New password:</label>
                {{form.new_password1}}
                {% for error in form.new_password1.errors %}
                    <div class="error-feedback">{{error}}</div>
                {% endfor %}
            </div>
        </div>
        <div class="row my-2">
            <div class="col">
                <label>Confirm password:</label>
                {{form.new_password2}}
                {% for error in form.new_password2.errors %}
                    <div class="error-feedback">{{error}}</div>
                {% endfor %}
            </div>
        </div>
        <input type="submit" value="Save" class="btn btn-primary mt-3">
    </div>
</form>

```
This form tag tells `htmx`:

> Once form is submitted, issue an HTTP POST request to user-password-update url then replace entire target element with the content of the response dynamically.

`hx-post` is basically like the standard `action` attribute which tells browser where to send data to. In this case to `user-password-update` url.

The second attribute `hx-swap` describe the way how htmx swap the HTML code returned by Django view onto the page. `outerHTML` in this case means entire form itself.

`hx-target` is usually paired with `hx-swap` if you want to load the response into a different element other than the one triggering request. A popular example is that you submit a `TaskCreateForm` then append the newly-created task to a `ul`  tag.

If `hx-target` is not specified, its default value is the element that make the request.


## STEP 2: Write Django views that accepts request from browsers and handle the logic of password update.

```python
# views.py
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.forms import PasswordChangeForm

class UserProfileView(TemplateView):
    """Display current user profile data."""
    template_name = "users/profile/profile.html"

    def get_context_data(self, **kwargs):
        """Provide form to template for first-time loading."""
        context_data = super().get_context_data(**kwargs)
        context_data["form"] = PasswordChangeForm(user=self.request.user)
        return context_data

class PasswordChangeViewAdmin(PasswordChangeView):
    """Allow change password for current user."""
    template_name = "users/profile/password_update.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("admin-login")
```

```python
# urls.py

from . import views

urlpatterns = [
    path("profile/", include([
        path(
            "",
            views.UserProfileView.as_view(),
            name="user-profile",
        ),
        path(
            "update/",
            views.UserProfileUpdateView.as_view(),
            name="user-profile-update",
        ),
    ])),
]
```

There are 2 possible outcome. If `PasswordChangeForm` takes invalid data (two password does not match, for example), PasswordChangeViewAdmin return a response with `password_update.html` fragment and the `PasswordChangeForm` instance in the context data. htmx takes this fragment and load it on the page. As you're changing your old password so the page should dynamically re-render the form.

![htmx re-render form tag](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/g5s0d9cfbllfbqj1zyaj.png)

The second scenario is that the data you submit is valid, according to the initial implementation of `PasswordChangeViewAdmin`, it should return a response including the admin-login template. Now here comes the problem: the page is expected to load the admin-login page into the form tag. It does not make sense and not what we want to do.


## STEP 3: Redirect after successful form submission
The solution to this circumstance is to modify the behavior of `hx-post`, prevent it from swapping response onto the page. Instead we should redirect users to another page: 

```python
class PasswordChangeViewAdmin(PasswordChangeView):
    """Allow change password for current user."""
    template_name = "users/profile/password_update.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("admin-login")

    def form_valid(self, form):
        """Insert HX-Redirect attribute to response header.

        The purpose is to modify htmx swapping mechanism
        in case of successful update.
        """
        form.save()
        response = HttpResponse()
        response["HX-Redirect"] = reverse("admin-login")
        return response
```
By this way, we tell htmx to redirect user to the login page to re-sign in rather than staying on the current page.

Hopefully this quick example gives you some inspirations of what htmx can do in combination with Django forms. It gives you ability to render elements without reloading page. More importantly, it can be achieved but not write a single line of Javascript code...




