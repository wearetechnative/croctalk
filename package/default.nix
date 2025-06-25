{ lib
, python3Packages
, python
, ...
 }:

python3Packages.buildPythonPackage rec {
  pname = "croctalk";
  version = "0.2.0";
  src = ./..;

  propagatedBuildInputs = with python3Packages; [
    python-telegram-bot
    openai-whisper
    python-dotenv
  ];
}
