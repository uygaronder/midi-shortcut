import mido

def get_midi():
    input_device = mido.open_input()

    for message in input_device:
        print(input_device.name, message)

print(mido.get_input_names())

get_midi()