#https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html

mkdir conan-kcov
git clone "this" recipe


# download sources
conan source recipe --source-folder=tmp/source

#install dependancies
conan install recipe --install-folder=tmp/build --profile default


#build
conan build recipe --source-folder=tmp/source --build-folder=tmp/build

#package
conan package recipe --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package

#make it available locally
conan export-pkg recipe user/channel --source-folder=tmp/source --build-folder=tmp/build --profile=default

#test it
conan test recipe/test_package kcov/0.0.0@davidtazy/testing