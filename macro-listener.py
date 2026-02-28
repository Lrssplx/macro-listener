import serial
import time
import subprocess
import random

arduino = serial.Serial('COM3', 9600)
time.sleep(2)

while True:

    # Simulação temporária de temperatura
    cpu = random.randint(40, 70)
    gpu = random.randint(35, 65)

    arduino.write(f"CPU:{cpu}\n".encode())
    arduino.write(f"GPU:{gpu}\n".encode())

    if arduino.in_waiting:
        comando = arduino.readline().decode().strip()

        if comando == "RUN_TEST":
            print("Executando Cypress...")
            resultado = subprocess.run("npx cypress run", shell=True)

            if resultado.returncode == 0:
             print("Enviando TEST_OK")
             arduino.write("TEST_OK\n".encode())
        else:
             print("Enviando TEST_FAIL")
             arduino.write("TEST_FAIL\n".encode())

    time.sleep(3)