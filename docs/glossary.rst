.. _glossary:

========
Glossary
========

.. glossary::
   :sorted:

   REST
      REpresentational State Transfer. More a philosophy than a protocol, REST
      states that each resource must have a distinct and permanent URL, and that
      the resource must be queryable using a query string in the :term:`URL`
      rather than via an opaque XML-RPC or SOAP API.

   HTTP
      HyperText Transfer Protocol. The protocol that enables a browser to load
      a web page using an unambiguous identifier in the form of a :term:`URL`.

   URL
      Uniform Resource Locator. A string that idenfies the location of a
      resource. http://www.example.com/ is a URL. The formal syntax is:

      ``scheme://[username[:password@]]domain[:port]/path[?query_string][#anchor]``

      http://en.wikipedia.org/wiki/Uniform_Resource_Locator

   JSON
      JavaScript Object Notation. A representation of data in text, using the
      Javascript language syntax for data structures. JSON is also the native
      document format of some NoSQL document stores.

      http://www.json.org/

   UUID
      Universally Unique Identifier, also known as a GUID (Globally Unique
      Identifier) in Windows. UUIDs are long, random numbers that are pretty
      much guaranteed to be unique. They are recommended for database primary
      keys in distributed databases, where records may have to be inserted
      during a network partition.

      A UUID is a 16-byte (128-bit) number. The number of theoretically possible
      UUIDs is therefore about 3 × 10 :sup:`38`. In its canonical form, a UUID consists
      of 32 hexadecimal digits, displayed in 5 groups separated by hyphens, in
      the form ``8-4-4-4-12`` for a total of 36 characters (32 digits and 4
      hyphens). For example: ``550e8400-e29b-41d4-a716-446655440000``. There are
      five versions or types of UUIDs. Type 4 is completely random and therefore
      the default choice.

      http://en.wikipedia.org/wiki/Universally_Unique_Identifier

   SQL
      Structured Query Language, the standard for querying relational databases.

   API
      Application Programming Interface, a documented mechanism for third-party
      software to interact with the application.
