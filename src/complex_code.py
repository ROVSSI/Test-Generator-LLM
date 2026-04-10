def authorize(user_role, is_active, has_2fa):
    if user_role == "admin":
        return True

    if is_active and has_2fa:
        return True

    return False
