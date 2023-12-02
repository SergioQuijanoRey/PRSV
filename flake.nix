{
    description = "Flake to handle some tasks and dependencies for this project";
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
        utils.url = "github:numtide/flake-utils";
    };

    outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let

        python = "python312";
        pkgs = nixpkgs.legacyPackages.${system};

        # Define a custom python enviroment
        custom_python_packages = pp: [
            pp.pytest
            pp.python-lsp-server
        ];
        custom_python_env = pkgs.${python}.withPackages custom_python_packages;

        # Packages that we are going to use in both shells, for coding and for
        # writing the Latex thesis
        shared_packages = [];

      in {

        # Packages that we use in `nix develop`
        devShells.default = pkgs.mkShell {
            buildInputs = shared_packages ++ [
                # Use our custom python enviroment
                custom_python_env
            ];


            # Add some paths to PYTHONPATH
            PYTHONPATH = "${custom_python_env}/${custom_python_env.sitePackages}:.:./src:./src/lib";

            # To install some packages using pip
            # shellHook = ''
            #     if [ ! -d ".venv" ]; then
            #         python3 -m venv .venv;
            #     fi
            #     source .venv/bin/activate;

            #     # Install some packages that are not present in nix repos
            #     pip install python-lsp-server

            #     # Log that we're in a custom enviroment
            #     echo "❄️  Running custom dev enviroment with python and other packages"
            # '';
        };
    });
}
