from ShipEnv.shipenv import ShipEnv
import os

if __name__ == '__main__':
    print(os.getcwd())
    env = ShipEnv(screen_size=(300, 300), fps=120)
    observation, reward, done, info = env.reset()
    while True:
        observation, reward, done, info = env.step(env.action_space.sample())
        for i in range(10):
            observation, reward, done, info = env.step(1)
            if reward > 0:
                print(reward)
        if done:
            observation, reward, done, info = env.reset()