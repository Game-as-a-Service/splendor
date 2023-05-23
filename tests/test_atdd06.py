from tests.base_flask_test_case import BaseFlaskTestCase
from dbmodels.game_profile import GameInfo,PlayerInfo,PlayerNobleInfo,PlayerDevelopmentCardInfo,TableInfo,TableNoblesInfo,TableDevelopmentCardInfo
import base64
import json
from werkzeug.test import TestResponse

class TestApiHome(BaseFlaskTestCase):
    def setUp(self) -> None:    
        self._clear_test_data()
        self._game_id =str('e6b7e318-6d9a-4eb0-b1e6-98e7356f7f04')
        self._table_id =str('e6b7e318-6d9a-4eb0-b1e6-98e7356f7f09')
        self._p1 =str('e6b7e318-6d9a-4eb0-b1e6-98e7356f7f05')
        self._p2 =str('e6b7e318-6d9a-4eb0-b1e6-98e7356f7f06')
        self._p3 =str('e6b7e318-6d9a-4eb0-b1e6-98e7356f7f07')
        self._p4 =str('e6b7e318-6d9a-4eb0-b1e6-98e7356f7f08')
        self._prepare_test_data()
        return super().setUp()

    def tearDown(self) -> None:
        #self._clear_test_data()
        return super().tearDown()
    
    # def test_it_should_200_when_player_exists(self):
    #     """一般用戶存在，應該回應200"""
    #     with self.app.test_client() as client:
    #         res: TestResponse = client.get(f"/player?gameId={self._game_id}&playerId={self._p1}")
    #         self.assertEqual(200, res.status_code)
    
    # def test_it_should_200_when_table_exists(self):
    #     """一般用戶存在，應該回應200"""
    #     with self.app.test_client() as client:
    #         res: TestResponse = client.get(f"/table?gameId={self._game_id}&tableId={self._table_id}")
    #         self.assertEqual(200, res.status_code)

    def test_it_should_200_when_player_buy_card_exists(self):
        """一般用戶存在，應該回應200"""
        with self.app.test_client() as client:
            data = {
            'game_id': self._game_id,
            'player_id': self._p1,
            'level':1,
            'id':25,
            'resource':{
                'diamond': 0,
                'sapphire': 0,
                'emerald': 1,
                'ruby': 0,
                'onyx': 0,
                'gold': 0,
            }
        }
        res: TestResponse = client.post('/player/buycard/1', json=data)
        self.assertEqual(200, res.status_code)

    def _clear_test_data(self):
        self.user_sql_session.query(GameInfo).delete()
        self.user_sql_session.query(TableInfo).delete()
        self.user_sql_session.query(TableNoblesInfo).delete()
        self.user_sql_session.query(TableDevelopmentCardInfo).delete()
        self.user_sql_session.query(PlayerInfo).delete()
        self.user_sql_session.query(PlayerNobleInfo).delete()
        self.user_sql_session.query(PlayerDevelopmentCardInfo).delete()
        self.user_sql_session.flush()
        self.cache.clear()
    
    def _prepare_test_data(self):
        game_id =self._game_id
        table_id =self._table_id
        p1=self._p1
        p2=self._p2
        p3=self._p3
        p4=self._p4
        #game
        self.user_sql_session.add(
            GameInfo(
                **{
                    "game_id": game_id,
                    "status": "processing",
                    "turn": p1,
                    "whos_winner":None
                }
            )
        )
        #table
        self.user_sql_session.add(
            TableInfo(
                **{
                    "game_id": game_id,
                    "table_id": table_id,
                    "diamond":1,
                    "sapphire":5,
                    "emerald":3,
                    "ruby":1,
                    "onyx":2,
                    "gold":4,
                }
            )
        )
        table_nobles_info_list = [
            TableNoblesInfo(game_id=game_id, table_id=table_id, noble_id=2, seq=2),
            TableNoblesInfo(game_id=game_id, table_id=table_id, noble_id=3, seq=3),
            TableNoblesInfo(game_id=game_id, table_id=table_id, noble_id=4, seq=4),
            TableNoblesInfo(game_id=game_id, table_id=table_id, noble_id=5, seq=5)
        ]
        self.user_sql_session.add_all(table_nobles_info_list)

        table_developmen_card_info_list = [
            #table
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=24,seq=1,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=25,seq=2,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=21,seq=3,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=20,seq=4,status='ontable'),

            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=21,seq=1,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=13,seq=2,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=18,seq=3,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=16,seq=4,status='ontable'),

            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=5,seq=1,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=7,seq=2,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=9,seq=3,status='ontable'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=8,seq=4,status='ontable'),
            #deck
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=26,seq=26,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=27,seq=27,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=28,seq=28,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=29,seq=29,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=30,seq=30,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=31,seq=31,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=32,seq=32,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=33,seq=33,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=34,seq=34,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=35,seq=35,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=36,seq=36,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=37,seq=37,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=38,seq=38,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=39,seq=39,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=1,id=40,seq=40,status='indeck'),

            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=22,seq=22,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=23,seq=23,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=24,seq=24,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=25,seq=25,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=26,seq=26,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=27,seq=27,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=28,seq=28,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=29,seq=29,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=2,id=30,seq=30,status='indeck'),

            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=10,seq=10,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=11,seq=11,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=12,seq=12,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=13,seq=13,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=14,seq=14,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=15,seq=15,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=16,seq=16,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=17,seq=17,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=18,seq=18,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=19,seq=19,status='indeck'),
            TableDevelopmentCardInfo(game_id=game_id, table_id=table_id,level=3,id=20,seq=20,status='indeck'),

        ]
        self.user_sql_session.add_all(table_developmen_card_info_list)

        #p1
        self.user_sql_session.add(
            PlayerInfo(
                **{
                    "game_id": game_id,
                    "player_id": p1,
                    "seq":1,
                    "score":7,
                    "diamond":1,
                    "sapphire":0,
                    "emerald":1,
                    "ruby":1,
                    "onyx":1,
                    "gold":0,
                    "bonus_diamond":4,
                    "bonus_sapphire":1,
                    "bonus_emerald":2,
                    "bonus_ruby":3,
                    "bonus_onyx":3,
                }
            )
        )
        self.user_sql_session.add(
            PlayerNobleInfo(
                **{
                    "game_id": game_id,
                    "player_id": p1,
                    "noble_id":1,
                }
            )
        )
        self.user_sql_session.add(
            PlayerNobleInfo(
                **{
                    "game_id": game_id,
                    "player_id": p1,
                    "noble_id":3,
                }
            )
        )
        
        player_developmen_car_info_list = [
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=1,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=5,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=7,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=9,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=10,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=11,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=12,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=13,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=17,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=22,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=1, id=23,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=2, id=6,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=2, id=9,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p1, level=3, id=1,status='reserve'),
        ]
        self.user_sql_session.add_all(player_developmen_car_info_list)
        #p2
        self.user_sql_session.add(
            PlayerInfo(
                **{
                    "game_id": game_id,
                    "player_id": p2,
                    "seq":2,
                    "score":14,
                    "diamond":1,
                    "sapphire":1,
                    "emerald":0,
                    "ruby":2,
                    "onyx":1,
                    "gold":0,
                    "bonus_diamond":1,
                    "bonus_sapphire":2,
                    "bonus_emerald":5,
                    "bonus_ruby":0,
                    "bonus_onyx":0,
                }
            )
        )
        player_developmen_car_info_list = [
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=1, id=3,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=1, id=16,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=2, id=2,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=2, id=5,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=2, id=8,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=2, id=10,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=2, id=11,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=2, id=15,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=1, id=2,status='reserve'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p2, level=2, id=17,status='reserve'),
        ]
        self.user_sql_session.add_all(player_developmen_car_info_list)
        #p3
        self.user_sql_session.add(
            PlayerInfo(
                **{
                    "game_id": game_id,
                    "player_id": p3,
                    "seq":3,
                    "score":10,
                    "diamond":0,
                    "sapphire":1,
                    "emerald":3,
                    "ruby":0,
                    "onyx":0,
                    "gold":1,
                    "bonus_diamond":1,
                    "bonus_sapphire":1,
                    "bonus_emerald":1,
                    "bonus_ruby":1,
                    "bonus_onyx":2,
                }
            )
        )
        player_developmen_car_info_list = [
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=1, id=6,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=2, id=1,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=2, id=3,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=2, id=14,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=2, id=20,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=3, id=4,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=2, id=4,status='reserve'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=2, id=19,status='reserve'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p3, level=3, id=2,status='reserve'),
        ]
        self.user_sql_session.add_all(player_developmen_car_info_list)
        #p4
        self.user_sql_session.add(
            PlayerInfo(
                **{
                    "game_id": game_id,
                    "player_id": p4,
                    "seq":4,
                    "score":8,
                    "diamond":4,
                    "sapphire":0,
                    "emerald":0,
                    "ruby":3,
                    "onyx":3,
                    "gold":0,
                    "bonus_diamond":4,
                    "bonus_sapphire":3,
                    "bonus_emerald":1,
                    "bonus_ruby":1,
                    "bonus_onyx":0,
                }
            )
        )
        player_developmen_car_info_list = [
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=1, id=4,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=1, id=8,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=1, id=14,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=1, id=15,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=1, id=18,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=1, id=19,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=2, id=7,status='buy'),
            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=2, id=12,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=3, id=3,status='buy'),

            PlayerDevelopmentCardInfo(game_id=game_id, player_id=p4, level=3, id=6,status='reserve'),
        ]
        self.user_sql_session.add_all(player_developmen_car_info_list)
        self.user_sql_session.flush()
