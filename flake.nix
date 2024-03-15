{
  description = "Automated Decision Making";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";

    tsplib95.url = "github:rhgrant10/tsplib95";
  };

  outputs = inputs@{ nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python311;
          tsplib95 = python.pkgs.buildPythonPackage {
            name = "tsplib95";
            src = inputs.tsplib95;
            pyproject = true;
            propagatedBuildInputs = with python.pkgs; [ setuptools pytest-runner tabulate deprecated networkx ];
          };
        in
        {
          devShells =
            {
              default = pkgs.mkShell {
                packages = [
                  (python.withPackages (ps: with ps; [
                    pip
                    python-lsp-server
                    python-lsp-black
                    pylsp-mypy
                    pylsp-rope
                    python-lsp-ruff
                    ujson
                    isort

                    numpy
                    matplotlib
                    tsplib95
                  ]))
                ];
              };
            };
        });
}
