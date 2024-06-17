from cfg.models import CTBPROFILE

def profile_data(request):

    if request.user.is_authenticated:
        profile = CTBPROFILE.objects.get(fk_user=request.user)
        return {'user_profile': profile}
    return {}