import asyncio

import bleak.exc
from bleak import BleakScanner
from bleak import BleakClient




async def main():
    stall = True
    while stall:
        devices = await BleakScanner.discover()
        for device in devices:
            print(device)
            if device.name == "Kano-4SB-54-aa-59":
                print("FOUND DEVICE")
                ADDY = device.address
                stall = False
                break

    async with BleakClient(ADDY) as client:
        print(f"Connected: {client.is_connected}")

        paired = await client.pair(protection_level=2)
        print(f"Paired: {paired}")

        services = await client.get_services()
        for service in services:
            #print(f" Client services available: {service} \n\n")
            for char in service.characteristics:
                descriptors = char.descriptors
                for descriptor in descriptors:
                    handle = descriptor.handle

                    value = await client.read_gatt_descriptor(handle)
                    try:
                        data = await client.read_gatt_char(char.handle)
                        print(f"{char.handle}      is currently sending this data {data}")
                    except(bleak.exc.BleakError):
                        print(f" Aparently reading {char.handle}   is not permitted")



                    print(f"This feature does: {value} ")
                    print(f"It's char handle is {char.handle} while its descriptor handle is {handle} \n\n")


                    for i in range(20):
                        binary = bin(i)[2:]
                        binary_data = bytes([int(binary, 2)])
                        await client.write_gatt_char(37, binary_data)




asyncio.run(main())
