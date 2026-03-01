import serial
import time
import subprocess
import psutil
import wmi
from datetime import datetime

# ===== SERIAL =====
arduino = serial.Serial('COM5', 9600)  # ajuste se necessário
time.sleep(2)

# ===== OPEN HARDWARE MONITOR =====
w = wmi.WMI(namespace="root\OpenHardwareMonitor")

def get_gpu_usage():
    for sensor in w.Sensor():
        if sensor.SensorType == u'Load' and "GPU Core" in sensor.Name:
            return int(sensor.Value)
    return 0

def get_cpu_usage():
    return int(psutil.cpu_percent(interval=1))

def get_ram_usage():
    return int(psutil.virtual_memory().percent)

def get_current_branch():
    branch = subprocess.check_output(
        "git rev-parse --abbrev-ref HEAD",
        shell=True
    ).decode().strip()
    return branch

# ===== LOOP PRINCIPAL =====
while True:

    cpu = get_cpu_usage()
    ram = get_ram_usage()
    gpu = get_gpu_usage()
    branch = get_current_branch()

    # Envia dados de monitoramento
    arduino.write(f"CPU:{cpu}\n".encode())
    arduino.write(f"RAM:{ram}\n".encode())
    arduino.write(f"GPU:{gpu}\n".encode())
    arduino.write(f"BRANCH:{branch}\n".encode())

    # Escuta comandos do Arduino
    if arduino.in_waiting:
        comando = arduino.readline().decode().strip()

        # =============================
        # EXECUTAR TESTES
        # =============================
        if comando == "RUN_TEST":
            print("Executando Cypress...")
            resultado = subprocess.run("npx cypress run", shell=True)

            if resultado.returncode == 0:
                arduino.write("TEST_OK\n".encode())
            else:
                arduino.write("TEST_FAIL\n".encode())

        # =============================
        # AUTO COMMIT + PUSH
        # =============================
        elif comando == "GIT_PUSH":
            branch = get_current_branch()
            print(f"Commit automático na branch {branch}")

            subprocess.run("git add .", shell=True)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f'chore: auto commit via QA Panel - {now}'

            subprocess.run(f'git commit -m "{commit_msg}"', shell=True)

            arduino.write(f"PUSH_BRANCH:{branch}\n".encode())

            push_result = subprocess.run(f"git push origin {branch}", shell=True)

            if push_result.returncode == 0:
                arduino.write("PUSH_OK\n".encode())
            else:
                arduino.write("PUSH_FAIL\n".encode())

    time.sleep(2)