#/usr/bin/bash

rm -rf data/*
wget -P data http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Training_Images.zip
wget -P data http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Test_Images.zip

pushd data
unzip GTSRB_Final_Training_Images.zip
unzip GTSRB_Final_Test_Images.zip
popd
