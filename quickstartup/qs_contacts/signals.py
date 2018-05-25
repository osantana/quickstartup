from django.dispatch import Signal

new_contact = Signal(providing_args=["contact", "request"])
