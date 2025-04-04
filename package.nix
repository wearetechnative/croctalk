{ pkgs }:

pkgs.python3Packages.buildPythonPackage rec {
  pname = "croctalk";
  version = "0.1.2";
  src = ./.;

  propagatedBuildInputs = with pkgs.python3Packages; [ 
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
}
