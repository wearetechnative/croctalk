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
        src = ./.;  # Points to the current directory where the package code is

        # Add any dependencies your package needs

        propagatedBuildInputs = with pkgs.python3Packages; [ 
          torch-bin
          torchaudio-bin
          librosa
          jiwer
          datasets
          transformers
          evaluate
          accelerate
          pip
          torchvision
          pycuda
          langchain
          langchain-community
          openai
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

