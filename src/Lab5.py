# author: men19195
# date: 29/02/2020
# file: Lab5

import simpy
import random

# ============ Valores que cambian según cada simulación ============
RAM_memoria = 100  # La cantidad de memoria en la RAM
CPU_ips = 1  # Instrucciones por unidad de tiempo que lee el CPU
time_given = 3  # Es la cantidad de tiempo que se le da al procesador para hacer cada proceso
cantidad_procesos = 25  # La cantidad de procesos que entraran al CPU
intervalos_procesos = 10  # El intervalo del tiempo en que llegan los procesos (ditr exponencial)
random.seed(500)


# =========================== Simulación ===========================
def process(env, name, ram, cpu, cpu_ips, max_time):
    instructions = random.randint(1, 10)
    memory_needed = random.randint(1, 10)

    print("El proceso ", name, " llegó a la fase \"new\" en ", env.now)

    while instructions > 0:
        # Mientras queden instrucciones pido memoria a la ram
        yield ram.get(memory_needed)
        hasRam = True

        # Mientras tengo RAM pido espacio al CPU
        while hasRam:
            print("El proceso ", name, " llegó a la fase \"ready\" en ", env.now)

            # Pido espacio al CPU
            yield cpu.get(1)
            print("El proceso", name, " está en la fase \"running\" en", env.now)

            # Espero hasta lo que pase primero, me quede sin instrucciones o pase el tiempo maximo
            yield env.timeout(min(instructions / cpu_ips, max_time))
            print("El proceso", name, "salió de la fase \"running\" en", env.now)
            instructions = - time_given * cpu_ips

            # Salgo del CPU
            yield cpu.put(1)

            # Veo si tengo tengo que devolver la RAM (terminé o waiting)
            hasRam = random.randint(1, 2) == 2 and instructions > 0
            if not hasRam:
                yield ram.put(memory_needed)

        # Si libere espacio de RAM y tengo instrucciones (en waiting) lo muestro
        if instructions > 0:
            print("El proceso", name, "está en la fase \"waiting\" en", env.now)

    # Al quedarme sin insrucciones imprimo que el proceso terminó
    print("El proceso", name, "está en la fase \"terminated\" en", env.now)



env = simpy.Environment()
RAM = simpy.Container(env, init=RAM_memoria, capacity=RAM_memoria)
CPU = simpy.Container(env, init=1, capacity=1)

for i in range(2):
    env.process(process(env, i, RAM, CPU, CPU_ips, time_given))

env.run()
