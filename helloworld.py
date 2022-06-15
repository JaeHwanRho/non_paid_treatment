#!/usr/bin/env python3

print("content-type:text/html; charset=uft-8\n")
print()

import cgi
form = cgi.FieldStorage()
pageId = form["id"].value

print('''<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
  </head>
  <body class="vsc-initialized">
    <header>
      <title>info.cern.ch</title>
    </header>

    <h1>http://info.cern.ch - home of the first website</h1>
    <h1>내용이 수정됨 in Apache Server</h1>
    <p>From here you can:</p>
    <ul>
      <li><a href="helloworld.py?id=HTML">HTML</a></li>
      <li><a href="helloworld.py?id=CSS">CSS</a></li>
      <li><a href="http://home.web.cern.ch/topics/birth-web">Learn about the birth of the web</a></li>
      <li><a href="http://home.web.cern.ch/about">Learn about CERN, the physics laboratory where the web was born</a></li>
    </ul>
    <h2>{title}</h2>

    </body>
</html>
'''.format(title=pageId))
