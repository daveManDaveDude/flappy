# Flappy

Vide coded with codexcli, this readme was written by chatgpt

A **minimal Flappy Bird–style prototype** written in Python with [Pygame](https://www.pygame.org/). It demonstrates sprite animation, gravity-based physics, and frame-rate-independent movement in fewer than 150 lines of code.

---

## 🎮 Gameplay

| Key | Action |
|-----|--------|
| **SPACE** | Flap upward |
| **Q** | Quit the game |
| **D** | Cycle debug modes: show collision circle & pipe speed → disable collisions → off |

The bird continuously falls under gravity. Time your flaps to keep it in the air and off the ground.

* In debug mode, a collision circle is drawn around the bird and the current pipe speed is shown in the UI.
* When collisions are disabled (second debug state), an asterisk (*) is appended to the score display to indicate no-collision mode.

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
$ python run.py
```

If you are on macOS or Linux you may have multiple Python installations; replace `python` with `python3` as needed.

---

## 🗂️ Project structure

```
flappy/
├─ run.py               # entry-point script
├─ game.py              # orchestrates game loop, physics, and state
├─ bird.py              # Bird sprite: physics & animation
├─ pipe.py              # Pipe obstacle: geometry & rendering
├─ assets.py            # image-loading utility with caching
├─ settings.py          # configuration constants (physics, colors, UI)
├─ utils.py             # collision detection & randomization helpers
├─ input_handler.py     # maps raw Pygame events to high-level actions
├─ renderer.py          # encapsulates all drawing logic
├─ sprites/             # image assets (wing frames)
│   ├─ wings_down.png
│   ├─ wings_level.png
│   └─ wings_up.png
└─ __pycache__/         # byte-compiled cache (auto-generated)
```

---

## ⚙️ Configuration

Game constants live in `settings.py`. Feel free to tweak any of these values:

```python
WIDTH = 800               # window width (px)
HEIGHT = 600              # window height (px)
FPS = 60                  # target frames per second
GRAVITY = 200.0           # downward acceleration (px/s²)
JUMP_VELOCITY = -105.0    # flap impulse velocity (px/s)
RESTITUTION = 0.8         # bounce damping on pipes (0–1)
SCALE_FACTOR = 8          # image scaling divisor
FRAME_DURATION = 80       # ms per bird animation frame
PIPE_WIDTH = 50           # width of each pipe (px)
PIPE_GAP = 150            # vertical gap between pipes (px)
PIPE_SPEED = 100          # horizontal speed of pipes (px/sec)
PIPE_SPAWN_INTERVAL = 3500 # ms between spawning new pipes
PIPE_MIN_HEIGHT = 50      # minimum height for pipe segments (px)
PIPE_VARIANCE = 0.2       # variability fraction for gap/spawn interval
PIPE_BOUNCE_CHANCE = 0.2  # probability a pipe has a bounce zone (0–1)
PIPE_BOUNCE_STRIPE_HEIGHT = 5  # height of the bounce-zone stripe (px)
```  

Experiment to find a feel you like!

---

## 📐 Code Organization

This project follows a modular structure:
  • run.py            – entry point, instantiates and runs Game
  • game.py           – high-level game state, update loop, collision & scoring
  • input_handler.py  – isolates input/event processing
  • renderer.py       – centralizes all rendering and UI drawing
  • bird.py           – Bird sprite: movement, gravity, animation
  • pipe.py           – Pipe sprite: gap generation, movement, bounce logic
  • assets.py         – image loading & caching utility
  • settings.py       – tunable constants (dimensions, speeds, colors)
  • utils.py          – shared helpers (collision tests, randomized gaps/spawns)

---

## 🛣️ Roadmap / Ideas

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

Please follow [PEP 8](https://peps.python.org/pep-0008/), include type hints and docstrings,
and consider using a formatter (e.g. black), linter (flake8), and import sorter (isort).
We welcome updates to pre-commit configs or CI workflows to enforce code quality.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details. If no license file is present, the default copyright remains with the author.

---

## 🙏 Acknowledgements

* Original *Flappy Bird* concept by .GEARS Studios
* Inspired by countless tutorial prototypes
* Wing sprites created by chatgpt
