# CrocTalk

Croctalk, Talk your way in to Twenty.

<img src="croctalk.svg" width="250" height="250">
![render test](croctalk.svg)

<!-- PROJECT SHIELDS -->

## Install

### Configure environment vars

Create a .env-file or set environment vars.

```bash
# Twenty api token
TOKEN=

# Twenty site 
SITE=example.com

# Telegram bot token
BOT_TOKEN=

# Where to save the txt files (these are tmp files)
SAVE_DIR_TXT=/tmp/croctalk-text

# Where to save the voice files (these are tmp files)
SAVE_DIR_VOICE=/tmp/croctalk-voice

# Whisper model (tiny, base, small, medium, large or turbo )
WHISPER_MODEL=small
```

### Without Nix

Install requirements with Pip of if you have a working nix with flake enabled.

### Devlopment with nix

```
nix develop
python -m croctalk.main
```

### Install on nixos

```
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    croctalk.url = "github:wearetechnative/croctalk"
  };
  outputs = { nixpkgs, croctalk, ... }: {
    nixosConfigurations.<name> = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [ 
          croctalk.packages."${system}".croctalk # croctalk Package
          croctalk.nixosModules.${system}.croctalk # croctalk Module
      ];
    };
  };
}
```

### Croctalk Module
Create an `croctalk.env` file in `/etc`, look at `.env.sample`.
``` 
{ croctalk, ... }:

{
  services.croctalk = {
    enable  = true;
    envFile = "/etc/croctalk.env"; # Default
    group   = "croctalk"; # Default
    user    = "croctalk"; # Default
  };
}
```

## CONTRIBUTE

### Issues, Bugs, and Feature Requests

File issue requests [in this repo](https://github.com/wearetechnative/croctalk/issues/new)

### Open Source & Contributing

Croctalk is open source and we appreciate contributions and positive feedback.

### Docs for Project Maintainers

Read the docs and roadmaps

- [Release runbook](RELEASE-RUNBOOK.md)
- [Roadmap](TODO.md)
- [Changelog](CHANGELOG.md)

## Credits


## License and Copyright

Copyright 2025 [TechNative B.V.](https://technative.eu) | Published under the [Apache License](LICENSE).
