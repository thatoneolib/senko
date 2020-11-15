import asyncio
import logging
import sys
import datetime

__all__ = ("GitError", "NoRepository", "NoCommits", "Git")

class GitError(Exception):
    """
    The base exception for git-related errors.
    """

class NoRepository(GitError):
    """
    Exception raised when calling any :class:`Git` methods
    when the working directory is not a valid git repository.
    """

class NoCommits(GitError):
    """
    Exception raised when calling certain :class:`Git` methods
    that require at least one commit to exist when there is no
    commit.
    """

class Commit:
    """
    A container class representing a commit made to a git repository.

    All parameters are exposed as attributes.

    Parameters
    ----------
    hash: str
        The commit hash.
    short_hash: str
        The abbreviated commit hash.
    author_name: str
        The author name.
    author_mail: str
        The author e-mail.
    timestamp: datetime.datetime
        An aware UTC timestamp of the commit date.
    subject: str
        The commit subject.
    body: str
        The commit body.
    """
    def __init__(self, hash, short_hash, author_name, author_mail, timestamp, subject, body):
        self.hash = hash
        self.short_hash = short_hash
        self.author_name = author_name
        self.author_mail = author_mail
        self.timestamp = timestamp
        self.subject = subject
        self.body = body

    @classmethod
    def from_data(self, *args):
        """
        Create a new :class:`Commit` from a sequence of arguments.

        This is internally used by :class:`Git` to create commit objects.

        Parameters
        ----------
        \*args
            An argument list of values to create the commit from.
        
        Returns
        -------
        Commit
            A new commit object created from the given set of values.
        """
        return Commit(
            args[0],
            args[1],
            args[2],
            args[3],
            datetime.datetime.fromtimestamp(int(args[4]), tz=datetime.timezone.utc),
            args[5],
            args[6]
        )
   
    def __str__(self):
        return f"<Commit hash={self.hash}>"

