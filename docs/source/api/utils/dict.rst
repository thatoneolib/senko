.. _utils_dict:

Case Insensitive Dict
#####################

This case insensitive dict implementation is used in the custom commands
framework. It should be mostly compatible with the regular :class:`dict`
implementation, but there are no guarantees made regarding more complex
use cases, such as compatibility with the new dictionary merge operators.

.. autoclass:: senko.utils.CaseInsensitiveDict
    :members:
