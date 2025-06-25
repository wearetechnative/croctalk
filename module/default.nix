{
  config,
  pkgs,
  lib,
  ...
}:
let
  cfg = config.services.croctalk;
  defaultUser = "croctalk";
  defaultGroup = defaultUser;
  defaultSpaceDir = "/var/lib/croctalk";
in
{
  options = {
    services.croctalk = {
      enable = lib.mkEnableOption "";

      user = lib.mkOption {
        type = lib.types.str;
        default = defaultUser;
        example = "yourUser";
        description = ''
          The user to run croctalk as.
          By default, a user named `${defaultUser}` will be created.
        '';
      };

      group = lib.mkOption {
        type = lib.types.str;
        default = defaultGroup;
        example = "yourGroup";
        description = ''
          The group to run croctalk under.
          By default, a group named `${defaultGroup}` will be created.
        '';
      };

      envFile = lib.mkOption {
        type = lib.types.nullOr lib.types.path;
        default = "${defaultSpaceDir}/.env";
        example = "/etc/croctalk.env";
        description = ''
          File containing extra environment variables. For example:

          ```
          # Twenty api token
          TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwZmU3NjFiOC02ZDMyLTRkYTQtYTBmNC1iZjlkNzYwMGZhOTkiLCJ0eXBlIjoiQVBJX0tFWSIsIndvcmtzcGFjZUlkIjoiMGZlNzYxYjgtNmQzMi00ZGE0LWEwZjQtYmY5ZDc2MDBmYTk5IiwiaWF0IjoxNzM4NTg3MDgzLCJleHAiOjQ4OTIxODcwODIsImp0aSI6ImY1MjdhNjllLTY0NGQtNDRkOC04OGRmLTZjZjBiMmQ2MmJlMSJ9.kLK-4thMP_7yhR_EDUFZhkyQiG3GddIzNZQSRE7RqBI

          # Twenty site
          SITE=example.com

          # Telegram bot token
          BOT_TOKEN=

          # Whisper model (tiny, base, small, medium, large or turbo )
          WHISPER_MODEL=small

          ```
        '';
      };
    };
  };

  config = lib.mkIf cfg.enable {
    systemd.services.croctalk = {
      description = "croctalk service";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];

      serviceConfig = {
        Type = "simple";
        User = "${cfg.user}";
        Group = "${cfg.group}";
        EnvironmentFile = lib.mkIf (cfg.envFile != null) "${cfg.envFile}";
        ExecStart =
          "${config.system.path}/bin/croctalk";
        Restart = "on-failure";
      };
    };

    users.users.${defaultUser} = lib.mkIf (cfg.user == defaultUser) {
      isSystemUser = true;
      group = cfg.group;
      description = "croctalk daemon user";
    };

    users.groups.${defaultGroup} = lib.mkIf (cfg.group == defaultGroup) { };
  };

  meta = {
    maintainers = with lib.maintainers; [ Caspersonn ];
  };
}