class Git:
    """
    Implements a simple interface to interact with the git repository in the
    working directory.

    Requires the working directory, as returned by :meth:`os.getcwd`, to be a
    valid, initialized git repository and the ``git`` command to be available
    on the current system.

    .. important::

        On Windows operating systems, the event loop must be an instance
        of :class:`asyncio.ProactorEventLoop`, otherwise using any of the
        methods of this class will cause errors.

    .. note::

        On Linux operating systems all ``git`` commands will be run with
        ``sudo`` prepended. This may lead to issues with permissions if
        the current user can not use ``sudo``.
    
    Parameters
    ----------
    loop: asyncio.AbstractEventLoop
        The event loop to use.
    """
    def __init__(self, loop):
        self.loop = loop
        self.log = logging.getLogger("senko.utils.git")

        # Use sudo on Linux.
        if sys.platform == "linux":
            self._command = ("sudo", "git")
        else:
            self._command = ("git",)

    async def run(self, *args):
        """
        Run a git command and return the results.

        Takes any amount of positional arguments to append to
        the ``git`` command as supported by the operating system.

        Returns
        -------
        str
            The console output.
        """
        process = await asyncio.create_subprocess_exec(
            *self._command,
            *args,
            loop=self.loop,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        stdout = stdout.decode("utf-8").strip()
        stderr = stderr.decode("utf-8").strip()

        # Handle errors.
        if stderr != "" and stderr.startswith("fatal:"):
            error = stderr.split("\n")[0].replace("fatal: ", "", 1)
            command = " ".join(self._command + args)
            info = f"An error occured while running {command!r}: {error}"

            if stderr.startswith("fatal: not a git repository"):
                raise NoRepository(info)
            elif stderr.startswith("fatal: your current branch") and stderr.endswith("does not have any commits yet"):
                raise NoCommits(info)
            else:
                raise GitError(info)
        
        # Otherwise just return stdout.
        return stdout

    async def in_repo(self):
        """
        Check whether the working directory is a valid git repository.

        Returns
        -------
        bool
            ``True`` if the working directory is a valid git repository,
            otherwise ``False``.
        """
        try:
            in_tree = await self.run("rev-parse", "--is-inside-work-tree")
        except GitError:
            return False

        return (in_tree == "true")

    async def is_behind_remote(self):
        """
        Checks whether the local branch is behind, or has diverged from the
        remote.

        Raises
        ------
        GitError
            When an error occurs during command execution.
        NoRepository
            When the working directory is not a valid git repository.
        
        Returns
        -------
        bool
            A boolean indicating whether the locla branch is behind
            the remote.
        """
        branch = await self.run("rev-parse", "--abbrev-ref", "HEAD")
        await self.run("remote", "update")

        branch_range = f"{branch}..origin/{branch}"
        revisions = await self.run("rev-list", "--count", branch_range)
        return int(revisions) > 0

    async def pull_from_remote(self):
        """
        Pull the latest available revision from the remote.

        Internally calls ``git pull --ff-only`` on the working directory.

        .. warning::

            If the local branch has diverged from the remote this can and most
            likely will change files. It is recommended the bot is restarted
            after calling this, to apply any changes that were made.

        Raises
        ------
        GitError
            When an error occurs during command execution.
        NoRepository
            When the working directory is not a valid git repository.
        """
        await self.run("pull", "--ff-only")

    async def get_branch(self):
        """
        Returns the name of the local branch.

        Raises
        ------
        GitError
            When an error occurs during command execution.
        NoRepository
            When the working directory is not a valid git repository.
        
        Returns
        -------
        str
            The name of the local branch.
        """
        return await self.run("rev-parse", "--abbrev-ref", "HEAD")

    async def get_commit_count(self, no_merges=True):
        """
        Returns the total amount of commits in the local branch.

        Ignores merge commits by default.

        Parameters
        ----------
        no_merges: Optional[bool]
            Whether to not include merge commits in the calculation.
            Defaults to ``True``.
        
        Raises
        ------
        GitError
            When an error occurs during command execution.
        NoRepository
            When the working directory is not a valid git repository.
        NoCommits
            If the repository does not yet have any commits.
        
        Returns
        -------
        int
            The amount of commits.
        """
        args = ("rev-list", "HEAD", "--count")
        if no_merges:
            args += ("--no-merges", )

        commits = await self.run(*args)
        return int(commits)

    async def get_latest_commit(self, offset=0, no_merges=True):
        """
        Fetches information about the last commit.

        The desired commit can be offset using the ``offset`` parameter.

        Ignores merge commits by default.

        Returns a dictionary containing the following keys:

        Parameters
        ----------
        offset: Optional[int]
            The offset of the commit to return. Defaults to 0,
            returning the most recent commit.
        no_merges: Optional[bool]
            Whether to not include merge commits. Defaults to ``True``.
        
        Raises
        ------
        GitError
            When an error occurs during command execution.
        NoRepository
            When the working directory is not a valid git repository.
        NoCommits
            If the repository does not yet have any commits.
        
        Returns
        -------
        Optional[Commit]
            A commit instance representing the requested commit, or ``None``
            if the requested commit does not exist.
        """
        # See https://git-scm.com/docs/pretty-formats for format parameters.
        # hash        = %H
        # short hash  = %h
        # author name = %an
        # author mail = %ae
        # timestamp   = %ct (unix timestamp)
        # subject     = %s
        # body        = %b

        args = (
            "log",
            "-1",
            "--pretty=%H%n%h%n%an%n%ae%n%ct%n%s%n%b",
            f"--skip={offset}",
        )

        if no_merges:
            args = args + ("--no-merges", )

        data = await self.run(*args)

        if data == "":
            return None

        sequence = data.split("\n", 7)
        if len(sequence) < 7:
            sequence += [""] * (7 - len(sequence))
        
        return Commit.from_data(*sequence)
