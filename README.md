# A dynamic documentation server `dds`
A small Flask server that serves documentation (or any static HTML/Markdown).
Inspired by [Harp](http://harpjs.com/), but with Sphinx websites in mind.

## Installation

__These instructions assume `git`, `pip`, and `python` are on the PATH.__

```
// Clone and install
git clone http://github.com/andrewmfiorillo/dds.git
pushd dds && pip install . && popd
```

## Usage

To launch the server:
```bash
// options are:
//   <config_file> - Default is "~/.dds/config.json". The CLI flags take priority over config file's.
//   <public_dir>  - Default is "~/.dds/public". The directory to serve files.
//   <bind_ip>     - Default is "0.0.0.0". The IP to bind to.
//   <bind_port>   - Default is 8001. The port to listen on.
dds <public_dir> --listen <bind_ip> --port <bind_port> --config <config_file>
```

## License

MIT License

Copyright (c) 2018 Andrew Fiorillo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.