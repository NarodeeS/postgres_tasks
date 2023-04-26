class OutOfMovesError(Exception):
    def __str__(self) -> str:
        return "You're out of moves!"
