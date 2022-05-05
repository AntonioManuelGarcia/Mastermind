from django.db import transaction

from commons.ddd import repository, DDDRepository


@repository
class BoardGameRepository(DDDRepository):
    """
    The repository is a central place to write to the database.
    Some ACL logic can be performed here.
    """

    @transaction.atomic
    def bulk_create(self, objs):
        self.model.objects.bulk_create(objs)

    def get_by_id(self, id):
        aggr = self.model.objects.get(id=id)
        return aggr

    @transaction.atomic
    def create(self, obj):
        obj.save()

    @transaction.atomic
    def delete(self, obj):
        obj.delete()

    @transaction.atomic
    def update(self, obj):
        prev_obj = self.get_by_id(obj.id)
        obj.save()


@repository
class GameRepository(DDDRepository):
    """
    The repository is a central place to write to the database.
    Some ACL logic can be performed here.
    """

    @transaction.atomic
    def bulk_create(self, objs):
        self.model.objects.bulk_create(objs)

    def get_by_id(self, id):
        aggr = self.model.objects.get(id=id)
        return aggr

    @transaction.atomic
    def create(self, obj):
        obj.save()

    @transaction.atomic
    def delete(self, obj):
        obj.delete()

    @transaction.atomic
    def update(self, obj):
        prev_obj = self.get_by_id(obj.id)
        obj.save()


@repository
class GuestRepository(DDDRepository):
    """
    The repository is a central place to write to the database.
    Some ACL logic can be performed here.
    """

    @transaction.atomic
    def bulk_create(self, objs):
        print('bulk in repository')
        self.model.objects.bulk_create(objs)

    def get_by_id(self, id):
        aggr = self.model.objects.get(id=id)
        return aggr

    @transaction.atomic
    def create(self, obj):
        obj.save()

    @transaction.atomic
    def delete(self, obj):
        obj.delete()

    @transaction.atomic
    def update(self, obj):
        prev_obj = self.get_by_id(obj.id)
        obj.save()
