# TaskOrc CLI

The `orc` binary. A [GitHub CLI-style](https://oclif.io) Node.js CLI that plugin skills invoke as a subprocess to read and write TaskOrc data. Not intended for direct use.

## Overview

- **Binary** — `orc`
- **Framework** — [oclif](https://oclif.io)
- **Runtime** — Node.js 22+, npm

## Development

```bash
npm install
npm run build   # tsc → dist/
npm link        # makes orc available globally
```

After `npm link`, skills can invoke `orc` commands from anywhere.

## Commands

Commands are organized by resource: `orc auth`, `orc project`, `orc task`, etc. Run `orc --help` for the full list once built.

## Testing & Linting

```bash
npm test        # mocha
npm run lint    # eslint
```

## Publishing

```bash
npm run version   # regenerates oclif command docs in README
npm publish
```

Install globally from npm:

```bash
npm install -g taskorc
```

## Project Structure

```
cli/
  src/
    commands/    # one file per orc subcommand
  test/          # mocha tests
  package.json
  tsconfig.json
```
