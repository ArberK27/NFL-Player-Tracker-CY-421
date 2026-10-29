# Centralized in-memory repository for NFL players
class Repository:

    def __init__(self):
        # Store all players in memory
        self.players = []

        # Start automatic player IDs at 1
        self.next_id = 1


    # Create a new player with an automatic unique ID
    def create(self, data):

        new_player = {
            "id": self.next_id,
            "name": data["name"],
            "team": data["team"],
            "position": data["position"],
            "number": data["number"],
            "active": data.get("active", True)
        }

        # Add the player to the repository
        self.players.append(new_player)

        # Increase the ID for the next player
        self.next_id += 1

        return new_player


    # Get all players
    def get_all(self):
        return self.players


    # Update a player by ID
    def update(self, player_id, data):

        for player in self.players:

            if player["id"] == player_id:

                player["name"] = data.get("name", player["name"])
                player["team"] = data.get("team", player["team"])
                player["position"] = data.get("position", player["position"])
                player["number"] = data.get("number", player["number"])
                player["active"] = data.get("active", player["active"])

                return player

        # Return None if the player does not exist
        return None


    # Delete a player by ID
    def delete(self, player_id):

        for player in self.players:

            if player["id"] == player_id:

                # Remove the player from memory
                self.players.remove(player)

                return True

        # Return False if the player does not exist
        return False