# Archivist Adventure 2

Embark on a captivating journey in "ArchivistAdventure2," a retro-inspired RPG that blends the charm of the classic titles. Play as a courageous young archivist, whose mission is to rescue her partner imprisoned by malevolent spirits and their wicked minions.

Travel through a world rich with history, puzzles, and secrets. Along the way, meet supportive friends and family who will equip you with essential weapons, share arcane magic, and impart valuable information. Face off against nefarious foes, solve intricate puzzles, and unravel the mysteries that surround you.

"ArchivistAdventure2" offers a compelling narrative filled with twists and turns, engaging battles, and a beautiful pixel-art world to explore. Every decision matters, every clue counts. Will you save your partner and defeat the evil that plagues the land?

Discover the adventure, experience the magic, and become the hero in "ArchivistAdventure2."

## For Local Development

### Using Conda (Recommended)

1. **Create a New Conda Environment from `environment.yml` File:**

   ```bash
   conda env create -f environment.yml

   ```

2. **Activate the Conda Environment archivist_adventure_2**

   ```bash
   conda activate archivist_adventure_2

   ```

### Using pip (Alternative)

1. **Create a Virtual Environment (Optional):**

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   ```

2. **Install Dependencies from `requirements.txt`:**

   ```bash
   pip install -r requirements.txt

   ```

## Package the Application

To package the application as a standalone executable, use PyInstaller with the provided spec file:

```bash
pyinstaller archivist_adventure_2.spec

```

This will create an executable file in the dist directory, which you can then distribute to users.
