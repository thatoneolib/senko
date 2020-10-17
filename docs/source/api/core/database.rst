.. _database:

Database
########

The database connection pool is initialized using a helper function that
prepares each acquired connection with custom type codecs.

Type Codecs
***********

The following types, encoders and decoders are registered.

======================= =============================== ========================
Type                    Encoder                         Decoder
======================= =============================== ========================
``JSONB``               :func:`json.dumps`              :func:`json.loads`
======================= =============================== ========================

Reference
*********

.. autofunction:: senko.init_db
