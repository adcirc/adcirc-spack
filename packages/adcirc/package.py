# ----------------------------------------------------------------------------#
#
#     spack install adcirc
#
# You can edit this file again by typing:
#
#     spack edit adcirc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------#
#
# ----------------------------------------------------------------------------#
#                                                                             #
#                              ADCIRC                                         #
#                                                                             #
#    A (PARALLEL) ADVANCED CIRCULATION MODEL FOR SHELVES, COASTAL SEAS        #
#                         AND ESTUARIES                                       #
#                                                                             #
#                                                                             #
#                          DEVELOPED BY:                                      #
#                                                                             #
#                      DR. R.A. LUETTICH, JR                                  #
#                                                                             #
#             UNIVERSITY OF NORTH CAROLINA AT CHAPEL HILL                     #
#                   INSTITUTE OF MARINE SCIENCES                              #
#                                                                             #
#                        DR. J.J. WESTERINK                                   #
#                                                                             #
#          DEPARTMENT OF CIVIL ENGINEERING AND GEOLOGICAL SCIENCES            #
#                     UNIVERSITY OF NOTRE DAME                                #
#                       NOTRE DAME, IN 46556                                  #
#                                                                             #
#                                                                             #
#        MAJOR FUNDING FOR THE DEVELOPMENT OF ADCIRC WAS PROVIDED BY          #
#                                                                             #
#                       DEPARTMENT OF THE ARMY                                #
#                    WATERWAYS EXPERIMENT STATION                             #
#                 COASTAL ENGINEERING RESEARCH CENTER                         #
#                        3909 HALLS FERRY RD                                  #
#                      VICKSBURG, MI 39180-6199                               #
#                                                                             #
# ----------------------------------------------------------------------------#
#                                                                             #
#          THE ADCIRC SOURCE CODE IS COPYRIGHTED, 1994-2022 BY:               #
#                                                                             #
#                 R.A. LUETTICH, JR AND J.J. WESTERINK                        #
#                                                                             #
# ----------------------------------------------------------------------------#

from spack.package import *


