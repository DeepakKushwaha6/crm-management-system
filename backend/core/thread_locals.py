import threading

_thread_locals = threading.local()


def get_current_organization():
    return getattr(_thread_locals, 'organization', None)


def set_current_organization(organization):
    _thread_locals.organization = organization


def get_current_membership():
    return getattr(_thread_locals, 'membership', None)


def set_current_membership(membership):
    _thread_locals.membership = membership
