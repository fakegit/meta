<h1 align="center">
  <br>
  <a href="https://github.com/s0md3v/meta"><img src="https://i.ibb.co/s1dFjnR/meta.png" alt="meta"></a>
</h1>

<h4 align="center">Explains and tests HTTP response headers</h4>

<p align="center">
  <a href="https://github.com/s0md3v/meta/releases">
    <img src="https://img.shields.io/github/release/s0md3v/meta.svg">
  </a>
  <a href="https://travis-ci.com/s0md3v/meta">
    <img src="https://img.shields.io/travis/com/s0md3v/meta.svg">
  </a>
  <a href="https://github.com/s0md3v/meta/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/s0md3v/meta.svg">
  </a>
</p>

![demo](https://i.ibb.co/cC6Qs9M/Screenshot-2019-01-12-19-42-50.png)

#### Features
- Describe response headers
- Check for missing security headers
- Check for misconfigurations
    - CORS
    - Cookie

more to come...

#### Installation [Optional]
Navigate to `meta` directory and run the following command as root:

`make install`

#### Documentation

Testing a website's response headers is pretty straight forward:

`python meta.py -u http://example.com`

The output can be strictly formatted to JSON as follows:

`python meta.py -u http://example.com --json`
