from models import Response
from algo_v1 import AlgoV1


class AlgoRunner:
    def __init__(self, algo_name: str = 'AlgoV1'):
        self.algo_name = algo_name
        if algo_name == 'AlgoV1':
            self.algo = AlgoV1()

    def run_cli(self, top_n: int = 1):
        while(True):
            guess_words = list(self.algo.guess_words(top_n))
            print(f"Recommendations out of {len(guess_words)}:")
            for i, word in enumerate(guess_words):
                print(f"\t{i+1}): {word}")

            choice = int(input(f'Choose (1-{len(guess_words)}):').strip())
            colors = list(input('Enter Wordle response:'))

            response = Response(guess_words[choice - 1], colors)
            if not response.is_valid():
                print("\tRESPONSE INVALID. Please try again\n")
            elif response.is_game_over():
                return print("Game Over! Congratulations!!")
            else:
                self.algo.add_response(response)


if __name__ == '__main__':
    AlgoRunner().run_cli(1)
