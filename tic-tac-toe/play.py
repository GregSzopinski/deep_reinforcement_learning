from environment import State
from agents import ComputerPlayer, HumanPlayer

if __name__ == "__main__":
    # play with human
    p1 = ComputerPlayer("computer", exp_rate=0)
    p1.load_policy("policy_p1")

    p2 = HumanPlayer("human")

    st = State(p1, p2)
    st.play_with_human()
