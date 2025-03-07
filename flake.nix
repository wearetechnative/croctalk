{
  description = "Croctalk";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: 
    let
      system = "x86_64-linux";

      
      openai-overlay  = final: prev: {
        openai-whisper = prev.openai-whisper.override {
          torch = [
            prev.torch-bin
          ];
        };
      };
      pkgs = import nixpkgs { inherit system; config.allowUnfree = true; overlay = [ openai-overlay ]; };

    in {
      packages.${system}.croctalk = pkgs.python3Packages.buildPythonPackage rec {
        pname = "croctalk";
        version = "0.1.0";
        src = ./.;

        propagatedBuildInputs = with pkgs.python3Packages; [ 
          torch-bin
          langchain
          langchain-community
          openai-whisper
          pydub
          python-dotenv
          requests
          tiktoken
          telegram-text
          python-telegram-bot
        ];
      };
      
      # Expose the default package
      defaultPackage.${system} = self.packages.${system}.croctalk;

      # Create an app for the command-line interface
      apps.${system}.croctalk = {
        type = "app";
        program = "${self.packages.${system}.croctalk}/bin/croctalk";  # This is where the executable is
      };
    }; 
}

