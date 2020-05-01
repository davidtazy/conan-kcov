#https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html



# download sources
conan source . --source-folder=tmp/source

#install dependancies
conan install . --install-folder=tmp/build --profile default


#build
conan build . --source-folder=tmp/source --build-folder=tmp/build

#package
conan package . --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package

#make it available locally
conan export-pkg . davidtazy/testing --source-folder=tmp/source --build-folder=tmp/build --profile=default

#test it
conan test ./test_package kcov/0.0.0@davidtazy/testing
