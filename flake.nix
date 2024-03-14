{
  description = "Automated Decision Making";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          devShells =
            {
              default = pkgs.mkShell {
                packages = with pkgs; [
                  clang-tools_16
                  clang_16
                  fmt
                  gdb
                  gnumake
                  bear

                  python310
                  mypy
                  black

                  hexyl
                ];
              };
            };
        });
}
