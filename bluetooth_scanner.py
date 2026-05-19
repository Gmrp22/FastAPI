import asyncio
from bleak import BleakScanner


async def scan(duration: int = 10):
    print(f"Escaneando dispositivos Bluetooth por {duration} segundos...\n")

    results = await BleakScanner.discover(timeout=duration, return_adv=True)

    if not results:
        print("No se encontraron dispositivos.")
        return

    print(f"{'MAC':<20} {'RSSI':<8} Nombre")
    print("-" * 60)

    items = sorted(results.values(), key=lambda x: x[1].rssi, reverse=True)
    for device, adv in items:
        name = device.name or "(sin nombre)"
        print(f"{device.address:<20} {adv.rssi:<8} {name}")

    print(f"\nTotal: {len(results)} dispositivo(s) encontrado(s).")


if __name__ == "__main__":
    asyncio.run(scan(duration=10))
