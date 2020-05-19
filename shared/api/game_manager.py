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

    def get_game_state(self, game_uuid, player_uuid):
        if not isinstance(game_uuid, UUID) or not isinstance(player_uuid, UUID):
            raise TypeError("game_uuid and player_uuid must be type uuid.UUID")
        url = self.base_url + "games/{}?player_uuid={}".format(str(game_uuid), str(player_uuid))
        print(url)
        succeeded = False
        game_state = None
        response = requests.get(url)
        if response.status_code == 200:
            response_obj = response.json()
            print(game_state)
            if response_obj and GAME_STATE_VALIDATOR.is_valid(response_obj):
                game_state = response_obj
                succeeded = True
        return succeeded, game_state
