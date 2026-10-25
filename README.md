# Wealth Clicker

A desktop wealth-building game made with Python and Tkinter. Earn money by clicking, invest in income-producing properties and businesses, trade a simulated stock market, and collect cars, jets, and yachts.

**Description**  
Build your fortune in a Python desktop clicker game. Earn cash, invest in businesses and real estate, trade a simulated stock market, and collect cars, jets, and yachts. Your progress and portfolio are saved between sessions.

## Features

- Earn **$1 per click** and watch your balance grow.
- Buy real estate and businesses that generate passive income.
- Continue earning passive income while the game is closed.
- Browse and collect cars, private jets, and yachts; choose basic or standard engine/crew options when available.
- Trade 19 fictional stocks in a simulated market with price charts, share quantities, and portfolio profit/loss details.
- Automatically save your balance, purchases, income, stock prices, and portfolio.
- Browse asset images from the included `Assets/` folders. Some item images are requested online; unavailable remote images use a placeholder.
- Asset prices are approximate USD reference prices; actual prices vary by model year, configuration, condition, and market. Yacht and aircraft prices are especially dependent on the specific model and build.

## Requirements

- Python 3
- Tkinter (usually included with the standard Python installation on Windows)
- Pillow
- Requests
- An internet connection for item images hosted online; local images and the game itself are available offline.

## Run the game

Open a terminal in this folder, install the Python packages, and start the game:

```powershell
py -m pip install Pillow requests
py Whole_game.py
```

If the `py` command is not available, use `python` instead:

```powershell
python -m pip install Pillow requests
python Whole_game.py
```

On Linux, you may need to install your distribution's Tkinter package (often named `python3-tk`) before launching the game.

## How to play

1. On **Home**, click the money button to earn cash.
2. Use the **Real Estate** tab to buy properties that add passive income.
3. Open **Businesses** to browse companies and see the ones you own.
4. Visit **Shop** to browse cars, jets, and yachts. Some purchases offer basic or standard engine/crew options; standard costs 10% more.
5. Use **Stock Market** on Home to select a fictional stock, enter a whole-number share quantity, and buy or sell. Prices update periodically.
6. Check **Liabilities** for your owned cars, jets, and yachts.

The stock market is simulated and has no connection to real securities or exchanges.

## Project files

```text
.
├── Whole_game.py                 # Game application
├── wealth_clicker_save.json      # Local game progress (created/updated by the game)
└── Assets/
    ├── Cars/
    ├── Jets/
    ├── Real_Estate/
    └── Yachts/
```

Keep the `Assets/` directory alongside `Whole_game.py`; the game uses relative asset paths. The save file is also stored beside the script. Back it up before deleting it. To share a clean starting state, close the game and remove the save file before publishing or running it; the game will create a new one.

## Images and licensing

Most images are bundled in `Assets/`; some item images are fetched from Wikimedia Commons URLs at runtime. Image availability for remote images depends on the network. Check the terms and attribution requirements for each image before redistributing it.

The following bundled car images are from Wikimedia Commons:

- Ferrari 296 GTB photo by MrWalkr, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Ferrari_296_GTB.jpg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- Rolls-Royce Phantom photo by IFCAR, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Rolls-Royce_Phantom.jpg), public domain.

No project license is included. Add a `LICENSE` file if you want to specify how others may use, modify, or redistribute the project.
