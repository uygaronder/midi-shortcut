import mido

def midi_listener(loaded_data):
    midiDevices = mido.get_input_names()

    # listen to all available devices
    with mido.open_input() as inport:
        for msg in inport:
            for device in loaded_data['devices']:
                for input in device['inputs']:
                    if input['type'] == msg.type and input['channel'] == msg.channel:
                        if (input['type'] == 'note_on' and input['note'] == msg.note) or (input['type'] == 'control_change' and input['control'] == msg.control):
                            print(f"Matched: {input}")