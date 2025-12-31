{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "my-dev-env";

  buildInputs = with pkgs; [
    python312Packages.textual
    python312Packages.textual-dev
    python312Packages.pandas-stubs
    python312Packages.pandas
    python312Packages.numpy
  ];

  shellHook = ''
    echo "Welcome to your Nix shell environment!"
    echo "Python version: $(python3 --version)"
  '';
}
