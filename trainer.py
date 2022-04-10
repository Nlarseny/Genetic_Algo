
import random
import subprocess
import time
import os.path
from heapq import nlargest

# START
# Generate the initial population | spawn 20 dna strands initially
# Compute fitness | have each one compete against the MCTC on easy 5 times, the highest 5 progress
# REPEAT
#     Selection | top 5 ranking
#     Crossover | function to mix
#     Mutation | decent change to go up or down 1
#     Compute fitness | play 5 rounds on easy mode again
# UNTIL population has converged | winning basically everytime, print out current stats
# STOP

class Thing:
    def __init__(self, name, dna, score):
        self.name = name
        self.dna = dna
        self.score = score


def spawn(num):
    number_contestants = num

    contestants = []

    for i in range(number_contestants):
        score = 0
        contestants.append(Thing(str(i), [random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5)], score))

    return contestants


def start_reversi_server():
    server = subprocess.Popen(["sh", "server_start.sh"])

    return server


def start_reversi_adversary():
    ad = subprocess.Popen(["sh", "adversary_start.sh"])

    return ad


def refresh():
    subprocess.Popen(["sh", "refresh.sh"])


def start_strand(strand):
    new_strand = ','.join(str(x) for x in strand)

    start = subprocess.Popen(["sh", "start_strand.sh", new_strand])

    return start


def compute_fitness(strand):
    # remove any indicator files
    if os.path.exists("./reversi_training_grounds/won.txt"):
        os.remove("./reversi_training_grounds/won.txt")
    else:
        print("Can not delete the won.txt as it doesn't exists")

    if os.path.exists("./reversi_training_grounds/lost.txt"):
        os.remove("./reversi_training_grounds/lost.txt")
    else:
        print("Can not delete the lost.txt as it doesn't exists")


    # open reversi server
    server = start_reversi_server()

    time.sleep(2)

    ad = start_reversi_adversary()

    print(strand.dna)
    start = start_strand(strand.dna)

    # have a busy while loop till we get a won.txt?

    win = 0
    flag = 1
    counter = 0
    while flag:
        file_won = os.path.exists('./reversi_training_grounds/won.txt')
        file_lost = os.path.exists('./reversi_training_grounds/lost.txt')

        if file_won and not file_lost:
            flag = 0
            # update score for this bugger
            win = 1

        if not file_won and file_lost:
            flag = 0
            # update score for this bugger
            win = 0
        else:
            time.sleep(1)
            counter += 1

        if counter >= 312:
            flag = 0
            win = 0


    ad.kill()
    server.kill()
    start.kill()

    time.sleep(2)
    refresh()
    time.sleep(1)

    return win

def init_board(score_board, contestants):
    for c in contestants:
        score_board[c.name] = 0 # this is there score per round


def test(contestants, rounds=2):
    score_board = {}
    init_board(score_board, contestants)

    for r in range(rounds): # number of rounds for each
        for i in contestants:
            win = compute_fitness(i)
            score_board[i.name] += win
            i.score += win

            print(score_board)
            time.sleep(1)

    return score_board


def crossover(good_strands, num_wanted, old_contestants):



    strands = []
    good_strands = list((int(x) for x in good_strands))
    print(good_strands)
    for x in good_strands:
        strands.append(Thing(random.randint(0,100000), old_contestants[x].dna, 0))

    print(type(good_strands))

    num_total = len(strands)
    while num_total < num_wanted:
        new_strand = []

        for i in range(3):
            flg = 0
            for j in range(len(good_strands)):
                if flg == 0:
                    if random.randint(0,100) < 15:
                        new_strand.append(good_strands[j])
                        flg = 1

                    elif random.randint(0,100) < 10:
                        mutated_num = good_strands[j] - 1
                        new_strand.append(mutated_num)
                        flg = 1

                    elif random.randint(0,100) < 10:
                        mutated_num = good_strands[j] + 1
                        new_strand.append(mutated_num)
                        flg = 1

        while len(new_strand) < 3:
            if random.randint(0,100) < 10:
                mutated_num = random.randint(-10, 10) - 1
                new_strand.append(mutated_num)
            elif random.randint(0,100) < 10:
                mutated_num = random.randint(-10, 10) + 1
                new_strand.append(mutated_num)
            else:
                new_strand.append(random.randint(-10, 10))

        new_thing = Thing(str(random.randint(0,100000)), new_strand, 0)
        strands.append(new_thing)
        num_total = len(strands)    

    return strands    


def main(num_starters, rounds):
    
    contestants = spawn(num_starters)
    for i in contestants:
        print(i.name, i.dna)

    score_board = test(contestants, rounds) # arg 2 is rounds
    
    # get the largest N of strands
    N = 3
    res = nlargest(N, score_board, key = score_board.get)

    print(contestants)
    print(score_board)
    print(res)


    # begin while loop
    flag = 1
    round = 1
    while flag:
        new_contestants = crossover(res, 10, contestants)
        for i in new_contestants:
            print(i.name, i.dna)
        
        score_board = test(new_contestants, rounds)
        # write results of each round
        with open('results.txt', 'a') as the_file:
            temp = "Round:" + str(round) + "\n"
            the_file.write(temp)

            for q in new_contestants:
                temp_dna = ' '.join(str(x) for x in q.dna)
                liner = str(q.name) + " score: " 
                liner += str(q.score) + " dna: " 
                liner += temp_dna + "\n"
                the_file.write(liner)
        print("---- results updated ----")
        round += 1


        N = 5
        res = nlargest(N, score_board, key = score_board.get)

        print(new_contestants)
        print(score_board)
        print(res)

        

        winners = 0
        for c in new_contestants:
            if c.score >= rounds - 1:
                winners += 1

        percent_winners = winners / 10

        if percent_winners > .75:
            flag = 0

        if round == 50:
            flag = 0


    print("FINAL RESULTS")
    print(new_contestants)
    print(score_board)
    print(res)




    print("done!")

if __name__ == "__main__":
    main(6, 3)

