{
  description = "Croctalk";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, }:
  let
    supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    nixpkgsFor = forAllSystems (system: import nixpkgs { inherit system; config.allowUnfree = true;  overlays = [  ];  });
  in {
    nixosModules = forAllSystems (system:
    let
      pkgs = nixpkgsFor.${system};
    in
    {
      croctalk =  import ./module;
    });

    packages = forAllSystems (system:
    let
      pkgs = nixpkgsFor.${system};
    in
    {
      croctalk = pkgs.callPackage ./package { };
    });

    croctalk = forAllSystems (system: self.packages.${system}.croctalk);


    devShells = forAllSystems (system:
    let
      pkgs = nixpkgsFor.${system};
    in
    {
      default =
        let
          python = pkgs.python312.override { };
        in
        pkgs.mkShell {
          packages = [
            (python.withPackages (ps: with ps; [
              python-telegram-bot
              openai-whisper
              python-dotenv
            ]))
          ];
        };
      });
    };
  }

