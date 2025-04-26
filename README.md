# Flappy

Vide coded with codexcli, this readme was written by chatgpt

A **minimal Flappy Bird–style prototype** written in Python with [Pygame](https://www.pygame.org/). It demonstrates sprite animation, gravity-based physics, and frame-rate-independent movement in fewer than 150 lines of code.

---

## 🎮 Gameplay

| Key | Action |
|-----|--------|
| **SPACE** | Flap upward |
| **Q** | Quit the game |

The bird continuously falls under gravity. Time your flaps to keep it in the air and off the ground.

---

## 📦 Requirements

* Python 3.8 or newer
* `pygame >= 2.0`

### Install dependencies

```bash
pip install --upgrade pygame
```

---

## 🚀 Running the game

```bash
# clone the repository
$ git clone https://github.com/daveManDaveDude/flappy.git
$ cd flappy

# launch the prototype
$ python flappy_03.py
```

If you are on macOS or Linux you may have multiple Python installations; replace `python` with `python3` as needed.

---

## 🗂️ Project structure

```
flappy/
├─ flappy_03.py         # main game script
├─ wings_level.png      # sprite frame – wings level
├─ wings_down.png       # sprite frame – wings down
├─ wings_up.png         # sprite frame – wings up
└─ __pycache__/         # byte-compiled cache (auto-generated)
```

---

## ⚙️ Configuration

Several constants at the top of `flappy_03.py` let you tweak gameplay without digging through the code:

```python
WIDTH = 400        # window width (px)
HEIGHT = 600       # window height (px)
FPS = 60           # target frames per second
GRAVITY = 200.0    # downward acceleration (px/s²)
JUMP_VELOCITY = -105.0  # flap impulse velocity (px/s)
RESTITUTION = 0.8  # bounciness on floor contact (0–1)
```

Experiment to find a feel you like!

---

## 🛣️ Roadmap / Ideas

* Add scrolling pipes and collision detection
* Score keeping and a game-over screen
* Sound effects for flap and collision events
* Difficulty scaling over time
* Packaging via `pipx` or a standalone executable with PyInstaller

Feel free to open an issue or pull request if you’d like to tackle one of these.

---

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/my-improvement`)
3. Commit your changes (`git commit -m "Add amazing improvement"`)
4. Push to the branch (`git push origin feature/my-improvement`)
5. Open a pull request

Please follow [PEP 8](https://peps.python.org/pep-0008/) and add docstrings where appropriate.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details. If no license file is present, the default copyright remains with the author.

---

## 🙏 Acknowledgements

* Original *Flappy Bird* concept by .GEARS Studios
* Inspired by countless tutorial prototypes
* Wing sprites created by chatgpt
