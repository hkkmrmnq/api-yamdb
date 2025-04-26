from rest_framework import status
from rest_framework.response import Response


class PartialUpdateMixin:
    """
    Миксин для возможности частичного обновления объекта
    в DRF вьюсетах.
    """

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save().save()
        return Response(serializer.data, status=status.HTTP_200_OK)
