from environment import State
from agents import ComputerPlayer

if __name__ == "__main__":
    # training
    p1 = ComputerPlayer("p1")
    p2 = ComputerPlayer("p2")

    st = State(p1, p2)
    print("training...")
    st.play_with_ai(50000)

    p1.save_policy()
    p2.save_policy()