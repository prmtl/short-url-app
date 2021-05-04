def get_request(info):
    return info.context


def get_current_user(info):
    return info.context.user
