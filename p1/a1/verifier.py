from django.shortcuts import redirect

def verified_required(required):
    def verf(request, *args, **kwargs):
        if not request.session.get('is_verified'):
            return redirect('reg')
        return required(request, *args, **kwargs)
    return verf