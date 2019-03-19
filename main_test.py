from shipenv import ShipEnv

if __name__ == '__main__':
    import random
    env = ShipEnv(screen_size=(300, 300), fps=30)
    env.reset()

    while True:
        action = random.randint(0, 3)
        o, r, end, _ = env.step(action)

        if end:
            env.reset()
