from cx_Freeze import setup, Executable

exe = Executable(
                 script="Program.py",
                 base="Win32GUI",
                 )

setup(
      name="Anansi WebCalc",
      version="0.1.0.0",
      description= "A calculator that aggreates news as you use it.",
      executables = [exe]
      )