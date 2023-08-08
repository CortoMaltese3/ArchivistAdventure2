# Archivist Adventure 2

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
