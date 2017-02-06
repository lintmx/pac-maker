# pac-maker

A Proxy Auto-config file generator.

## Usage

```
$ ./make.py -h
usage: make.py [-h] [-s ADDRESS] [--method METHOD] [-w ADDRESS] [-b ADDRESS]
               [--delete] [-u] [-c] [-o PATH]

A tool to quickly generate proxy auto-config files.

optional arguments:
  -h, --help            show this help message and exit
  -s ADDRESS, --special ADDRESS
                        Add a rule to special list.
  --method METHOD       Set special rule method.
  -w ADDRESS, --white ADDRESS
                        Add a rule to white list.
  -b ADDRESS, --black ADDRESS
                        Add a rule to black list.
  --delete              Delete rule action.
  -u, --update          Update China ip list.
  -c, --compression     Compress the pac file.
  -o PATH, --out PATH   Write output to file

```

## Thanks

[Flora_Pac](https://github.com/Leask/Flora_Pac)

[mono_pac](https://github.com/blackgear/mono_pac)

## License

MIT
