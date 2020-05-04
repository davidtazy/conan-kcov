from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os

class KcovConan(ConanFile):
    name = "kcov"
    version = "0.0.0"
    license = "GPL-2.0"
    author = "davidtazy"
    url = "https://github.com/davidtazy/conan-kcov"
    description = "Code coverage tool for compiled programs, Python and Bash which uses debugging information to collect and report data without special compilation options"
    topics = ("coverage", "linux", "debug")
    settings = "os", "compiler", "build_type", "arch" 
    #options = {"shared": [True, False]}
    #default_options = {"shared": False}
    requires = ["zlib/1.2.11",
                "libiberty/9.1.0",
                "libcurl/7.64.1"]
    generators = "cmake"

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            raise ConanInvalidConfiguration("kcov can not be built by Visual Studio.")

    def source(self):
        self.run("git clone https://github.com/SimonKagstrom/kcov.git")
        #inject conan deps
        tools.replace_in_file("kcov/CMakeLists.txt", "project (kcov)",
                              '''project (kcov)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def system_requirements(self):
        required_package = []
        if  self.settings.os == "Linux": 
        
            if tools.os_info.linux_distro in ["ubuntu", "debian"]:
                required_package.append( "libdw-dev" )
            elif tools.os_info.linux_distro in ["fedora", "centos"]:
                required_package.append(  "elfutils-libs")
            elif tools.os_info.linux_distro == "opensuse":
                required_package.append( "libdw-devel")
            elif tools.os_info.linux_distro == "arch":
                required_package.append(  "libelf" )

            
            if tools.os_info.linux_distro in ["ubuntu", "debian"]:
                required_package.append(  "binutils-dev")
            elif tools.os_info.linux_distro in ["fedora", "centos", "opensuse"]:
                required_package.append(  "binutils-devel")
            elif tools.os_info.linux_distro == "arch":
                required_package.append(  "binutils")
            elif tools.os_info.is_freebsd:
                required_package.append(  "libbfd")
        
        
        installer = tools.SystemPackageTool()
        installer.install(required_package)
                


    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="kcov")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder="kcov")
        cmake.install()

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)

