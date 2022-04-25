from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.status import *
from django.urls import reverse
from model_bakery import baker
from .models import *
from .serializers import *
from users.models import User


class TestBoardgameAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username="admin", password="admin",
            email="admin@example.com"
        )
        cls.mindbreak_boardgame = BoardGame.objects.create(name="Mindbreak")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
        cls.mindbreak_boardgame.delete()

    def test_create_boardgame(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Boardgame/',
                                    {'name': 'Monopoly'}, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_boardgame_already_exist(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Boardgame/',
                                    {'name': 'Mindbreak'}, format="json")

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_boardgame_status(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/game/Boardgame/',
                                   {'boardgame': self.mindbreak_boardgame.pk}, format="json")
        boardgame_results = response.data['results'][0]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(boardgame_results['name'], 'Mindbreak')


class TestGameAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username="admin", password="admin",
            email="admin@example.com"
        )
        cls.mindbreak_boardgame = BoardGame.objects.create(name="Mindbreak")
        cls.game1 = Game.objects.create(user=cls.user, boardgame=cls.mindbreak_boardgame, code='RGBY')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
        cls.mindbreak_boardgame.delete()
        cls.game1.delete()

    def test_create_game(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Game/',
                                    {'user': self.user.id, 'boardgame': self.mindbreak_boardgame.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_create_game_without_user(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Game/',
                                    {'boardgame': self.mindbreak_boardgame.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_game_status(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/game/Game/',
                                   {'game': self.game1.pk}, format="json")
        game_results = response.data['results'][0]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(game_results['finished'], False)
        self.assertEqual(game_results['winned'], False)
        self.assertEqual(game_results['max_guests'], 10)
        self.assertEqual(game_results['code'], '')
        self.assertEqual(game_results['user'], 1)
        self.assertEqual(game_results['boardgame'], 'Mindbreak')
        self.assertEqual(game_results['guests'], [])


class TestGuestAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username="admin", password="admin",
            email="admin@example.com"
        )
        cls.mindbreak_boardgame = BoardGame.objects.create(name="Mindbreak")
        cls.game1 = Game.objects.create(user=cls.user, boardgame=cls.mindbreak_boardgame, code='RGBY')
        cls.game2 = Game.objects.create(user=cls.user, boardgame=cls.mindbreak_boardgame, code='BBWW')
        cls.game3 = Game.objects.create(user=cls.user, boardgame=cls.mindbreak_boardgame, code='BBWW', max_guests=1)
        cls.game_finish = Game.objects.create(user=cls.user, finished=True, boardgame=cls.mindbreak_boardgame,
                                              code='BBWW', max_guests=1)
        cls.game_winned = Game.objects.create(user=cls.user, winned=True, boardgame=cls.mindbreak_boardgame,
                                              code='BBWW', max_guests=1)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
        cls.mindbreak_boardgame.delete()
        cls.game1.delete()
        cls.game2.delete()

    def test_create_guest(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Guest/',
                                    {'guest_code': 'WWWW', 'game': self.game1.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get('black_result'), 0)
        self.assertEqual(response.data.get('white_result'), 0)

    def test_create_max_guest(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Guest/',
                                    {'guest_code': 'WWWW', 'game': self.game3.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        response2 = self.client.post('/api/game/Guest/',
                                     {'guest_code': 'WWWW', 'game': self.game3.pk}, format="json")
        self.assertEqual(response2.status_code, HTTP_400_BAD_REQUEST)

    def test_not_new_guest_in_finished_game(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Guest/',
                                    {'guest_code': 'WWWW', 'game': self.game_finish.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_not_new_guest_in_winned_game(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Guest/',
                                    {'guest_code': 'WWWW', 'game': self.game_winned.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_guest_black_results(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Guest/',
                                    {'guest_code': 'RWBW', 'game': self.game1.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get('black_result'), 2)
        self.assertEqual(response.data.get('white_result'), 0)
        response2 = self.client.post('/api/game/Guest/',
                                     {'guest_code': 'WGWY', 'game': self.game1.pk}, format="json")
        self.assertEqual(response2.status_code, HTTP_201_CREATED)
        self.assertEqual(response2.data.get('black_result'), 2)
        self.assertEqual(response2.data.get('white_result'), 0)

    def test_winning_game(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Guest/',
                                    {'guest_code': 'RGBY', 'game': self.game1.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get('black_result'), 4)
        self.assertEqual(response.data.get('white_result'), 0)

    def test_guest_white_results(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/game/Guest/',
                                    {'guest_code': 'WRBW', 'game': self.game1.pk}, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get('black_result'), 1)
        self.assertEqual(response.data.get('white_result'), 1)
        response2 = self.client.post('/api/game/Guest/',
                                     {'guest_code': 'YRGB', 'game': self.game1.pk}, format="json")
        self.assertEqual(response2.status_code, HTTP_201_CREATED)
        self.assertEqual(response2.data.get('black_result'), 0)
        self.assertEqual(response2.data.get('white_result'), 4)
        response3 = self.client.post('/api/game/Guest/',
                                     {'guest_code': 'YWYW', 'game': self.game1.pk}, format="json")
        self.assertEqual(response3.status_code, HTTP_201_CREATED)
        self.assertEqual(response3.data.get('black_result'), 0)
        self.assertEqual(response3.data.get('white_result'), 1)
        response4 = self.client.post('/api/game/Guest/',
                                     {'guest_code': 'YWYB', 'game': self.game1.pk}, format="json")
        self.assertEqual(response4.status_code, HTTP_201_CREATED)
        self.assertEqual(response4.data.get('black_result'), 0)
        self.assertEqual(response4.data.get('white_result'), 2)


class TestCreateCode(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.VALID_GUEST_VALUES = ['R', 'G', 'B', 'Y', 'W', 'O']

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_method(self):
        code = createcode()
        self.assertEqual(len(code), 4)
        self.assertEqual(code[0] in self.VALID_GUEST_VALUES, True)
        self.assertEqual(code[1] in self.VALID_GUEST_VALUES, True)
        self.assertEqual(code[2] in self.VALID_GUEST_VALUES, True)
        self.assertEqual(code[3] in self.VALID_GUEST_VALUES, True)


class TestCheckGuestValue(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.VALID_GUEST_VALUES = ['R', 'G', 'B', 'Y', 'W', 'O']

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_method(self):
        self.assertEqual(checkguestvalue('R'), True)
        self.assertEqual(checkguestvalue('Y'), True)
        self.assertEqual(checkguestvalue(''), False)
        self.assertEqual(checkguestvalue(None), False)
        self.assertEqual(checkguestvalue('RG'), False)
        self.assertEqual(checkguestvalue('YW'), False)


class TestCheckValidGuest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.VALID_GUEST_VALUES = ['R', 'G', 'B', 'Y', 'W', 'O']

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_method(self):
        self.assertEqual(checkvalidguest('RGWB'), True)
        self.assertEqual(checkvalidguest('YOGG'), True)
        self.assertRaises(IndexError, checkvalidguest, '')
        self.assertRaises(TypeError, checkvalidguest, None)
        self.assertEqual(checkvalidguest('RAMG'), False)
        self.assertEqual(checkvalidguest('Y-AW'), False)


class TestCheckGuestFormat(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.VALID_GUEST_VALUES = ['R', 'G', 'B', 'Y', 'W', 'O']

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_method(self):
        self.assertEqual(checkguestformat('RGWB'), True)
        self.assertEqual(checkguestformat('YOGG'), True)
        self.assertEqual(checkguestformat(''), False)
        self.assertEqual(checkguestformat(None), False)
        self.assertEqual(checkguestformat('RAMG'), False)
        self.assertEqual(checkguestformat('YB'), False)
        self.assertEqual(checkguestformat('YBRGWB'), False)


class TestCheckBlacks(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.code1 = 'RGBY'
        cls.code2 = 'WWBB'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_correct_returns(self):
        self.assertEqual(checkblacks(self.code1, 'RGWB'), 2)
        self.assertEqual(checkblacks(self.code1, 'RGBY'), 4)
        self.assertEqual(checkblacks(self.code1, 'RG--'), 2)
        self.assertEqual(checkblacks(self.code2, 'WWBB'), 4)
        self.assertEqual(checkblacks(self.code2, 'BWBW'), 2)

    def test_exceptions(self):
        self.assertRaises(IndexError, checkblacks, guest='', code=self.code2)
        self.assertRaises(IndexError, checkblacks, guest='RB', code=self.code2)


class TestCheckWhites(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.code1 = 'RGBY'
        cls.code2 = 'WWBB'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_correct_returns(self):
        self.assertEqual(checkwhites(self.code1, 'RGWB'), 1)
        self.assertEqual(checkwhites(self.code1, 'RGBY'), 0)
        self.assertEqual(checkwhites(self.code1, 'RG--'), 0)
        self.assertEqual(checkwhites(self.code2, 'WWBB'), 0)
        self.assertEqual(checkwhites(self.code2, 'BWBW'), 2)
        self.assertEqual(checkwhites(self.code2, 'BBWW'), 4)


    def test_exceptions(self):
        self.assertRaises(IndexError, checkwhites, guest='', code=self.code2)
        self.assertRaises(IndexError, checkwhites, guest='RB', code=self.code2)


