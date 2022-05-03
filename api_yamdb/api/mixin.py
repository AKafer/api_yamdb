from rest_framework import viewsets, mixins


class MyCreateListDestroyClass(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    "Кастомный миксин класс"
    pass
