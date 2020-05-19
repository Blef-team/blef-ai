import requests
from uuid import UUID
from jsonschema import Draft6Validator

GAME_STATE_SCHEMA = {
    "$schema": "https://json-schema.org/schema#",

    "type": "object",
    "properties": {
        "game_uuid": {"type": "string"},
        "players": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                        "nickname": {
                            "type": "string"
                            },
                        "n_cards": {
                            "type": "integer"
                            }
                        }
                }
            },
        "hands": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                        "nickname": {
                            "type": "string"
                            },
                        "hand": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "integer"
                                    },
                                    "colour": {
                                        "type": "integer"
                                    }
                                }
                            }
                            }
                        }
                }
            }

    },
    "required": ["players", "hands"]
}
Draft6Validator.check_schema(GAME_STATE_SCHEMA)
GAME_STATE_VALIDATOR = Draft6Validator(GAME_STATE_SCHEMA)

class GameManager(object):
    """Manager of API calls to the Blef Game Engine Service."""

    def __init__(self, base_url="http://localhost:8002/v3/"):
        super(GameManager, self).__init__()
        self.base_url = base_url
        self.game_uuid = None
        self.player_uuid = None

    def create_game(self):
        url = self.base_url + "games/create"
        succeeded = False
        game_uuid = None
        response = requests.get(url)
        if response.status_code == 200:
            json = response.json()
            uuid = json.get("game_uuid")
            if uuid:
                try:
                    game_uuid = UUID(uuid)
                    succeeded = True
                except:
                    pass
        return succeeded, game_uuid

    def get_game_state(self, game_uuid=None, player_uuid=None):
        self.update_game_uuid(game_uuid)
        self.update_player_uuid(player_uuid)

        url = self.base_url + "games/{}?player_uuid={}".format(str(self.game_uuid), str(self.player_uuid))
        print(url)
        succeeded = False
        game_state = None
        response = requests.get(url)
        if response.status_code == 200:
            response_obj = response.json()
            if response_obj and GAME_STATE_VALIDATOR.is_valid(response_obj):
                game_state = response_obj
                succeeded = True
        return succeeded, game_state

    def update_game_uuid(self, game_uuid):
        if game_uuid is not None:
            if isinstance(game_uuid, UUID):
                self.game_uuid = game_uuid
            else:
                print("Provided game_uuid is not valid and will be ignored.")
        if self.game_uuid is None or not isinstance(self.game_uuid, UUID):
            raise TypeError("game_uuid is required and must be type uuid.UUID")

    def update_player_uuid(self, player_uuid):
        if player_uuid is not None:
            if isinstance(player_uuid, UUID):
                self.player_uuid = player_uuid
            else:
                print("Provided player_uuid is not valid and will be ignored.")
        if self.player_uuid is None or not isinstance(self.player_uuid, UUID):
            raise TypeError("player_uuid is required and must be type uuid.UUID")
