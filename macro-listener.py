import serial
import time
import subprocess
import random
from datetime import datetime

arduino = serial.Serial('COM3', 9600)
time.sleep(2)

def get_current_branch():
    branch = subprocess.check_output(
        "git rev-parse --abbrev-ref HEAD",
        shell=True
    ).decode().strip()
    return branch

while True:

    # Simulação de temperatura
    cpu = random.randint(40, 70)
    gpu = random.randint(35, 65)

    arduino.write(f"CPU:{cpu}\n".encode())
    arduino.write(f"GPU:{gpu}\n".encode())

    if arduino.in_waiting:
        comando = arduino.readline().decode().strip()

        # =========================
        # EXECUTAR TESTES
        # =========================
        if comando == "RUN_TEST":
            print("Executando Cypress...")
            resultado = subprocess.run("npx cypress run", shell=True)

            if resultado.returncode == 0:
                arduino.write("TEST_OK\n".encode())
            else:
                arduino.write("TEST_FAIL\n".encode())

        # =========================
        # AUTO COMMIT + PUSH
        # =========================
        elif comando == "GIT_PUSH":

            branch = get_current_branch()
            print(f"Preparando commit automático na branch {branch}...")

            # Adiciona arquivos
            subprocess.run("git add .", shell=True)

            # Mensagem com timestamp
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f'chore: auto commit via QA Panel - {now}'

            # Tenta fazer commit
            commit_result = subprocess.run(
                f'git commit -m "{commit_msg}"',
                shell=True
            )

            if commit_result.returncode != 0:
                print("Nenhuma alteração para commit.")

            # Envia nome da branch para o LCD
            arduino.write(f"PUSH_BRANCH:{branch}\n".encode())

            print(f"Executando git push origin {branch}...")
            push_result = subprocess.run(
                f"git push origin {branch}",
                shell=True
            )

            if push_result.returncode == 0:
                arduino.write("PUSH_OK\n".encode())
            else:
                arduino.write("PUSH_FAIL\n".encode())

    time.sleep(2)