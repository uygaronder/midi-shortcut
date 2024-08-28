import mido

from modules.system_controller import accept_input

def midi_listener(loaded_data):
    midiDevices = mido.get_input_names()

    # listen to all available devices
    with mido.open_input() as inport:
        for msg in inport:
            print("msg: ",msg)
            for device in loaded_data['devices']:
                for input in device['inputs']:
                    if input['type'] == msg.type and input['channel'] == msg.channel:
                        if (input['type'] == 'note_on' and input['note'] == msg.note) or (input['type'] == 'control_change' and input['control'] == msg.control):
                            accept_input(msg, input)
