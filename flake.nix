{
  description = "Croctalk";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, }: 
  let
    openai-overlay  = final: prev: {
      openai-whisper = prev.python312Packages.openai-whisper.override {
        torch = [
          prev.torch-bin
        ];
      };
    };
    supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    nixpkgsFor = forAllSystems (system: import nixpkgs { inherit system; config.allowUnfree = true; config.cudaSupport= true; overlays = [  ];  });
  in {    
    packages = forAllSystems (system:
    let
      pkgs = nixpkgsFor.${system};
    in
    {
      croctalk = pkgs.callPackage ./package.nix { };
    });

    defaultPackage = forAllSystems (system: self.packages.${system}.croctalk);


    devShells = forAllSystems (system:
    let
      pkgs = nixpkgsFor.${system};
    in
    {
      default = pkgs.mkShell {
        buildInputs = with pkgs; [
          self.packages.${system}.croctalk
        ];
      };
    });
  };
}

