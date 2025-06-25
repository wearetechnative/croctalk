# TODO/ROADMAP


## Version v0.1.1

- [x] Cuda support for NVIDIA GPU's 


## Version v0.1.0

- [x] extra cli arguments:
 - [ ] --envfile
 - [x] --version
 - [x] --help
 - [ ] --temporary
- [x] nix package to run via Flake
- [x] nix module to include with these options via Flake

```nix
services.croctalk = {
  enable = true
  envFile = /var/secrets/.env
}
```
- [x] implementation howto for suitable for nix users
- [x] new release using the [release runbook](RELEASE-RUNBOOK.md)

## Backlog

- Multiple providers like Whatsapp, Slack or Signal 
- Full documentation
- PR in nixos/nixpkgs
- Logo and header info about TechNative
