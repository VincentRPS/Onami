.. currentmodule:: onami

onami as an API
=================

onami contains numerous internal classes and functions it uses to facilitate
both the commands in the `cog <cog.html>`_ and miscellaneous parts of bot development.

You can use almost all of these for your own use, but be aware that the internals
of onami, and how they work, are subject to change.

Most of the content in this document is autogenerated.

REPL-related classes and functions
----------------------------------

.. currentmodule:: onami.repl.scope

.. autoclass:: Scope
    :members:

.. autofunction:: get_parent_scope_from_var

.. autofunction:: get_parent_var

.. currentmodule:: onami.repl.compilation

.. autoclass:: AsyncCodeExecutor
    :members:

.. currentmodule:: onami.shell

.. autoclass:: ShellReader
    :members:

Function-related tools
-----------------------

.. currentmodule:: onami.functools

.. autofunction:: executor_function


Paginator-related tools
-----------------------

.. currentmodule:: onami.paginators

.. autoclass:: PaginatorInterface
    :members:

.. autoclass:: PaginatorEmbedInterface
    :members:

.. autoclass:: FilePaginator
    :members:

.. autoclass:: WrappedPaginator
    :members:

Help command classes
--------------------

These are classes you can use, or subclass yourself, for help commands.

You can use them like this:

.. code:: python3

    from nextcord.ext import commands

    from onami.help_command import MinimalPaginatorHelp

    bot = commands.Bot('?', help_command=MinimalPaginatorHelp())

.. currentmodule:: onami.help_command

.. autoclass:: DefaultPaginatorHelp
    :members:

.. autoclass:: DefaultEmbedPaginatorHelp
    :members:

.. autoclass:: MinimalPaginatorHelp
    :members:

.. autoclass:: MinimalEmbedPaginatorHelp
    :members:
