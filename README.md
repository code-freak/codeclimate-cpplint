# cpplint as CodeClimate plugin

Runs [cpplint](https://github.com/cpplint/cpplint) as [CodeClimate](https://codeclimate.com/) plugin to check
your C/C++ source code against Google's style guide.

**Warning:** This image is unofficial and not included in the default CodeClimate distribution.

## Config
```yaml
plugins:
  cpplint:
    enabled: true
    config:
      # Every config entry is passed as --argument to cppcheck
      filter: "-,+whitespace,-whitespace/ending_newline"
```

## Usage
Currently only in custom codeclimate builds or in dev mode by cloning this repository and build it with
`docker build -t codeclimate/codeclimate-cpplint .`. You can then run codeclimate by using the `--dev` flag. This
will pick up local build images that are not available in the default engines list.