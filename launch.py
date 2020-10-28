import asyncio
import logging
import logging.handlers
import os
import sys

import aiohttp

import config
import senko

# Use uvloop event loop on linux systems when available.
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop(uvloop.EventLoopPolicy())


class Launcher:
    """
    A utility class that performs the initial setup, starts the bot and
    performs post-run cleanup.
    """

    def __init__(self):
        self.log = logging.getLogger("senko.launcher")

        self.path = None
        self.loop = None

        self.session = None
        self.db = None
        self.bot = None
        self.exit_code = 0
    
    def _setup(self):
        # Set up path, ensure logs directory exists and set working directory.
        self.path = os.path.dirname(os.path.abspath(__file__))
        logs = os.path.join(self.path, "logs")

        os.chdir(self.path)

        try:
            os.mkdir(logs)
        except OSError:
            pass

        self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)

        # Set up logging with a handler for stdout and a log file.
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        for domain, level in config.logging_levels:
            logging.getLogger(domain).setLevel(level)

        logging.getLogger("discord").setLevel(logging.WARNING)
        logging.getLogger("discord.http").setLevel(logging.WARNING)

        streamHandler = logging.StreamHandler(stream=sys.stdout)

        fileHandler = logging.handlers.TimedRotatingFileHandler(
            os.path.join(logs, "senko.log"),
            when="midnight",
            backupCount=7,
            encoding="utf-8",
            utc=True,
        )

        fmt = "{asctime} | {levelname:<8} | {name}: {message}"
        date = "%d.%m.%Y %H:%M:%S"
        formatter = logging.Formatter(fmt, date, style="{")

        for handler in (streamHandler, fileHandler):
            handler.setFormatter(formatter)
            root.addHandler(handler)

        # Create the client session and database connection pool.
        self.log.info("New session started.")
        self.loop.run_until_complete(self._create_session())
        self.loop.run_until_complete(self._create_pool())

    async def _create_session(self):
        # Creates the client session.
        self.log.info("Creating client session.")
        try:
            self.session = aiohttp.ClientSession(loop=self.loop)
        except Exception as exc:
            self.log.exception("Could not create client session!", exc_info=exc)
            raise

    async def _create_pool(self):
        # Creates the asyncpg connection pool.
        self.log.info("Creating database connection pool.")
        try:
            self.db = await senko.init_db(**config.database_credentials)
        except Exception as exc:
            self.log.exception("Could not connect to database!", exc_info=exc)
            raise

    async def _close_session(self):
        # Closes the client session.
        try:
            await self.session.close()
        except:
            pass

    async def _close_pool(self):
        # Closes the asyncpg connection pool.
        try:
            await self.db.close()
        except:
            pass

    def _cleanup(self):
        self.log.info("Performing cleanup.")

        # Nothing left to do if the loop is already closed.
        if self.loop.is_closed():
            return
        
        # If the loop has not yet been closed, close the client session and
        # database connection pool.
        self.log.info("Cleaning up client session and database pool.")
        self.loop.run_until_complete(self._close_session())
        self.loop.run_until_complete(self._close_pool())

        # Stop the event loop, if not yet closed, and stop pending tasks.
        self.log.info("Consuming unhandled exceptions.")
        self.loop.stop()
        tasks = asyncio.all_tasks(loop=self.loop)
        self.log.info(f"Cancelling {len(tasks)} task(s).")

        for task in tasks:
            if not task.done():
                task.cancel()
                # Print some info about the tasks we're closing.
                coro = task.get_coro()
                file = coro.cr_code.co_filename
                line = coro.cr_code.co_firstlineno
                name = coro.cr_code.co_name
                self.log.info(f"Cancelling {name!r} at {file}:{line}.")
                try:
                    # Let the task be cancelled and silence the exception.
                    self.loop.run_until_complete(task)
                except:
                    pass
            elif not task.cancelled() and task.exception() is not None:
                error = task.exception()
                self.log.exception(f"Unhandled exception in {task}!", exc_info=error)

        # Clean up the event loop if it has not yet been closed.
        self.log.info("Forcibly closing the event loop.")
        try:
            self.loop.close()
        except Exception as exc:
            self.log.exception("An error has occured while closing the event loop!", exc_info=exc)

    def _run(self):
        # Perform initial setup.
        try:
            self._setup()
        except Exception as exc:
            self.log.exception("An error occured during setup!", exc_info=exc)
            self.exit_code = 1
            return

        # Create the bot instance.
        self.log.info("Setting up bot.")
        try:
            bot = senko.Senko(db=self.db, session=self.session, loop=self.loop)
        except Exception as exc:
            self.log.exception("An error occured during initialization!", exc_info=exc)
            self.exit_code = 1
            return

        # Run the bot.
        try:
            self.exit_code = bot.run()
        except Exception as exc:
            self.log.exception("An error occured while running!", exc_info=exc)
            self.exit_code = 1
            return

    def run(self):
        """
        Start the launcher. This method will block
        until the bot is terminated.

        Returns
        -------
        int
            The :ref:`exit code <exit_codes>`.
        """
        self._run()
        self._cleanup()
        self.log.info(f"Closed with code {self.exit_code}.")
        logging.shutdown()
        return self.exit_code


if __name__ == "__main__":
    launcher = Launcher()
    sys.exit(launcher.run())
