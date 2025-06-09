# VSP

### **`macOS`** type the following commands : 

- We have also added a [Makefile](Makefile) which has the recipe called 'setup' which will run all the commands for setting up the environment.
Feel free to check and use if you are tired of copy pasting so many commands.

     ```BASH
    make setup
    ```
    After that active your environment by following commands:
    ```BASH
    source .venv/bin/activate
    ```
Or ....
- `Step_1:` Update Homebrew and install ffmpeg by following commands:
    ```sh
    brew update
    brew install ffmpeg
    ```
  Restart Your Terminal and than check the **ffmpeg version**  by run the following commands:
     ```sh
    ffmpeg -version
    ```
- `Step_2:` Install the virtual environment and the required packages by following commands:

    ```BASH
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
    
### **`WindowsOS`** type the following commands :

- `Step_1:` Update Chocolatey and install ffmpeg by following commands:
    ```sh
    choco upgrade chocolatey
    choco install ffmpeg
    ```
    Restart Your Terminal and then check the **ffmpeg version**  by running the following commands:
     ```sh
    ffmpeg -version
    ```

- `Step_2:` Install the virtual environment and the required packages by following commands.

   For `PowerShell` CLI :

    ```PowerShell
    pyenv local 3.11.3
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    For `Git-bash` CLI :
  
    ```BASH
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    **`Note:`**
    If you encounter an error when trying to run `pip install --upgrade pip`, try using the following command:
    ```Bash
    python.exe -m pip install --upgrade pip
    ```
  
