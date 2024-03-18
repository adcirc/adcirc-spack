# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gahm
#
# You can edit this file again by typing:
#
#     spack edit gahm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Gahm(CMakePackage):
    """GAHM: The Generalized Asymmetric Holland Model."""

    homepage = "https://www.adcirc.org"
    git = "https://github.com/adcirc/gahm.git"
    url = "https://github.com/adcirc/gahm/releases/download/v0.0.1/gahm_v0.0.1.tar.gz"

    maintainers("zcobell")
    version("main", branch="main", preferred=True)

    variant("fortran", default=False, description="Build the Fortran module")
    variant("python", default=False, description="Builds the pygahm module")
    variant("shared", default=True, description="Build the shared library object")
    variant("static", default=False, description="Build the static library object")
    variant("system_boost", default=False, description="Use the system boost instead of spack")

    depends_on("boost@1.71:", type=("build", "link"), when="~system_boost")
    depends_on("python@3:", type=("build", "link"), when="+python")
    depends_on("swig@4:", type=("build"), when="+python")

    def cmake_args(self):
        args = []

        if "+fortran" in self.spec:
            args.append(self.define("GAHM_ENABLE_FORTRAN", True))

        if "+python" in self.spec:
            args.append(self.define("GAHM_ENABLE_PYTHON", True))
            args.append(self.define("PYTHON_PACKAGE_BUILD", True))
            args.append(self.define("Python3_ROOT_DIR",self.spec["python"].prefix)) 

        if "+shared" in self.spec:
            args.append(self.define("GAHM_ENABLE_SHARED", True))
        if "+static" in self.spec:
            args.append(self.define("GAHM_ENABLE_STATIC", True))

        return args
