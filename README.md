# ADCIRC Spack Package

ADCIRC's cmake system can be used with the Spack (https://spack.io) package management system. This documentation
provides a brief guide for setting up and building ADCIRC via the Spack system

## Installation and Initial Setup

### Installing Spack

If Spack is not currently installed on your system, you can install it using git:

```bash
$ git clone -c feature.manyFiles=true https://github.com/spack/spack.git ~/spack
```

In the above example, Spack will be installed in the user's home directory in a directory
called `spack`. Spack has few requirements and it is heavily customizable. 

Once spack is installed, you will need to initialize the environment. Assuming that the environment
was installed to the user's home path as shown above, the command to initialize is:
```bash
$ source ~/spack/share/spack/setup-env.sh
```
Note that this command will need to be run each time the shell is initialized. If you want to add spack to your 
default environment, you will need to modify your `~/.bashrc or ~/bash_profile` to run this command at startup.

Often, rather than placing the source command in the `~/.bashrc` directly, it is more useful to alias the command as 
follows:

```bash
$ alias spack-setup=`source ~/spack/share/spack/setup-env.sh`
```

### Initializing the ADCIRC Spack repository

Spack organizes collections of packages into "repositories". In the case of ADCIRC, the repository is
currently maintained outside the official spack repository (though this may change in the future after user testing occurs).

To add the ADCIRC spack repository to your instance, use the command:

```bash
$ spack repo add /path/to/adcirc_repository/spack 
```
This assumes that the string `/path/to/adcirc_repository` is the root directory of the ADCIRC package.

Note that this command only needs to be run once per spack installation.

### System Compiler Configuration

While Spack can easily build compilers from source or binary which are not currently installed on the target system,
sometimes it is useful to use those which are already configured on the system to ensure compatibility with Infiniband or 
other system specific configurations. 

Spack can locate available compilers on the system using the command:
```bash
$ spack compiler find
```
Note that for some systems which use modules, you may need to load the compilers before running the find command

Additionally, if you wish to use system libraries (including mpi), you can specify them as externals. You can allow spack
to automatically detect these libraries using this command:
```bash
$ spack external find
```
or, by specifying manually using the packages.yaml file in either the user or system directory. Additional information
for manual specification of external packages can be found [here](https://spack.readthedocs.io/en/latest/build_settings.html#external-packages).

Note that this is not an exhaustive tutorial for the setup of Spack and users should consult the Spack documentation 
and tutorials directly for comprehensive instructions. 

## Building ADCIRC

The ADCIRC build process enabled by spack should be straight forward. To view the information on the ADCIRC package, you
can run the command:

```bash
$ spack info adcirc
```

This will print out a listing of available versions and options for use within the spack package. Unless you have specific needs,
it is recommended to use the preferred version. 

```bash
$ spack install adcirc@56.0.2
```

The default build will build adcirc and all dependencies from source as specified by your spack configuration. This 
will build (by default) ADCIRC in serial and parallel with netCDF enabled. Additional executables (such as `adcswan`, 
`padcswan`, and `aswip`) can be enabled by specificying additional flags to Spack as shown below:

```bash
$ spack install adcirc +swan +aswip
```

If you'd like to change the compiler that is used to build adcirc, you can pass that using:

```bash
$ spack install adcirc %oneapi
```
This will build ADCIRC using the Intel-LLVM (i.e. Intel OneAPI) compilers. Note that only ADCIRC version 56.00+ 
is compatible with the Intel-LLVM compiler suite. Note that you'll need to ensure these compilers are installed/enabled
before executing the above command:

### Installing Intel OneAPI Compilers 
```bash
$ spack install intel-oneapi-compilers
$ spack activate intel-oneapi-compilers
$ spack compiler find
$ spack deactivate intel-oneapi-compilers
```

Following that, you should see output like below showing the new Intel compilers (intel, oneapi, and dpcpp) installed:
```bash
$ spack compilers
==> Available compilers
-- dpcpp debian11-x86_64 ----------------------------------------
dpcpp@2022.2.1

-- gcc debian11-x86_64 ------------------------------------------
gcc@10.2.1

-- intel debian11-x86_64 ----------------------------------------
intel@2021.7.1

-- oneapi debian11-x86_64 ---------------------------------------
oneapi@2022.2.1
```

Another variant would be to enable the system to build OpenMPI from source using Intel-LLVM with SLURM support:

```bash
$ spack install adcirc ^openmpi+legacylaunchers schedulers=slurm %oneapi
```

If you'd like to build with your specific mpi library, you should provide the specification that matches the 
one defined in your `packages.yaml`. This will force the system to build with the system MPI rather than one
it tries to build itself.

```bash
$ spack install adcirc ^openmpi@4.2.0%gcc
```
