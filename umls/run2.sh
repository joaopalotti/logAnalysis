
PUBLICMMPATH="/home/palotti/Dropbox/tuwien/PhD/umls/public_mm"

export CLASSPATH=".:${PUBLICMMPATH}/src/javaapi/dist/MetaMapApi.jar:${PUBLICMMPATH}/src/javaapi/dist/prologbeans.jar:${PUBLICMMPATH}/opencsv-2.4.jar"

javac myApi2.java

# ./run2.sh -i input.gz -o output.csv -n <numberOfLines> -a (?append)
java myApi2 $@

