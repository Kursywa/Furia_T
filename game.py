from datetime import datetime
try:
    from .exceptions import WrongUsernameException
    from .settings import (
        TOTAL_HIGHSCORES,
        TIME_COEFFICIENT,
        ERROR_COEFFICIENT,
        HIGHSCORE_FILENAME)
except ImportError:
    from exceptions import WrongUsernameException
    from settings import (
        TOTAL_HIGHSCORES,
        TIME_COEFFICIENT,
        ERROR_COEFFICIENT,
        HIGHSCORE_FILENAME)


class User:
    def __init__(self, username:str):
        self.username = username
        self.games = []

    def __get_username(self) -> str:
        return self.__username

    def __set_username(self, username:str):
        if isinstance(username, str) and len(username) > 0:
            self.__username = username
        else:
            raise WrongUsernameException(f"Invalid username: {username} ({type(username)})")

    username = property(__get_username, __set_username)


class HighScores:
    def __init__(self, filename=HIGHSCORE_FILENAME, total_high_scores=TOTAL_HIGHSCORES):
        self.__filename = filename
        self.__highscores = []
        self.read_highscores()
        self.total_high_scores = total_high_scores

    @staticmethod
    def calculate_highscore(total_time_in_s:float, number_of_errors:float):
        return (1_000_000.0 / total_time_in_s * TIME_COEFFICIENT
                + number_of_errors * ERROR_COEFFICIENT)

    def read_highscores(self):
        with open(self.__filename, "r", encoding="utf-8") as f:
            for line in f:
                elements = line.strip().rsplit(";", maxsplit=1)
                self.__highscores.append([elements[0], float(elements[1])])

    def check_and_add_highscore(self, score, username):
        added = False
        for index, highscore in enumerate(self.__highscores):
            if score > highscore[1]:
                self.__highscores.insert(index, (username, score))
                added = True
                break
        if not added:
            self.__highscores.append((username, score))
        self.__highscores = self.__highscores[:self.total_high_scores]

    def write_highscores(self):
        with open(self.__filename, "w", encoding="utf-8") as f:
            for highscore in self.__highscores:
                f.write("{};{:.2f}\n".format(*highscore))

    def get_highscores(self):
        return self.__highscores


class Game:
    def __init__(self):
        self.__start_time = datetime.now()
        self.__total_time = 0
        self.__max_level = 1 # na którym poziomie jest obecnie gracz
        self.__number_of_errors = 0

    def update_time(self): # zapisywane na koniec jakiegoś etapu
        self.__total_time = datetime.now() - self.__start_time

    def add_error(self):
        self.__number_of_errors += 1

    def set_user(self, user):
        if not isinstance(user, User):
            raise TypeError("user must be an instance of User")
        self.__user = user

    def play(self): # tu powinno być odwołanie do pętli głównej z przekazaniem self, ustawienie usera

        pass


if __name__ == "__main__":
    username = "Adam"#input('Enter your name: ')
    player = User(username)
    player2 = User('Player2')
    high_scores = HighScores()
    score = high_scores.calculate_highscore(300, 2)
    high_scores.check_and_add_highscore(score, player.username)
    score2 = high_scores.calculate_highscore(301, 2)
    high_scores.check_and_add_highscore(score2, player2.username)
    for i in range(7):
        score = high_scores.calculate_highscore(303 + i, 2)
        high_scores.check_and_add_highscore(score, player.username)
    high_scores.write_highscores()
    #print(high_scores.get_highscores())