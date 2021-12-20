.. currentmodule:: onami

What's new?
================

Version 2.3.2
-------------

Fixed a regression from 2.3.1 that made permtrace return bad results on 1.7.2


Version 2.3.1
-------------

This is a patch release to fix a number of issues with permtrace and improve ``__main__``.


Version 2.3.0
-------------

No changelog for this version.


Version 2.2.0
-------------

The ``oni sudo``, ``oni su`` and ``oni in`` commands have been removed and replaced with a single command that handles all three at once.

``oni exec`` now automatically handles IDs or mentions for channels, users, or threads (only with nextcord v2.0a+).
Aliases with a postfix ``!`` bypass checks and cooldowns, like ``oni sudo`` used to do.

Example of how the commands change with this release:

- ``oni su @user command`` -> ``oni exec @user command``
- ``oni in #channel command`` -> ``oni exec #channel command``
- ``oni in #channel oni su @user command`` -> ``oni exec #channel @user command`` or ``oni exec @user #channel command``
- ``oni sudo command`` -> ``oni exec! command``

This allows combinations that were previously not possible, for example,
``oni exec! #channel @user command`` now executes a command as a user in another channel or thread, bypassing any checks or cooldowns that user or channel has against the command.

The flag system (i.e. the ``onami_FLAG=...`` system) has been rewritten to use various degrees of lazy evaluation.
This means setting flags like ``onami_HIDE`` and ``onami_RETAIN`` need only precede loading the onami extension, as opposed to the entire module.

Flags that only evaluated at command runtime will now have their changes take effect immediately.
For example, executing ``os.environ['onami_NO_UNDERSCORE'] = '1'`` no longer requires a reload to take effect.

A programmatic interface for flags is available, however, its use is discouraged except in subclass initialization, due to the fact that the changes will **NOT** persist across reloads of the extension.

.. code:: python3

    onami.Flags.NO_UNDERSCORE = True

The ``oni invite`` command has been added, which is a developer convenience command that supplies the invite link for the bot it is ran on.
This command is most useful for bots that predate the behavior change that merged bot and application IDs, saving the time of having to retrieve the application ID yourself.

Permissions can be supplied, e.g., ``oni invite kick_members manage_messages`` will create an invite requesting those two permissions.

The invites produced request slash commands for convenience.

Some regressions have been fixed and other internal cleanup has been addressed in this release.

Version 2.1.0
-------------

A new implementation of PaginatorInterface has been created using nextcord's interaction buttons system.
It is available when using nextcord 2.0.0 or greater (currently alpha).

onami will now avoid uploading files either when detecting the author is on mobile or through an explicit ``onami_FORCE_PAGINATOR`` switch.
This is to better support mobile platforms that do not have inline file previews yet. (`PR #111 <https://github.com/Gorialis/onami/pull/111>`_).

Humanize has been removed as a dependency. Selftest now uses nextcord's own relative timestamp formatting markdown extension for timing,
and pretty printing of memory usage has been implemented within the Feature itself.

Version 2.0.0
--------------

Python version changes
~~~~~~~~~~~~~~~~~~~~~~~

Python version 3.7 has been dropped. onami 2.0 requires Python 3.8 or greater.

New commands
~~~~~~~~~~~~~

- ``oni rtt``
    Calculates the round-trip time between your bot and the nextcord API.
    Reports exact values as well as an average and standard deviation.

- ``oni dis``
    Disassembles a given piece of Python code in REPL context, returning the bytecode.
    This does not actually execute the code, but can be used to identify compiler behavior and optimizations.

- ``oni permtrace``
    Calculates the effect of permissions and overwrites on a given member or set of roles in a channel.
    This can be used to identify why a member does, or does not, have a permission in a given place.

Command improvements
~~~~~~~~~~~~~~~~~~~~~
- ``oni``
    Information on sharding status for both automatically and manually sharded bots is now displayed.

    The root 'oni' command can now be sanely overridden, removed, or renamed using the Feature system.

- ``oni py`` / ``oni pyi``
    Exceptions now display the line from which they originate, instead of just the line number.

    Large results that fit within the nextcord preview threshold are now uploaded as files,
    for better navigability.

- ``oni sh``
    Timeout has been increased from 90 seconds from invocation, to 120 seconds from the last output.

    This should reduce the chance of termination from long-running installs or other processes.

- ``oni source``
    Triple backticks inside of source files no longer cause the file content to spill outside of its codeblock.

    Large results that fit within the nextcord preview threshold are now uploaded as files,
    for better navigability.

- ``oni vc``
    Voice commands no longer appear if their relevant dependencies are not installed.

- ``oni shutdown``
    Now uses ``bot.close`` to prevent deprecation warnings.

    Fixed a regression with braille J support.

API changes
~~~~~~~~~~~~

- Feature system
    The Feature system has been implemented as a means to solve subclassing problems with onami.

    Certain functionality can now be disabled in subclasses, additional commands can be easily facilitated
    without affecting the native onami cog, and overriding subcommands or groups is now possible without
    needing to reimplement commands that would otherwise become orphaned in the process.

- PaginatorInterface
    Updating mechanism has been entirely rewritten to better prevent cascades of message edits.

    This change has also made it possible to synchronously trigger interface updates, paving the way for
    possible native stream or TextIO support in the future.
