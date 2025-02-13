{
  description = "Croctalk";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: 
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };

    in {
      packages.${system}.croctalk = pkgs.python3Packages.buildPythonPackage rec {
        pname = "croctalk";
        version = "0.1.0";
        src = ./.;

        propagatedBuildInputs = [ 
          pkgs.openai-whisper
          pkgs.python3Packages.torch-bin
          pkgs.python3Packages.torchaudio-bin
          pkgs.python3Packages.langchain
          pkgs.python3Packages.langchain-community
          #openai-whisper
          pkgs.python3Packages.pydub
          pkgs.python3Packages.python-dotenv
          pkgs.python3Packages.requests
          pkgs.python3Packages.tiktoken
          pkgs.python3Packages.telegram-text
          pkgs.python3Packages.python-telegram-bot
        ];
      };
      
      defaultPackage.${system} = self.packages.${system}.croctalk;

      apps.${system}.croctalk = {
        type = "app";
        program = "${self.packages.${system}.croctalk}/bin/croctalk";
      };
    }; 
}

