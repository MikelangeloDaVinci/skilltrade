
def check_user_settings(request):
    if request.user.is_authenticated():
        return {'USER_HAS_MISSING_PROFILE_DATA': request.user.profile.has_missing_user_data()}
    else:
        return {'USER_HAS_MISSING_PROFILE_DATA': False}