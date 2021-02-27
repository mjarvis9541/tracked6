class UserFormKwargsMixin:
    """
    CBV mixin which puts the user from the request into the form kwargs.
    Note: Using this mixin requires you to pop the `user` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs['user'] = self.request.user
        return kwargs