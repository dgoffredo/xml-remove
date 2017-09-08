xml-remove
==========
Filter out XML elements matching any of a set of XPath queries.

Why
---
I had a bunch of `<Proxy>` elements to remove from a configuration file, but
only those whose `<ServiceId>` child had one of several values.

What
----
`xml-remove.py` takes as command line arguments one or more [XPath][xpath]
queries and uses them to filter XML from standard input into standard output.
XML elements that match any of the provided XPath queries are omitted from the
output.

`xml-remove.py` mostly leaves the rest of the XML untouched, except that since
the entire input is read into an XML document and then printed back out, there
are some minor formatting changes:

- The script writes its own XML declaration (e.g.
  `<?xml version='1.0' encoding='UTF-8'?>`) unless instructed to omit it.
- It uses double quotes in attribute values (except in the XML declaration,
  where it uses single quotes).
- It collapses redudant whitespace between attributes.
- It collapses empty elements into one-tag elements, e.g. `<foo></foo>` becomes
  `<foo/>`.

Notably, though, the whitespace between elements is preserved.

This behavior is at the discretion of the implementation of `lxml.etree`, which
the script uses to do its XML parsing, XPath selection, and XML printing.

Usage
-----
### `--help`
```
usage: xml-remove.py [-h] [--no-declaration] [xpath [xpath ...]]

Remove elements from XML (stdin -> stdout).

positional arguments:
  xpath             XPath query whose matches will be remove
optional arguments:
  -h, --help        show this help message and exit
  --no-declaration  omit XML declaration
```

### Example

```
$ cat example/input.xml
<?xml version="1.0" encoding="UTF-8" ?>
<Configuration>
    <weird> white
  space!
        </weird>

    <tag attr1='single quotes' attr2="double quotes"    />

  <thing/>
    <thing foo='bar'>hi
    </thing>

  <!-- This is a comment -->

  <thing>stuff</thing>

</Configuration>
$ echo "Now we'll filter out the last <thing> element.\n"
Now we'll filter out the last <thing> element.

$ ./xml-remove.py '/Configuration/thing[text()="stuff"]' <example/input.xml
<?xml version='1.0' encoding='UTF-8'?>
<Configuration>
    <weird> white
  space!
        </weird>

    <tag attr1="single quotes" attr2="double quotes"/>

  <thing/>
    <thing foo="bar">hi
    </thing>

  <!-- This is a comment -->

</Configuration>$ echo "It's gone.\n"
It's gone.

$
```

More
----
`xml-remove` depends on:

- python2.7 (e.g. the debian package `python2.7`)
- [lxml][lxml] for python 2.7 (e.g. the debian package `python-lxml`)

[xpath]: https://www.w3.org/TR/xpath/
[lxml]: http://lxml.de/