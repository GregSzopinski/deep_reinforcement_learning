from torch.distributions import Categorical
import numpy as np
import gym
import torch
import torch.nn as nn
import torch.optim as optim

gamma = 0.99


class Pi(nn.Module):
    """Class implementing the policy network. In this case it is a simple MLP with 64 hidden units."""

    def __init__(self, in_dim, out_dim):
        super(Pi, self).__init__()
        layers = [
            nn.Linear(in_dim, 64),
            nn.ReLU(),
            nn.Linear(64, out_dim),
        ]

        self.model = nn.Sequential(*layers)
        self.onpolicy_reset()
        self.train()

    def onpolicy_reset(self):
        self.log_probs = []
        self.rewards = []

    def forward(self, x):
        pdparam = self.model(x)
        return pdparam

    def act(self, state):
        """Function takes a state and produce an probability of action sampled from categorical distribution"""
        x = torch.from_numpy(state.astype(np.float32))  # to tensor
        pdparam = self.forward(x)  # forward pass
        pd = Categorical(logits=pdparam)  # probability distribution
        action = pd.sample()  # pi(a|s) in action via pd
        log_prob = pd.log_prob(action)  # log_prob of pi(a|s)
        self.log_probs.append(log_prob)  # store for training
        return action.item()


def train(pi, optimizer):
    """Take the policy (pi) and the optimizer to compute the loss"""
    # Inner gradient-ascent loop of REINFORCE
    T = len(pi.rewards)
    rets = np.empty(T, dtype=np.float32)  # ret is for the returns
    future_ret = 0.0
    # Compute returns efficiently
    for t in reversed(range(T)):
        future_ret = pi.rewards[t] + gamma * future_ret
        rets[t] = future_ret
    rets = torch.tensor(rets)
    log_probs = torch.stack(pi.log_probs)
    loss = (
        -log_probs * rets
    )  # gradient term; PyTorch by default minimizes the loss-negative to maximize the objective
    loss = torch.sum(loss)
    optimizer.zero_grad()
    loss.backward()  # backpropagate, compute gradients of the loss equal to the policy gradient
    optimizer.step()  # gradient ascent, update the weights
    return loss


def main():
    env = gym.make("CartPole-v0")  #
    in_dim = env.observation_space.shape[0]
    out_dim = env.action_space.n
    pi = Pi(
        in_dim, out_dim
    )  # policy pi_theta for REINFORCE - a neural network specified earlier
    optimizer = optim.Adam(pi.parameters(), lr=0.01)
    for epi in range(300):
        state = env.reset()
        for t in range(200):  # cartpole max timestep
            action = pi.act(state)
            state, reward, done, _ = env.step(action)
            pi.rewards.append(reward)
            env.render()
            if done:
                break
        loss = train(pi, optimizer)  # train per episode
        total_reward = sum(pi.rewards)
        solved = total_reward > 195.0  # specify when the env
        pi.onpolicy_reset()  # onpolicy: clear memory (rewards & log probs) after training
        print(
            f"Episode {epi}, loss: {loss}, total_reward: {total_reward}, solved: {solved}"
        )


if __name__ == "__main__":
    main()
