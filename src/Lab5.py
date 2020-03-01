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
cantidad_CPU = 1

random.seed(10)


# =========================== Simulación ===========================
run_time = []  # Lista con los tiempos totales de cada proceso

def process(env, name, ram, cpu, cpu_ips, max_time, total_time):
    instructions = random.randint(1, 10)
    memory_needed = random.randint(1, 10)
    time = env.now

    print("El proceso", name, "llegó a la fase \"new\" en ", env.now, "\t Instrucciones restantes:", instructions)

    while instructions > 0:
        # Mientras queden instrucciones pido memoria a la ram
        yield ram.get(memory_needed)
        hasRam = True

        # Mientras tengo RAM pido espacio al CPU
        while hasRam:
            print("El proceso", name, "llegó a la fase \"ready\" en",
                  env.now, "\t Instrucciones restantes:", instructions)

            # Pido espacio al CPU
            yield cpu.get(1)
            print("El proceso", name, "está en la fase \"running\" en",
                  env.now, "\t Instrucciones restantes:", instructions)

            # Espero hasta lo que pase primero, me quede sin instrucciones o pase el tiempo maximo
            yield env.timeout(min(instructions / cpu_ips, max_time))
            instructions = instructions - time_given * cpu_ips
            if instructions < 0:
                instructions = 0
            print("El proceso", name, "salió de la fase \"running\" en",
                  env.now, "\t Instrucciones restantes:", instructions)

            # Salgo del CPU
            yield cpu.put(1)

            # Veo si tengo tengo que devolver la RAM (terminé o waiting)
            hasRam = random.randint(1, 2) == 2 and instructions > 0
            if not hasRam:
                yield ram.put(memory_needed)

        # Si libere espacio de RAM y tengo instrucciones (en waiting) lo muestro
        if instructions > 0:
            print("El proceso", name, "está en la fase \"waiting\" en",
                  env.now, "\t Instrucciones restantes:", instructions)

    # Al quedarme sin insrucciones imprimo que el proceso terminó
    print("El proceso", name, "está en la fase \"terminated\" en",
          env.now, "\t Instrucciones restantes:", instructions)
    total_time.append(env.now - time)


environmen  t = simpy.Environment()
RAM = simpy.Container(environment, init=RAM_memoria, capacity=RAM_memoria)
CPU = simpy.Container(environment, init=cantidad_CPU, capacity=cantidad_CPU)

environment.process(process(environment, "a", RAM, CPU, CPU_ips, time_given, run_time))
environment.process(process(environment, "b", RAM, CPU, CPU_ips, time_given, run_time))
environment.process(process(environment, "c", RAM, CPU, CPU_ips, time_given, run_time))

environment.run()

# ==================== Resultados ==========================

def promedio(cantidades):
    r = 0
    for cantidad in cantidades:
        r = r + cantidad

    return r / len(cantidades)


def desviacion(cantidades):
    media = promedio(cantidades)
    r = 0
    for cantidad in cantidades:
        r = r + (media - cantidad) ** 2

    return (r / (len(cantidades) - 1)) ** 0.5


print("\nTiempos Totales:")
for tiempo in run_time:
    print(tiempo)

print("\nTiempo Promedio: %.2f"
      "\nDesviación estándar poblacional: %.2f" % (promedio(run_time), desviacion(run_time)))
