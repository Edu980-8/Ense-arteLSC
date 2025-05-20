import os
import matplotlib.pyplot as plt
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

log_path = "./logs"
losses = {"train/loss": [], "eval/loss": []}

# Recorre todos los logs
for root, dirs, files in os.walk(log_path):
    for file in files:
        if file.startswith("events.out.tfevents"):
            try:
                ea = EventAccumulator(os.path.join(root, file))
                ea.Reload()

                for key in losses.keys():
                    if key in ea.Tags()["scalars"]:
                        for s in ea.Scalars(key):
                            losses[key].append((s.step, s.value))
            except Exception as e:
                print(f"[!] Error leyendo {file}: {e}")

# Graficar
for name, data in losses.items():
    if data:
        data.sort()
        steps, values = zip(*data)
        plt.plot(steps, values, label=name)

if any(losses.values()):
    plt.xlabel("Steps")
    plt.ylabel("Loss")
    plt.title("Training and Eval Loss over Steps")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("❌ No se encontraron datos de loss.")
