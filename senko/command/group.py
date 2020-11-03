import asyncio
import functools

import senko
from discord.ext import commands
from senko import LocaleMixin

from .overrides import CommandOverrides

# The following function was copied from discord.py's source code.
# Source: https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py
# License: https://github.com/Rapptz/discord.py/blob/master/LICENSE

def hooked_wrapped_callback(command, ctx, coro):
    @functools.wraps(coro)
    async def wrapped(*args, **kwargs):
        try:
            ret = await coro(*args, **kwargs)
        except commands.CommandError:
            ctx.command_failed = True
            raise
        except asyncio.CancelledError:
            ctx.command_failed = True
            return
        except Exception as exc:
            ctx.command_failed = True
            raise commands.CommandInvokeError(exc) from exc
        finally:
            if command._max_concurrency is not None:
                await command._max_concurrency.release(ctx)

            await command.call_after_hooks(ctx)
        return ret

    return wrapped


class Group(LocaleMixin, CommandOverrides, commands.Group):
    """
    A :class:`discord.ext.commands.Group` modified with
    :class:`senko.CommandOverrides`.

    The key differences to the original class are as follows:

    * By default, ``case_insensitive`` is set to ``True``.
    * The :meth:`senko.Group.command` decorator returns a :class:`senko.Command`.
    * The :meth:`senko.Group.group` decorator returns a :class:`senko.Group`.
    """

    def __init__(self, *args, **kwargs):
        case_insensitive = kwargs.pop("case_insensitive", True)
        super().__init__(*args, case_insensitive=case_insensitive, **kwargs)

    def __repr__(self):
        return f"<senko.Group qualified_name={self.qualified_name!r}>"

    def command(self, *args, **kwargs):
        cls = kwargs.pop("cls", senko.Command)
        return super().command(*args, cls=cls, **kwargs)

    def group(self, *args, **kwargs):
        cls = kwargs.pop("cls", senko.Group)
        return super().command(*args, cls=cls, **kwargs)

    # Unfortunately both invoke and reinvoke have to be completely copied
    # to make the call to get_command use the locale provided by the context.
    #
    # The invoke and reinvoke methods that follow are copied from discord.py.
    # Source: https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py
    # License: https://github.com/Rapptz/discord.py/blob/master/LICENSE

    async def invoke(self, ctx):
        ctx.invoked_subcommand = None
        ctx.subcommand_passed = None
        early_invoke = not self.invoke_without_command
        if early_invoke:
            await self.prepare(ctx)

        view = ctx.view
        previous = view.index
        view.skip_ws()
        trigger = view.get_word()

        if trigger:
            ctx.subcommand_passed = trigger
            # Look up the command using the locale. This is the only change.
            ctx.invoked_subcommand = self.get_command(trigger, locale=ctx.locale)

        if early_invoke:
            injected = hooked_wrapped_callback(self, ctx, self.callback)
            await injected(*ctx.args, **ctx.kwargs)

        if trigger and ctx.invoked_subcommand:
            ctx.invoked_with = trigger
            await ctx.invoked_subcommand.invoke(ctx)
        elif not early_invoke:
            view.index = previous
            view.previous = previous
            await super().invoke(ctx)

    async def reinvoke(self, ctx, *, call_hooks=False):
        ctx.invoked_subcommand = None
        early_invoke = not self.invoke_without_command
        if early_invoke:
            ctx.command = self
            await self._parse_arguments(ctx)

            if call_hooks:
                await self.call_before_hooks(ctx)

        view = ctx.view
        previous = view.index
        view.skip_ws()
        trigger = view.get_word()

        if trigger:
            ctx.subcommand_passed = trigger
            # Look up the command using the locale. This is the only change.
            ctx.invoked_subcommand = self.get_command(trigger, locale=ctx.locale)

        if early_invoke:
            try:
                await self.callback(*ctx.args, **ctx.kwargs)
            except:
                ctx.command_failed = True
                raise
            finally:
                if call_hooks:
                    await self.call_after_hooks(ctx)

        if trigger and ctx.invoked_subcommand:
            ctx.invoked_with = trigger
            await ctx.invoked_subcommand.reinvoke(ctx, call_hooks=call_hooks)
        elif not early_invoke:
            # undo the trigger parsing
            view.index = previous
            view.previous = previous
            await super().reinvoke(ctx, call_hooks=call_hooks)
