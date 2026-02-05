{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "sinmix-shell";

  buildInputs = [
    # Python3 with matplotlib included
    (pkgs.python3.withPackages (ps: with ps; [ matplotlib ]))
  ];

  shellHook = ''
    echo "Welcome to the SinMix Nix shell!"
    echo "Python version: $(python --version)"
  '';
}
