from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os

class KcovConan(ConanFile):
    name = "kcov"
    version = "0.0.0"
    license = "<Put the package license here>"
    author = "davidtazy"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Kcov here>"
    topics = ("coverage", "linux", "debug")
    settings = "os", "compiler", "build_type", "arch" #todo
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    requires = ["zlib/1.2.11",
                "libiberty/9.1.0",
                "libcurl/7.64.1"]
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/davidtazy/kcov.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("kcov/CMakeLists.txt", "project (kcov)",
                              '''project (kcov)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def system_requirements(self):
        required_package = None
        if 0: # self.settings.os == "Linux": #does not work for me
        
            if tools.os_info.linux_distro in ["ubuntu", "debian"]:
                required_package = "libdw-dev"
            elif tools.os_info.linux_distro in ["fedora", "centos"]:
                required_package = "elfutils-libs"
            elif tools.os_info.linux_distro == "opensuse":
                required_package = "libdw-devel"
            elif tools.os_info.linux_distro == "arch":
                required_package = "libelf"

            
            if tools.os_info.linux_distro in ["ubuntu", "debian"]:
                required_package = "binutils-dev"
            elif tools.os_info.linux_distro in ["fedora", "centos", "opensuse"]:
                required_package = "binutils-devel"
            elif tools.os_info.linux_distro == "arch":
                required_package = "binutils"
            elif tools.os_info.is_freebsd:
                required_package = "libbfd"
        
        if required_package != None:
            installer = tools.SystemPackageTool()
            if not installer.installed(required_package):
                raise ConanInvalidConfiguration("kcov requires {}.".format(required_package))


    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="kcov")
        cmake.build()

    def package(self):
        self.copy("*", dst="bin", src="bin")
    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

