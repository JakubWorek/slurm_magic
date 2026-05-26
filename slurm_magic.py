
from __future__ import print_function

import inspect
import io
import os
import shlex
import sys
from subprocess import (Popen, PIPE)

import pandas

from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic,
        line_cell_magic)
from IPython.core.magic_arguments import (argument, magic_arguments,
        parse_argstring)


def modal(func):
    def wrapped_func(obj, line):
        result = func(obj, line)
        if isinstance(result, tuple):
            stdout_text, stderr_text = result
        else:
            stdout_text, stderr_text = result, ""
        if obj._display == "pandas":
            if stderr_text:
                sys.stderr.write(stderr_text)
                if not stderr_text.endswith("\n"):
                    sys.stderr.write("\n")
            if not isinstance(stdout_text, str):
                stdout_text = str(stdout_text)
            if not stdout_text.strip():
                return pandas.DataFrame()
            return pandas.read_table(io.StringIO(stdout_text), sep='\s+',
                    on_bad_lines="skip")

        if stdout_text:
            sys.stdout.write(stdout_text)
            if not stdout_text.endswith("\n"):
                sys.stdout.write("\n")
        if stderr_text:
            sys.stderr.write(stderr_text)
            if not stderr_text.endswith("\n"):
                sys.stderr.write("\n")
        return None
    wrapped_func.__doc__ = func.__doc__
    return wrapped_func


@magics_class
class SlurmMagics(Magics):

    def __init__(self, shell=None, **kwargs):
        super(SlurmMagics, self).__init__(shell, **kwargs)
        self._display = "pandas"

    @line_magic
    def slurm(self, line):
        chunks = line.lower().split()
        variable, arguments = chunks[ 0 ], chunks[ 1 : ]
        if variable == "display" :
            return self._configure_display(arguments)

    def _configure_display(self, arguments):
        if arguments:
            mode = arguments[0]
            if mode not in [ "pandas", "raw" ] :
                raise ValueError("Unknown Slurm magics display mode", mode)
            self._display = mode
        return self._display

    @modal
    @line_magic
    def sacct(self, line):
        """Display accounting data for all jobs and job steps in the Slurm job
        accounting log or Slurm database."""
        return self._execute(line)

    @modal
    @line_magic
    def sacctmgr(self, line):
        """View and modify Slurm account information."""
        return self._execute(line)

    @line_magic
    def salloc(self, line):
        """Obtain a Slurm job allocation (a set of nodes), execute a command,
        and then release the allocation when the command is finished."""
        result = self._execute(line)
        if result:
            sys.stdout.write(result)
            if not result.endswith("\n"):
                sys.stdout.write("\n")
        return None

    @line_magic
    def sattach(self, line):
        """Attach to a Slurm job step."""
        pass

    @line_cell_magic
    def sbatch(self, line, cell=None):
        """Submit a batch script to Slurm."""
        # FIXME Document further.
        if cell is None:
            result = self._execute(line)
        else:
            result = self._execute(line, input=cell.encode(encoding='UTF-8'))
        if result:
            sys.stdout.write(result)
            if not result.endswith("\n"):
                sys.stdout.write("\n")
        return None

    @line_magic
    def sbcast(self, line):
        """Transmit a file to the nodes allocated to a Slurm job."""
        pass

    @line_magic
    def scancel(self, line):
        """Used to signal jobs or job steps that are under the control of
        Slurm."""
        result = self._execute(line)
        if result:
            sys.stdout.write(result)
            if not result.endswith("\n"):
                sys.stdout.write("\n")
        return None

    @line_magic
    def scontrol(self, line):
        """Used view and modify Slurm configuration and state."""
        result = self._execute(line)
        if result:
            sys.stdout.write(result)
            if not result.endswith("\n"):
                sys.stdout.write("\n")
        return None

    @modal
    @line_magic
    def sdiag(self, line):
        """Scheduling diagnostic tool for Slurm."""
        return self._execute(line)

    @modal
    @line_magic
    def sinfo(self, line):
        """View information about Slurm nodes and partitions."""
        return self._execute(line)

    @line_magic
    def smap(self, line):
        """Graphically view information about Slurm jobs, partitions, and set
        configurations parameters."""
        pass

    @modal
    @line_magic
    def sprio(self, line):
        """View the factors that comprise a job's scheduling priority."""
        return self._execute(line)

    @modal
    @line_magic
    def squeue(self, line):
        """View information about jobs located in the Slurm scheduling
        queue."""
        return self._execute(line)

    @line_magic
    def sreport(self, line):
        """Generate reports from the slurm accounting data."""
        pass

    @line_magic
    def srun(self, line):
        """Run parallel jobs."""
        result = self._execute(line)
        if result:
            sys.stdout.write(result)
            if not result.endswith("\n"):
                sys.stdout.write("\n")
        return None

    @modal
    @line_magic
    def sshare(self, line):
        """Tool for listing the shares of associations to a cluster."""
        return self._execute(line)

    @line_magic
    def sstat(self, line):
        """Display various status information of a running job/step."""
        pass

    @line_magic
    def strigger(self, line):
        """Used set, get or clear Slurm trigger information."""
        pass

    @line_magic
    def sview(self, line):
        """Graphical user interface to view and modify Slurm state."""
        pass

    def _execute(self, line, input=None, stderr=False):
        name = inspect.stack()[1][3]
        expanded_line = os.path.expandvars(line)
        process = Popen([name] + shlex.split(expanded_line), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr_output = process.communicate(input)
        stdout_text = stdout.decode("utf-8")
        stderr_text = stderr_output.decode("utf-8")
        if stderr_text and stderr:
            return stdout_text, stderr_text
        if stderr_text:
            return stdout_text + ("\n" if stdout_text else "") + stderr_text
        return stdout_text


def load_ipython_extension(ip):
    """Load extension in IPython."""
    slurm_magic = SlurmMagics(ip)
    ip.register_magics(slurm_magic)