class Adcirc(CMakePackage):
    """ADCIRC: The ADvanced CIRCulation model for simulation of time dependent, free surface circulation and transport in two and three dimensions"""

    # ...Metadata
    homepage = "https://www.adcirc.org"
    maintainers = ["zcobell"]
    license("LGPL-v3.0")

    # ...Package location and sample archive name
    git = "https://github.com/adcirc/adcirc.git"
    url = (
        "https://github.com/adcirc/adcirc/releases/download/v55.02/adcirc_v55.02.tar.gz"
    )

    # ...ADCIRC versions
    version(
        "56.0.2",
        sha256="74e0dff04ae25200f4bf3cc7b0f344595770e70b193a9ea928e76a86b17d83ba",
        preferred=True,
    )
    version(
        "56.0.1",
        sha256="cba0663722cfbfcc2c49dd01facb525d8ad49fe5f41c2017ce81173e3618b862",
        deprecated=True,
    )
    version(
        "56.0.0",
        sha256="2c53ebe89eb1bc1a6426781fdf9f8fdd8cb93261bfedb6afd59b94b926fc1c78",
        deprecated=True,
    )
    version(
        "55.02",
        sha256="10029efccf25796f5190d9ace89af5b371bf874b746de6116543ee136e9334ee",
    )
    version(
        "55.01",
        sha256="fa42ff973e157634ed6bedae9465067928944901524cc255c561b24db2d41b27",
        deprecated=True,
    )
    version(
        "55.00",
        sha256="0de3bbdeb69b8809d668d511f10e8f4784f253d278e1985c3bbd3907725142d7",
        deprecated=True,
    )
    version(
        "54.02",
        sha256="cb1aca0cc7a0b1b0c4cc91ad71a2ac2cbefc0a16d5ff25d6d2833e75b0fc5262",
    )
    version(
        "54.01",
        sha256="ff31a458c529f7ad970cf4ae099cbf0da9e949ad35af01be1e23e19dbb0ca6ca",
        deprecated=True,
    )
    version(
        "54.00",
        sha256="6c2ac516b7ebb0508e2f3fdc684170f78b6f0e949f6ebcf98dc9208e304f3d18",
        deprecated=True,
    )

    version("main", branch="main")

    # ...Build variants
    variant(
        "netcdf", default=True, description="Build with with netCDF4 format enabled"
    )
    variant(
        "grib",
        default=False,
        description="Builds the model with GRIB format enabled",
        when=("@55:+netcdf"),
    )
    variant(
        "xdmf",
        default=False,
        description="Builds the model with XDMF3 format support",
    )

    variant("mpi", default=True, description="Builds the parallel executables")
    variant(
        "swan", default=False, description="Builds the tightly coupled SWAN wave model"
    )
    variant(
        "libshared", default=False, description="Builds libadcirc as a shared library"
    )
    variant(
        "libstatic", default=False, description="Builds libadcirc as a static library"
    )
    variant("aswip", default=False, description="Builds aswip")
    variant(
        "utilities", default=False, description="Builds the adcirc utilities package"
    )

    # ...Dependencies
    depends_on("c", type="build")  
    depends_on("fortran", type="build")
    depends_on("cmake@3:", type="build")
    depends_on("perl", type="build", when="+swan")
    depends_on("hdf5~mpi~threadsafe", when="+netcdf", type=("build", "link"))
    depends_on("netcdf-c@4:~mpi", when="+netcdf", type=("build", "link"))
    depends_on("netcdf-fortran@4:", when="+netcdf", type=("build", "link"))
    depends_on("mpi", when="+mpi", type=("build", "link"))
    depends_on("jpeg", when="+grib", type=("build", "link"))
    depends_on("xdmf3~mpi+fortran", when="+xdmf", type=("build", "link"))
    depends_on("hdf5~mpi~threadsafe", when="+xdmf", type=("build", "link"))
    depends_on("netcdf-c@4:~mpi", when="+xdmf", type=("build", "link"))
    depends_on("netcdf-fortran@4:", when="+xdmf", type=("build", "link"))

    def url_for_version(self, version):
        """
        Note that there is a slight difference in naming once we move to the new
        python packaging system, so this handles that
        """
        if version >= Version("56.0.0"):
            url_fmt = "https://github.com/adcirc/adcirc/releases/download/v{0}/adcirc-v{0}.tar.gz"
        else:
            url_fmt = "https://github.com/adcirc/adcirc/releases/download/v{0}/adcirc_v{0}.tar.gz"
        return url_fmt.format(version)

    def cmake_args(self):
        args = []

        if "+netcdf" in self.spec or "+xdmf" in self.spec:
            args.append(self.define("ENABLE_OUTPUT_NETCDF", True))
            args.append(self.define("NETCDFHOME", self.spec["netcdf-c"].prefix))
            args.append(
                self.define("NETCDF_F90_ROOT", self.spec["netcdf-fortran"].prefix)
            )

        if "+grib" in self.spec:
            args.append(self.define("ENABLE_GRIB2", True))
            args.append(self.define("ENABLE_DATETIME", True))

        if "+xdmf" in self.spec:
            args.append(self.define("ENABLE_OUTPUT_XDMF", True))
            args.append(self.define("XDMFHOME", self.spec["xdmf3"].prefix))

        if "+swan" in self.spec:
            args.append(self.define("BUILD_ADCSWAN", True))

        if "+mpi" in self.spec:
            args.append(self.define("BUILD_PADCIRC", True))
            args.append(self.define("BUILD_ADCPREP", True))
            if "+swan" in self.spec:
                args.append(self.define("BUILD_PADCSWAN", True))

        if "+libshared" in self.spec:
            args.append(self.define("BUILD_LIBADCIRC_SHARED", True))

        if "+libstatic" in self.spec:
            args.append(self.define("BUILD_LIBADCIRC_STATIC", True))

        if "+aswip" in self.spec:
            args.append(self.define("BUILD_ASWIP", True))

        if "+utilities" in self.spec:
            args.append(self.define("BUILD_UTILITIES", True))

        # ...The gcc10+ fix. ADCIRC is generally ok without this but certain
        #   mpi flavors will cause issues
        if self.spec.satisfies("%gcc@10:"):
            args.append(self.define("CMAKE_Fortran_FLAGS", "-fallow-argument-mismatch"))

        args.append(self.define("BUILD_ADCIRC", True))
        return args
