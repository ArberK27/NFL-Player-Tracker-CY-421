import azure.functions as func
import json
import os
import functools

from repository import Repository


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Custom authentication error
class AuthError(Exception):
    pass


# Wrapper to handle authentication and unexpected errors
def handle_exceptions(handler):

    @functools.wraps(handler)
    def wrapper(*args, **kwargs):

        try:
            return handler(*args, **kwargs)

        except AuthError as exc:
            return func.HttpResponse(
                json.dumps({"error": str(exc)}),
                status_code=401,
                mimetype="application/json"
            )

        except Exception:
            return func.HttpResponse(
                json.dumps({"error": "Internal Server Error"}),
                status_code=500,
                mimetype="application/json"
            )

    return wrapper


# Check the API key
def validate_api_key(req):

    correct_key = os.environ.get("API_KEY")
    given_key = req.headers.get("x-api-key")

    if not correct_key or given_key != correct_key:
        raise AuthError("Unauthorized")


# Create one repository for the application
repository = Repository()


# Add starting NFL players

repository.create({
    "name": "Jaxson Dart",
    "team": "New York Giants",
    "position": "QB",
    "number": 6,
    "active": True
})

repository.create({
    "name": "Jalen Hurts",
    "team": "Philadelphia Eagles",
    "position": "QB",
    "number": 1,
    "active": True
})

repository.create({
    "name": "Josh Allen",
    "team": "Buffalo Bills",
    "position": "QB",
    "number": 17,
    "active": True
})

repository.create({
    "name": "Lamar Jackson",
    "team": "Baltimore Ravens",
    "position": "QB",
    "number": 8,
    "active": True
})

repository.create({
    "name": "Patrick Mahomes",
    "team": "Kansas City Chiefs",
    "position": "QB",
    "number": 15,
    "active": True
})

repository.create({
    "name": "Joe Burrow",
    "team": "Cincinnati Bengals",
    "position": "QB",
    "number": 9,
    "active": True
})

repository.create({
    "name": "Justin Jefferson",
    "team": "Minnesota Vikings",
    "position": "WR",
    "number": 18,
    "active": True
})

repository.create({
    "name": "CeeDee Lamb",
    "team": "Dallas Cowboys",
    "position": "WR",
    "number": 88,
    "active": True
})

repository.create({
    "name": "Saquon Barkley",
    "team": "Philadelphia Eagles",
    "position": "RB",
    "number": 26,
    "active": True
})

repository.create({
    "name": "Travis Kelce",
    "team": "Kansas City Chiefs",
    "position": "TE",
    "number": 87,
    "active": True
})


# Get all NFL players
@app.route(route="players", methods=["GET"])
@handle_exceptions
def get_players(req: func.HttpRequest) -> func.HttpResponse:

    validate_api_key(req)

    return func.HttpResponse(
        json.dumps(repository.get_all()),
        status_code=200,
        mimetype="application/json"
    )


# Create a new NFL player
@app.route(route="players", methods=["POST"])
@handle_exceptions
def create_player(req: func.HttpRequest) -> func.HttpResponse:

    validate_api_key(req)

    try:
        data = req.get_json()

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json"
        )

    # Check required fields
    if (
        "name" not in data
        or "team" not in data
        or "position" not in data
        or "number" not in data
    ):
        return func.HttpResponse(
            json.dumps({"error": "Missing required player information"}),
            status_code=400,
            mimetype="application/json"
        )

    # Create the player through the repository
    new_player = repository.create(data)

    return func.HttpResponse(
        json.dumps(new_player),
        status_code=201,
        mimetype="application/json"
    )


# Update an existing NFL player
@app.route(route="players/{player_id}", methods=["PUT"])
@handle_exceptions
def update_player(req: func.HttpRequest) -> func.HttpResponse:

    validate_api_key(req)

    try:
        player_id = int(req.route_params.get("player_id"))
        data = req.get_json()

    except (ValueError, TypeError):
        return func.HttpResponse(
            json.dumps({"error": "Invalid request"}),
            status_code=400,
            mimetype="application/json"
        )

    # Update the player through the repository
    player = repository.update(player_id, data)

    if player is None:
        return func.HttpResponse(
            json.dumps({"error": "Player not found"}),
            status_code=404,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps(player),
        status_code=200,
        mimetype="application/json"
    )


# Delete an NFL player
@app.route(route="players/{player_id}", methods=["DELETE"])
@handle_exceptions
def delete_player(req: func.HttpRequest) -> func.HttpResponse:

    validate_api_key(req)

    try:
        player_id = int(req.route_params.get("player_id"))

    except (ValueError, TypeError):
        return func.HttpResponse(
            json.dumps({"error": "Invalid player ID"}),
            status_code=400,
            mimetype="application/json"
        )

    # Delete the player through the repository
    deleted = repository.delete(player_id)

    if not deleted:
        return func.HttpResponse(
            json.dumps({"error": "Player not found"}),
            status_code=404,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps({"message": "Player deleted"}),
        status_code=200,
        mimetype="application/json"
    )