import gym
env = gym.make('CartPole-v0')


for i_episode in range(20):
    observation = env.reset()
    for time_step in range(100):
        env.render()
        print(observation)
        # take a random action
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print(f"Episode finished after {time_step+1} time steps")
            break
env.close()
