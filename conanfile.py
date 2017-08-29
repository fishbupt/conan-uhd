from conans import ConanFile, CMake, tools
import os


class UhdConan(ConanFile):
    name = "uhd"
    version = "003.010.001.001"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"enable_static": [True, False]}
    default_options = "enable_static=False", "Boost:shared=True", "Boost:fPIC=True"
    requires = "Boost/1.62.0/lasote/stable"
    generators = "cmake"
    folder_name = "release_%s" % version.replace(".", "_")

    def source(self):
        zip_name = "%s.zip" % self.folder_name
        url = "https://github.com/EttusResearch/uhd/archive/%s" % zip_name
        self.output.info("Downloading %s..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

        # Intergrate conan with cmake
        tools.replace_in_file("uhd-%s/host/CMakeLists.txt" % self.folder_name, "PROJECT(UHD CXX C)", '''PROJECT(UHD CXX C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake= CMake(self)
        if self.options.enable_static:
            cmake.definitions["ENABLE_STATIC_LIBS"] = "ON"

        cmake.definitions["ENABLE_DOXYGEN"] = "OFF"
        cmake.definitions["ENABLE_EXAMPLES"] = "OFF"
        cmake.definitions["ENABLE_MANUAL"] = "OFF"
        cmake.definitions["ENABLE_MAN_PAGES"] = "OFF"
        cmake.definitions["ENABLE_TESTS"] = "OFF"
        # cmake.definitions["ENABLE_UTILS"] = "OFF"
        # cmake.definitions["ENABLE_OCTOCLOCK"] = "OFF"
        # cmake.definitions["ENABLE_X300"] = "OFF"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder
        cmake.configure(source_dir="uhd-%s/host" % self.folder_name)
        cmake.build()
        cmake.install()

        # download and install FPGA&FW images
        self.run("python ./utils/uhd_images_downloader.py")

    def package_info(self):
        self.cpp_info.libs= ["uhd"]
