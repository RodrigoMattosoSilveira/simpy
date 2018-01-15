"""
Bank renege example

Covers:

- Resources: Resource
- Condition events

Scenario:
  A counter with a random service time and customers who renege after loosing their patience waiting to be served. Based on the
  program bank08.py from TheBank tutorial of SimPy 2. (KGM)

  New customers are created by the new_customer process every few time steps.

"""
import random
import simpy

import time

RANDOM_SEED = 42
NEW_CUSTOMERS = 50  # Total number of customers
CUSTOMERS_IAT = 5.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience

# A technique to get a random seed!
current_milli_time = round(time.time() * 1000)
RANDOM_SEED = current_milli_time%100
print ('Cuurent time in mils: %s' % (current_milli_time))
print ('RANDOM_SEED: %s' % (RANDOM_SEED))

# Fancy way whih I might use in the future
# current_milli_time = lambda: int(round(time.time() * 1000))
#print ('%s' % (current_milli_time()))


# This generator creates customers, adds them to the simulation environment, and yields
def new_customer(env, max_number_of_customers, customer_inter_arrival_time, counter):
    """Source generates customers randomly"""
    for i in range(max_number_of_customers):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / customer_inter_arrival_time)
        yield env.timeout(t)


def customer(env, name, counter, time_in_bank):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    # Notice that the counter (a resource) adheres to the WITH interface
    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))


# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)

# Set up the simpy environment
env = simpy.Environment()

# https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html#module-simpy.resources.resource
# Get a bank resource with one teller
counter = simpy.Resource(env, capacity=2)

# https://simpy.readthedocs.io/en/latest/api_reference/simpy.core.html#simpy.core.Environment
# Create a new Process instance for generator
# Note that this is the process that will triggger the battery charge interrupt
env.process(new_customer(env, NEW_CUSTOMERS, CUSTOMERS_IAT, counter))

# https://simpy.readthedocs.io/en/latest/api_reference/simpy.core.html#simpy.core.Environment
# Executes step() until the given criterion until is met.
env.run()
