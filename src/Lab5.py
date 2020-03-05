# author: men19195
# date: 29/02/2020
# file: Lab5

import simpy
import random

# ============ Valores que cambian según cada simulación ============
RAM_memoria = 100  # La cantidad de memoria en la RAM
CPU_ips = 3  # Instrucciones por unidad de tiempo que lee el CPU
cantidad_procesos = 5  # La cantidad de procesos que entraran al CPU
intervalos_procesos = 10  # El intervalo del tiempo en que llegan los procesos (distr exponencial)
cantidad_CPU = 1  # Es la cantidad de CPUs en el sistema para atender los procesos

random.seed(10)

# =========================== Simulación ===========================
run_time = []  # Lista con los tiempos totales de cada proceso
time_given = 1  # Es la cantidad de tiempo que se le da al procesador como máximo para cada proceso


def process(env, name, ram, cpu, cpu_ips, max_time, total_time, arrival_intervals):
    instructions = random.randint(1, 10)
    memory_needed = random.randint(1, 10)

    # Espero hasta que el carro aparezca
    yield env.timeout(random.expovariate(1 / arrival_intervals))
    time = env.now
    print("\033[94mEl proceso %s ha sido creado en %.2f \t\t\t Cantidad de instrucciones: %d \tMemoria RAM requerida: %d \033[0m"
          % (name, env.now, instructions, memory_needed))

    # Durante el ciclo completo necesito RAM
    yield ram.get(memory_needed)

    while instructions > 0:
        print("El proceso %s llegó a la fase \"ready\" en %.2f \t\t Instrucciones restantes: %d \t RAM restante: %d"
              %(name, env.now, instructions, ram.level))

        # Mientras tengo instrucciones pido espacio al CPU
        yield cpu.get(1)
        print("El proceso %s entró a la fase \"running\" en %.2f \t Instrucciones restantes: %d"
              % (name, env.now, instructions))

        # Espero hasta lo que pase primero, me quede sin instrucciones o pase el tiempo maximo en CPU
        yield env.timeout(min(instructions / cpu_ips, max_time))
        instructions = instructions - time_given * cpu_ips
        if instructions < 0:
            instructions = 0

        # Salgo del CPU
        yield cpu.put(1)
        print("El proceso %s salió de la fase \"running\" en %.2f \t Instrucciones restantes: %d"
              % (name, env.now, instructions))

        # Veo si estoy en estado waiting
        if random.randint(1, 2) == 2 and instructions > 0:
            print("El proceso %s entró a la fase \"waiting\" en %.2f \t Instrucciones restantes: %d"
                  % (name, env.now, instructions))

    # Al quedarme sin insrucciones imprimo que el proceso terminó y decuelvo la RAM
    yield ram.put(memory_needed)
    print("\033[92mEl proceso %s fue finalizado en %.2f \t Instrucciones restantes: %d\033[0m"
          % (name, env.now, instructions))

    # Añado el tiempo total a la lista total_time para guardar resultados
    total_time.append(env.now - time)


environment = simpy.Environment()
RAM = simpy.Container(environment, init=RAM_memoria, capacity=RAM_memoria)
CPU = simpy.Container(environment, init=cantidad_CPU, capacity=cantidad_CPU)

for i in range(cantidad_procesos):
    environment.process(process(environment, i, RAM, CPU, CPU_ips, time_given, run_time, intervalos_procesos))

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

    if len(cantidades) > 1:
        return (r / (len(cantidades) - 1)) ** 0.5
    else:
        return 0


print("\nTiempos Totales:")
for tiempo in run_time:
    print(round(tiempo, 2))

print("\nTiempo Promedio: %.2f"
      "\nDesviación estándar poblacional: %.2f" % (promedio(run_time), desviacion(run_time)))
