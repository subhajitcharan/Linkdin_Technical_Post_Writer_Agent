import tempfile
from git import Repo
from pathlib import Path
import os
from backend.project_pull.extract import notebook_file
import logging
os.environ["GIT_TERMINAL_PROMPT"] = "0"
def repo_pull(repo_url:str,CODE_EXTENSIONS = {".py", ".js", ".md", ".txt",".ipynb"}):
    full_content=''
    with tempfile.TemporaryDirectory() as temp_dir:
        Repo.clone_from(repo_url,temp_dir)
        temp_path=Path(temp_dir)
        for file_path in temp_path.rglob("*"):
            if file_path.is_file() and ".git" not in file_path.parts and "__init__.py" not in file_path.parts:
                if file_path.suffix in CODE_EXTENSIONS:
                    try:
                        if file_path.suffix=='.ipynb':
                            content=notebook_file(content)
                        else:
                            content=file_path.read_text(encoding="utf-8")
                        
                        full_content+=f"\n#Filename=={file_path.name}\n#content:\n{content}"
                    except Exception as e:
                        logging.exception(f'error for repo ->{repo_url},exception ->{e}')
    return full_content
                        

 



    