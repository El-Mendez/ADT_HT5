import simpy

def car(env, parkinglot, name):
    print(name, "existe en", env.now)
    yield parkinglot.get(1)
    print(name, "llego al parqueo en", env.now)
    yield env.timeout(3)
    put = parkinglot.put(1)
    yield parkinglot.put(1)
    print(name, "salió en", env.now)


env = simpy.Environment()
parqueos = simpy.Container(env, init=1, capacity=1)

env.process(car(env, parqueos, 1))
env.process(car(env, parqueos, 2))

env.run(until=10)