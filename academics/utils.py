ACTIVE_STATUS_CHOICES = (
    ("", "All"),
    ("1", "Active"),
    ("0", "Inactive"),
)


def get_user_role_by_group(user):
    """
    Return the role of the user based on their group.
    """

    user_role = None
    # returns ListQuerySet of user's groups
    groups = user.groups.values_list("name", flat=True)

    if "Admin" in groups:
        user_role = "admin"
    elif "Instructor" in groups:
        user_role = "instructor"
    elif "Student" in groups:
        user_role = "student"

    return user_role
