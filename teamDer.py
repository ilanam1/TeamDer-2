
from models import User  # assuming your user model is called User

def delete_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        user.delete()
        return True, "User deleted successfully"
    except User.DoesNotExist:
        return False, "User not found"
    except Exception as e:
        return False, str(e)
