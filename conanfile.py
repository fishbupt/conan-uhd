from conans import ConanFile, CMake, tools
import os


class UhdConan(ConanFile):
    name = "uhd"
    version = "003.010.001.001"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    folder_name = "release_%s" % version.replace(".", "_")

    def source(self):
        zip_name = "%s.zip" % self.folder_name
        url = "https://github.com/EttusResearch/uhd/archive/%s" % zip_name
        self.output.info("Downloading %s..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake= CMake(self)
        if self.options.shared:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        cmake.definitions["ENABLE_DOXYGEN"] = "OFF"
        cmake.definitions["ENABLE_EXAMPLES"] = "OFF"
        cmake.definitions["ENABLE_MANUAL"] = "OFF"
        cmake.definitions["ENABLE_MAN_PAGES"] = "OFF"
        cmake.definitions["ENABLE_TESTS"] = "OFF"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder
        cmake.configure(source_dir="../uhd-%s/host" % self.folder_name, build_dir="./build")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs= ["uhd"]
