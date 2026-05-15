# Laser-Microphone
> Reconstructing sound from light using a laser and photodiode. 

---

## Overview
This project demonstrates how sound vibrations on a reflective surface (glass/window)
can be reconstructed using a laser beam and a photodiode sensor.

Instead of recording sound directly, the system captures tiny light fluctuations
caused by surface vibrations and converts them back into audio.

---

## Project Media

### Animation / Working Principle
> Drive Link : [Access media here (Videos + images)](https://drive.google.com/drive/folders/1l8H-hZZI1A3veK387arMd_2Nyy2kBWVW?usp=sharing)

[![Diagram](media/Intro_label.png)](media/Intro_label.png)
[![Diagram](media/hardware.png)](media/hardware.png)
[![Diagram](media/hand_interupt.png)](media/hand_interupt.png)

### Circuit Diagram
[![Diagram](media/circuit_diagram.jpg)](media/circuit_diagram.jpg)

### Workflow
[![Diagram](media/workflow.jpg)](media/workflow.jpg)

### Output Samples
You can listen to reconstructed audio samples here:

## Hardware Used
| Component | Purpose |
|----------|----------|
| Laser Module | Sends laser beam |
| Photodiode | Detects reflected light |
| LM386 Amplifier | Amplifies weak signal |
| LM2596 Step Down | Voltage regulation |
| AUX Output | Audio output |
| USB Power | Power supply |

---

## Working Principle

1. Laser beam is directed at a reflective surface.
2. Sound causes microscopic vibrations on the surface.
3. Reflected laser intensity changes slightly.
4. Photodiode detects these changes.
5. LM386 amplifies the signal.
6. Audio is reconstructed through AUX output.

---

## Improvements
- Better noise filtering
- Long-distance testing
- DSP-based audio cleanup
- Higher sensitivity photodiodes
- Stable laser mounting

---

## Limitations
- Sensitive to vibrations
- Ambient light interference
- Requires accurate alignment
- Low signal strength

---

## Concepts Used
- Optical sensing
- Signal amplification
- Audio processing
- Photodiode response
- Vibration detection

---

## Author(build, design and execution)
Aryan 
