from services.user_service import create_user

def create_user_view(request):
    name = request.get("name")
    user = create_user(name)
    return {"user": user.name}
