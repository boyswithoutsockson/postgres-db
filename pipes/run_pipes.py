import time
from .mp_pipe import mp_pipe
from .parties_pipe import parties_pipe
from .ballot_pipe import ballot_pipe
from .vote_pipe import vote_pipe
from .mp_party_membership_pipe import mp_party_membership_pipe
from .interest_pipe import interest_pipe


def run_pipes():
    print("MP pipe:")
    start_t = time.time()
    mp_pipe()
    end_t = time.time()
    print(f"Done with mp pipe in {round(end_t - start_t, 2)}")
    print()

    print("Interest pipe:")
    start_t = time.time()
    interest_pipe()
    end_t = time.time()
    print(f"Done with interest pipe in {round(end_t - start_t, 2)}")
    print()

    print("Ballot pipe:")
    start_t = time.time()
    ballot_pipe()
    end_t = time.time()
    print(f"Done with ballot pipe in {round(end_t - start_t, 2)}")
    print()

    print("Vote pipe:")
    start_t = time.time()
    vote_pipe()
    end_t = time.time()
    print(f"Done with vote pipe in {round(end_t - start_t, 2)}")
    print()

    print("Party pipe:")
    start_t = time.time()
    parties_pipe()
    end_t = time.time()
    print(f"Done with party pipe in {round(end_t - start_t, 2)}")
    print()

    print("Party membership pipe:")
    start_t = time.time()
    mp_party_membership_pipe()
    end_t = time.time()
    print(f"Done with party pipe in {round(end_t - start_t, 2)}")
    print()

if __name__ == '__main__':
    run_pipes()
