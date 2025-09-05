"""
Script para limpar arquivos de cache Python
"""

import os
import shutil
import glob

def clean_python_cache():
    """Remove todos os arquivos __pycache__ e .pyc"""
    
    print("🧹 Limpando arquivos de cache Python...")
    
    # Remover pastas __pycache__
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    for dir_path in pycache_dirs:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"  ✅ Removido: {dir_path}")
    
    # Remover arquivos .pyc
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    for file_path in pyc_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"  ✅ Removido: {file_path}")
    
    # Remover arquivos .pyo
    pyo_files = glob.glob("**/*.pyo", recursive=True)
    for file_path in pyo_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"  ✅ Removido: {file_path}")
    
    print("✨ Limpeza concluída!")

if __name__ == "__main__":
    clean_python_cache()
