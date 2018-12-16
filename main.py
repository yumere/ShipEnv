from shipenv.environment import ShipEnv

if __name__ == "__main__":
    env = ShipEnv(screen_size=(300, 300), fps=60)
    env.reset()
    action = int(input())
    while True:
        env.step(action)