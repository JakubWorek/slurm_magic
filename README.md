P4: SLURM Magic — Jupyter Notebook Presentation

Contents:
- `slurm_student_lab.ipynb` — interactive lab for students using the local SLURM magics.
- `slurm_magic_presentation.ipynb` — shorter presentation-focused notebook.
- `slurm_magic.py` — local copy of the magic commands, patched to avoid the `squeue` tuple bug and to print cleaner output.
- `requirements.txt` — minimal Python packages for the notebook.
- `setup_env.sh` — creates a virtualenv and installs requirements.

Setup

Run:

```
cd p4_slurm_notebook
bash setup_env.sh
source venv/bin/activate
jupyter lab   # or jupyter notebook
```

Notes

- The lab notebook contains example `sbatch`, `srun`, and `salloc` snippets. On a non-SLURM system these commands will fail — they are instructional. On the cluster, run them from within the notebook or convert the presentation notebook to slides using `jupyter nbconvert --to slides slurm_magic_presentation.ipynb`.
- If you want a live slide view inside the notebook, install RISE (`pip install RISE`) after activating the env.
- Both notebooks load the local `slurm_magic.py` file directly inside the notebook, so the patched behavior is always used.
- The queue examples start with `%slurm display raw`; table output is available with `%slurm display pandas` after loading the local module.
