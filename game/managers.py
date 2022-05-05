from commons.ddd import DDDModel, DDDManager
from .models import *


class BoardGameManager(DDDManager):
    pass


class GameManager(DDDManager):
    pass


class GuestManager(DDDManager):
    pass
    # def create(self, **kwargs):
    #     #print('objs')
    #     #print(objs)
    #     print('kwargs')
    #     print(kwargs)
    #     print(self.all())
    #
    #     #super(Guest, self).create()
    #     pass

