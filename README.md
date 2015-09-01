
zerowiki
========

Zerowiki is an extremely simple wiki-esque system using markdown. It's just some JavaScript in `index.html`, which you place in any directory that is accessible via HTTP, and you're good to go.


Usage
-----

By default, zerowiki will try to display the contents of a file called `index.md` in the same directory as `index.html`. Make this your landing page. Create other markdown documents in the same directory and link between them using normal markdown syntax. Zerowiki will handle the markdown rendering for you, as long as the relative path of the document is prepended by a `?`, which happens automatically for markdown links to local `.md` documents.


Features
--------

Markdown files will be rendered as HTML using [marked](https://github.com/chjj/marked), with code-block highlighting from [google-code-prettify](https://github.com/google/code-prettify). By default, [this github-style CSS](https://github.com/sindresorhus/github-markdown-css) is used for styling, but you can modify `index.html` to use any CSS you like (try [these](http://jasonm23.github.io/markdown-css-themes/avenir-white.html) for example).

Zerowiki will override the CSS to style local (same host) links green. If you link to any local (non-`.md`) or remote file it will be accessed normally (as per your web server). Section links are styled red, and external links are styled blue. To disable this behaviour, change `colorLinks` to `false` in `index.html`.

Since there is a delay between document ready and the markdown being fetched via ajax, browsers that support scroll-resume on page reload will not be able to scroll-resume (as the document will be temporarily empty). To fix this, the document is made extremely tall until the markdown is loaded. If this causes compatability issues with your browser, post an issue and I will make that option configurable.

If you find this useful, throw me a line. Feel free to submit bug reports.