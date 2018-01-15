import simpy

# The car process
def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)

        print('Start driving at %d' % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)

# Run the process
env = simpy.Environment()

# https://simpy.readthedocs.io/en/latest/api_reference/simpy.core.html#simpy.core.Environment
# Create a new Process instance for generator
env.process(car(env))

# https://simpy.readthedocs.io/en/latest/api_reference/simpy.core.html#simpy.core.Environment
# Executes step() until the given criterion until is met.
env.run(until=15)

