'''
author: men19195
date: 29/02/2020
file: Lab5
'''

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
def process(env, name, ram, cpu, cpu_ips, time_given):
    instructions = random.randint(1, 10)
    memory_needed = random.randint(1, 10)
    print("El proceso ", name, " llegó a la fase \"new\" en ", env.now)

    # Mientras queden instrucciones pido memoria a la ram
    while instructions > 0:
        with ram.request(memory_needed) as ram_req:
            yield ram_req
            has_ram = True

            # Mientras no haya desocupado la RAM pido espacio al CPU
            while has_ram:
                print("El proceso", name, "está en la fase \"ready\" en", env.now)
                with cpu.request() as cpu_req:
                    yield cpu_req

                    # Cuando estoy en el CPU, espero hasta terminar las instrucciones o a pasar la cant de tiempo max
                    print("El proceso", name, " está en la fase \"running\" en", env.now)
                    env.timeout(min(instructions / cpu_ips, time_given))
                    print("El proceso", name, "salió de la fase \"ready\" en", env.now)
                    instructions = - time_given * cpu_ips

                # Después de liberar el CPU determino si tengo que liberar espacio de la RAM
                has_ram = random.randint(1, 2) == 2 and instructions > 0

            # Si libere espacio de RAM y tengo instrucciones (en waiting) lo muestro
            if instructions > 0:
                print("El proceso", name, "está en la fase \"waiting\" en", env.now)

    # Al quedarme sin insrucciones imrpimo que el proceso terminó
    print("El proceso", name, "está en la fase \"terminated\" en", env.now)



env = simpy.Environment()
RAM = simpy.Container(env, capacity=RAM_memoria)
CPU = simpy.Container(env, capacity=1)
