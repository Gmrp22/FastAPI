import subprocess
import asyncio
from bleak import BleakScanner, BleakClient

TARGET_NAME = "JBL Charge 5"


def blueutil_disconnect(address: str) -> bool:
    result = subprocess.run(
        ["blueutil", "--disconnect", address],
        capture_output=True, text=True
    )
    return result.returncode == 0


async def find_and_disconnect():
    print(f"Buscando '{TARGET_NAME}'...")
    results = await BleakScanner.discover(timeout=8, return_adv=True)

    target = None
    for device, adv in results.values():
        if device.name and TARGET_NAME.lower() in device.name.lower():
            target = (device, adv)
            break

    if not target:
        print(f"No se encontro '{TARGET_NAME}'. Asegurate de que este encendida.")
        return

    device, adv = target
    print(f"Encontrado: {device.name} | {device.address} | RSSI: {adv.rssi}")

    # Intento 1: blueutil (desconexion clasica de macOS)
    print("\n[1] Intentando desconectar via blueutil...")
    if blueutil_disconnect(device.address):
        print("    Desconectado exitosamente.")
        return

    # Intento 2: BLE connect/disconnect
    print("[2] Intentando via BLE connect/disconnect...")
    print(f"    RSSI actual: {adv.rssi} dBm", end="")
    if adv.rssi < -85:
        print(" (señal muy debil, puede fallar)")
    else:
        print()

    try:
        client = BleakClient(device.address, timeout=15.0)
        await client.connect()
        print(f"    Conectado. Servicios encontrados: {len(client.services)}")
        await client.disconnect()
        print("    Desconectado.")
    except Exception as e:
        print(f"    Error: {type(e).__name__}: {e}")
        print("    Posibles causas:")
        print("      - Señal demasiado debil (acercate a la bocina)")
        print("      - Ya esta conectada a otro dispositivo y no acepta mas")
        print("      - macOS bloqueo la conexion (verifica permisos Bluetooth)")


if __name__ == "__main__":
    asyncio.run(find_and_disconnect())
