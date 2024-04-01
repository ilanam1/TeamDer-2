from models import custumeUser  # assuming your user model is called User

def delete_user_by_email(email):
    try:
        user = custumeUser.objects.get(email=email)
        user.delete()
        return True, "User deleted successfully"
    except custumeUser.DoesNotExist:
        return False, "User not found"
    except Exception as e:
        return False, str(e)